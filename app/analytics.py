from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, auth

router = APIRouter()

@router.get("/me/analytics")
def my_analytics(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    urls = db.query(models.URL).filter(models.URL.owner_id == current_user.id).all()
    return [
        {
            "original_url": url.original_url,
            "short_key": url.short_key,
            "clicks": url.clicks,
            "last_accessed": url.last_accessed
        }
        for url in urls
    ]

@router.get("/analytics/{short_key}")
def shortlink_analytics(short_key: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    url = db.query(models.URL).filter(models.URL.short_key == short_key).first()
    if not url:
        raise HTTPException(status_code=404, detail="Short link not found")
    if url.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return {
        "original_url": url.original_url,
        "clicks": url.clicks,
        "created_at": url.created_at,
        "last_accessed": url.last_accessed
    }
