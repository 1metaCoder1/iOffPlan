from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from app.database.connection import get_db
from app.database.models import Valuation

router = APIRouter()

@router.get("/latest")
def get_latest_valuations(
    limit: int = Query(10, ge=1, le=1000, description="Количество записей"),
    db: Session = Depends(get_db)
):
    """Вернуть N последних записей"""
    valuations = db.query(Valuation).order_by(desc(Valuation.procedure_id)).limit(limit).all()
    return {"total": len(valuations), "valuations": valuations}

@router.get("/{valuation_id}")
def get_valuation_by_id(
    valuation_id: int,
    db: Session = Depends(get_db)
):
    """Вернуть запись по ID"""
    valuation = db.query(Valuation).filter(Valuation.id == valuation_id).first()
    if not valuation:
        raise HTTPException(status_code=404, detail="Valuation not found")
    return valuation

@router.get("/by-project/{project_id}")
def get_valuations_by_project_id(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Получить все оценки по ID проекта"""
    valuations = db.query(Valuation).filter(
        Valuation.area_id == project_id
    ).all()
    
    return {
        "total": len(valuations),
        "project_id": project_id,
        "valuations": valuations
    }

@router.get("/by-area/{area_id}")
def get_valuations_by_area(
    area_id: int,
    db: Session = Depends(get_db)
):
    """Получить все оценки по району"""
    valuations = db.query(Valuation).filter(
        Valuation.area_id == area_id
    ).all()
    
    return {
        "total": len(valuations),
        "area_id": area_id,
        "valuations": valuations
    }

@router.get("/by-property-type/{property_type_id}")
def get_valuations_by_property_type(
    property_type_id: int,
    db: Session = Depends(get_db)
):
    """Получить все оценки по типу собственности"""
    valuations = db.query(Valuation).filter(
        Valuation.property_type_id == property_type_id
    ).all()
    
    return {
        "total": len(valuations),
        "property_type_id": property_type_id,
        "valuations": valuations
    }
