from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any


class ScanResponse(BaseModel):
    id: str
    result: str
    confidence: float
    denomination: Optional[str] = None
    serial_number: Optional[str] = None
    features: Optional[dict[str, Any]] = None
    feature_scores: Optional[dict[str, float]] = None
    security_analysis: Optional[dict[str, Any]] = None
    reasons: Optional[list[str]] = None
    processing_time_ms: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ScanHistoryResponse(BaseModel):
    scans: list[ScanResponse]
    total: int
    page: int
    page_size: int


class ImageVariantsResponse(BaseModel):
    original: str
    grayscale: str
    red_channel: str
    green_channel: str
    blue_channel: str
    thermal: str
    edge: str
    hsv: str
    lab: str
    high_freq: str
    inverted: str
