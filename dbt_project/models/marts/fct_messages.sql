SELECT
    message_id,
    text,
    message_date,
    has_media,
    media_type
FROM {{ ref('stg_telegram_messages') }} 