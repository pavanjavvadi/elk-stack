from pydantic import BaseModel, EmailStr, PrivateAttr
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import json

# shipment Response model

class CustomerOut(BaseModel):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str
    products: str
    changed_by: int

class Shipment(BaseModel):
    id: str
    business_id_id: int
    tracking_number: str
    business_carrier_id_id: int
    shipment_type: str
    customer: CustomerOut
    status: str
    pickup_date: Optional[datetime]
    current_status_description: str
    pickup_from: str
    deliver_to: str
    shipment_time: Optional[datetime]
    is_active: Optional[str] = True
    has_changed: Optional[str] = False
    order_id: str
    extra_fields: Dict

class ShipmentIndex(BaseModel):

    def __init__(self, _index, _type, _id, _score, _source, highlight, sort):
        super().__init__(self)
        self.index = _index
        self.type = _type
        self.id = _id
        self.score = _score
        self.source = _source
        self.highlight = highlight
        self.sort = sort

    index: str
    type: str
    id: str
    score: float
    source: Shipment
    highlight: Dict
    sort: List


class Hits(BaseModel):
    total: Dict
    max_score: float = 0.0
    hits: List[ShipmentIndex]

class Shard(BaseModel):
    total: int
    successful: int
    skipped: int
    failed: int

class ShipmentIn(BaseModel):

    def __init__(__pydantic_self__, _shards, **data: Any) -> None:
        __pydantic_self__.shards = _shards
        super().__init__(**data)

    took: int
    timed_out: bool
    shards: Shard
    hits: Hits