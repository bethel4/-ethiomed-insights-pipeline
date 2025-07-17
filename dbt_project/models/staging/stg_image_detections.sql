SELECT
    id AS detection_id,
    message_id,
    detected_object_class,
    confidence_score,
    bbox_x1,
    bbox_y1,
    bbox_x2,
    bbox_y2,
    created_at
FROM {{ source('public', 'fct_image_detections') }} 