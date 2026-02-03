from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import desc

from app.database.connection import get_db
from app.database.models import LkpArea

router = APIRouter()

@router.get("/latest")
def get_latest_areas(
    limit: int = Query(10, ge=1, le=1000, description="Количество записей"),
    db: Session = Depends(get_db)
):
    """Вернуть N последних записей"""
    areas = db.query(LkpArea).order_by(desc(LkpArea.area_id)).limit(limit).all()
    return {"total": len(areas), "areas": areas}

@router.get("/{area_id}")
def get_area_by_id(
    area_id: int,
    db: Session = Depends(get_db)
):
    """Вернуть запись по ID"""
    area = db.query(LkpArea).filter(LkpArea.area_id == area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    return area


@router.get("/all")
def get_all_areas(
    db: Session = Depends(get_db)
):
    """Получить список всех районов"""
    areas = db.query(LkpArea).all()
    return {
        "total": len(areas),
        "areas": [
            {
                "area_id": area.area_id,
                "name_en": area.name_en,
                "name_ar": area.name_ar,
                "municipality_number": area.municipality_number
            }
            for area in areas
        ]
    }
