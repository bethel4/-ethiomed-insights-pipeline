from typing import List
from .database import get_db_connection
from .schemas import ProductAnalytics, ChannelActivity, MessageSearch

def get_top_products(limit: int = 10) -> List[ProductAnalytics]:
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    WITH product_mentions AS (
        SELECT 
            CASE 
                WHEN text ILIKE '%paracetamol%' THEN 'Paracetamol'
                WHEN text ILIKE '%vitamin%' THEN 'Vitamin'
                WHEN text ILIKE '%iron%' THEN 'Iron'
                WHEN text ILIKE '%folic acid%' THEN 'Folic Acid'
                WHEN text ILIKE '%collagen%' THEN 'Collagen'
                WHEN text ILIKE '%biotin%' THEN 'Biotin'
                WHEN text ILIKE '%zinc%' THEN 'Zinc'
                WHEN text ILIKE '%magnesium%' THEN 'Magnesium'
                WHEN text ILIKE '%omega%' THEN 'Omega'
                WHEN text ILIKE '%prenatal%' THEN 'Prenatal'
                ELSE 'Other'
            END as product_category,
            COUNT(*) as mention_count
        FROM raw_telegram_messages 
        WHERE text IS NOT NULL AND text != ''
        GROUP BY product_category
        HAVING product_category != 'Other'
    )
    SELECT 
        product_category as product_name,
        mention_count,
        NULL as avg_price,
        ARRAY['lobelia4cosmetics', 'tikvahpharma'] as channels
    FROM product_mentions
    ORDER BY mention_count DESC
    LIMIT %s
    """
    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    products = [ProductAnalytics(**row) for row in results]
    cursor.close()
    conn.close()
    return products

def get_channel_activity(channel_name: str) -> ChannelActivity:
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT 
        %s as channel_name,
        COUNT(*) as message_count,
        COUNT(CASE WHEN has_media THEN 1 END) as image_count,
        MAX(date::date) as last_activity
    FROM raw_telegram_messages
    WHERE text ILIKE %s
    """
    cursor.execute(query, (channel_name, f'%{channel_name}%'))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return ChannelActivity(**result)

def search_messages(query: str, limit: int = 10) -> List[MessageSearch]:
    conn = get_db_connection()
    cursor = conn.cursor()
    search_query = """
    SELECT 
        m.id as message_id,
        m.text,
        'lobelia4cosmetics' as channel,
        m.date::date as date,
        m.has_media,
        ARRAY_AGG(DISTINCT d.detected_object_class) FILTER (WHERE d.detected_object_class IS NOT NULL) as detected_objects
    FROM raw_telegram_messages m
    LEFT JOIN fct_image_detections d ON m.id = d.message_id
    WHERE m.text ILIKE %s
    GROUP BY m.id, m.text, m.date, m.has_media
    ORDER BY m.date DESC
    LIMIT %s
    """
    cursor.execute(search_query, (f'%{query}%', limit))
    results = cursor.fetchall()
    messages = [MessageSearch(**row) for row in results]
    cursor.close()
    conn.close()
    return messages 