from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.connection import get_db
from app.database.models import Building

router = APIRouter()

@router.get("/latest")
def get_latest_buildings(
    limit: int = Query(10, ge=1, le=1000, description="Количество записей"),
    db: Session = Depends(get_db)
):
    """Вернуть N последних записей"""
    buildings = db.query(Building).order_by(desc(Building.property_id)).limit(limit).all()
    return {"total": len(buildings), "buildings": buildings}

@router.get("/{property_id}")
def get_building_by_id(
    property_id: int,
    db: Session = Depends(get_db)
):
    """Вернуть запись по ID"""
    building = db.query(Building).filter(Building.property_id == property_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building
