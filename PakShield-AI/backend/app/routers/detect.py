import os
import json
import base64
import aiofiles
import uuid
import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.scan import ScanResponse, ImageVariantsResponse
from app.services.detection_service import process_detection, generate_image_variants
from app.services.default_user import get_default_user
from app.config import get_settings

router = APIRouter(prefix="/api/detect", tags=["Detection"])
settings = get_settings()

ALLOWED = {"png", "jpg", "jpeg"}
MAX_SIZE = settings.max_upload_size


def validate_image(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in ALLOWED


@router.post("", response_model=ScanResponse)
async def detect_currency(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not validate_image(file.filename or ""):
        raise HTTPException(status_code=400, detail="Only PNG, JPG, JPEG allowed")

    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")

    ext = file.filename.rsplit(".", 1)[-1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(settings.upload_dir, filename)

    os.makedirs(settings.upload_dir, exist_ok=True)
    async with aiofiles.open(filepath, "wb") as f:
        await f.write(content)

    user = await get_default_user(db)
    record = await process_detection(db, user.id, filepath)

    return ScanResponse(
        id=record.id,
        result=record.result,
        confidence=record.confidence,
        denomination=record.denomination,
        serial_number=record.serial_number,
        features=json.loads(record.features_json) if record.features_json else None,
        processing_time_ms=record.processing_time_ms,
        created_at=record.created_at,
    )


@router.post("/variants", response_model=ImageVariantsResponse)
async def get_image_variants(file: UploadFile = File(...)):
    if not validate_image(file.filename or ""):
        raise HTTPException(status_code=400, detail="Only PNG, JPG, JPEG allowed")

    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")

    nparr = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image file")

    variants = generate_image_variants(img)
    return ImageVariantsResponse(**variants)
