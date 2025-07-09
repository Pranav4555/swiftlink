import os
import io
import qrcode
import base64
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas, database, auth

router = APIRouter()

RENDER_BASE_URL = "https://swiftlink-4y8p.onrender.com"

@router.post("/shorten", response_model=schemas.URLInfo)
def create_short_url(
    request: schemas.URLCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    short_key = base64.urlsafe_b64encode(os.urandom(4)).decode("utf-8").rstrip("=")
    short_url = f"{RENDER_BASE_URL}/{short_key}"  # ✅ Use public base URL

    # Generate QR code as base64
    qr = qrcode.make(short_url)
    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    new_url = models.URL(
        original_url=request.url,
        short_key=short_key,
        qr_code=qr_base64,
        owner_id=current_user.id
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return schemas.URLInfo(
        original_url=new_url.original_url,
        short_url=short_url,
        qr_code=qr_base64
    )

@router.get("/{short_key}")
def redirect_url(short_key: str, db: Session = Depends(database.get_db)):
    url = db.query(models.URL).filter(models.URL.short_key == short_key).first()
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")

    url.clicks += 1
    url.last_accessed = datetime.utcnow()
    db.commit()

    return RedirectResponse(url.original_url)

@router.get("/qr/{short_key}")
def get_qr(short_key: str, db: Session = Depends(database.get_db)):
    url = db.query(models.URL).filter(models.URL.short_key == short_key).first()
    if not url:
        raise HTTPException(status_code=404, detail="QR code not found")
    return {"qr_code_base64": url.qr_code}

@router.get("/qr/{short_key}/download")
def download_qr(short_key: str, db: Session = Depends(database.get_db)):
    url = db.query(models.URL).filter(models.URL.short_key == short_key).first()
    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    short_url = f"{RENDER_BASE_URL}/{short_key}"  # ✅ Use same public domain

    # Regenerate QR for download
    qr_img = qrcode.make(short_url)
    img_io = io.BytesIO()
    qr_img.save(img_io, format="PNG")
    img_io.seek(0)

    return StreamingResponse(
        img_io,
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename={short_key}.png"}
    )
