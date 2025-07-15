SELECT
    id AS message_id,
    text,
    date::date AS message_date,
    has_media,
    media_type
FROM {{ source('public', 'raw_telegram_messages') }} 