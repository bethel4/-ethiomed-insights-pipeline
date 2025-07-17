from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ProductAnalytics(BaseModel):
    product_name: str
    mention_count: int
    avg_price: Optional[float]
    channels: List[str]

class ChannelActivity(BaseModel):
    channel_name: str
    message_count: int
    image_count: int
    last_activity: date

class MessageSearch(BaseModel):
    message_id: int
    text: str
    channel: str
    date: date
    has_media: bool
    detected_objects: List[str]

class TopProductsResponse(BaseModel):
    products: List[ProductAnalytics]
    total_count: int

class ChannelActivityResponse(BaseModel):
    activities: List[ChannelActivity]
    total_channels: int 