import uuid
import time
import json
import os
import base64
import cv2
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.scan import ScanRecord
from app.ml.predictor import predict_image


async def process_detection(
    db: AsyncSession,
    user_id: str,
    image_path: str,
) -> ScanRecord:
    start = time.time()
    result = predict_image(image_path)
    elapsed = (time.time() - start) * 1000

    record = ScanRecord(
        user_id=user_id,
        image_path=image_path,
        result=result["label"],
        confidence=result["confidence"],
        denomination=result.get("denomination"),
        serial_number=result.get("serial_number"),
        features_json=json.dumps(result.get("features", {})),
        processing_time_ms=round(elapsed, 2),
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def get_user_scans(
    db: AsyncSession,
    user_id: str,
    page: int = 1,
    page_size: int = 10,
) -> tuple[list[ScanRecord], int]:
    from sqlalchemy import select, func

    query = (
        select(ScanRecord)
        .where(ScanRecord.user_id == user_id)
        .order_by(ScanRecord.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    count_query = select(func.count()).select_from(ScanRecord).where(ScanRecord.user_id == user_id)

    result = await db.execute(query)
    total = (await db.execute(count_query)).scalar() or 0
    return list(result.scalars().all()), total


def _encode(img: np.ndarray) -> str:
    success, buf = cv2.imencode(".png", img)
    if not success:
        return ""
    return base64.b64encode(buf.tobytes()).decode("utf-8")


def _ensure_3channel(gray: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def generate_image_variants(img: np.ndarray) -> dict[str, str]:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    b, g, r = cv2.split(img)
    red_img = cv2.merge([np.zeros_like(r), np.zeros_like(r), r])
    green_img = cv2.merge([np.zeros_like(g), g, np.zeros_like(g)])
    blue_img = cv2.merge([b, np.zeros_like(b), np.zeros_like(b)])

    thermal = cv2.applyColorMap(cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX), cv2.COLORMAP_JET)
    edges = cv2.Canny(gray, 50, 150)
    edges_colored = _ensure_3channel(edges)
    hsv_colored = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    lab_colored = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    mean_filter = cv2.blur(gray, (9, 9))
    high_pass = cv2.subtract(gray, mean_filter)
    high_pass = cv2.normalize(high_pass, None, 0, 255, cv2.NORM_MINMAX)
    high_pass_colored = _ensure_3channel(high_pass)

    inverted = cv2.bitwise_not(gray)
    inverted_colored = _ensure_3channel(inverted)

    return {
        "original": _encode(img),
        "grayscale": _encode(_ensure_3channel(gray)),
        "red_channel": _encode(red_img),
        "green_channel": _encode(green_img),
        "blue_channel": _encode(blue_img),
        "thermal": _encode(thermal),
        "edge": _encode(edges_colored),
        "hsv": _encode(hsv_colored),
        "lab": _encode(lab_colored),
        "high_freq": _encode(high_pass_colored),
        "inverted": _encode(inverted_colored),
    }
