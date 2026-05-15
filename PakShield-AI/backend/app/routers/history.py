from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.scan import ScanHistoryResponse, ScanResponse
from app.services.detection_service import get_user_scans
from app.services.default_user import get_default_user
import json

router = APIRouter(prefix="/api/history", tags=["History"])


@router.get("", response_model=ScanHistoryResponse)
async def get_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    user = await get_default_user(db)
    scans, total = await get_user_scans(db, user.id, page, page_size)
    return ScanHistoryResponse(
        scans=[
            ScanResponse(
                id=s.id,
                result=s.result,
                confidence=s.confidence,
                denomination=s.denomination,
                serial_number=s.serial_number,
                features=json.loads(s.features_json) if s.features_json else None,
                processing_time_ms=s.processing_time_ms,
                created_at=s.created_at,
            )
            for s in scans
        ],
        total=total,
        page=page,
        page_size=page_size,
    )
