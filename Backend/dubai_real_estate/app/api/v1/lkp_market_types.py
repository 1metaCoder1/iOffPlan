from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.connection import get_db
from app.database.models import LkpMarketType

router = APIRouter()

@router.get("/latest")
def get_latest_market_types(
    limit: int = Query(10, ge=1, le=1000, description="Количество записей"),
    db: Session = Depends(get_db)
):
    """Вернуть N последних записей"""
    market_types = db.query(LkpMarketType).order_by(desc(LkpMarketType.market_type_id)).limit(limit).all()
    return {"total": len(market_types), "market_types": market_types}

@router.get("/{market_type_id}")
def get_market_type_by_id(
    market_type_id: int,
    db: Session = Depends(get_db)
):
    """Вернуть запись по ID"""
    market_type = db.query(LkpMarketType).filter(LkpMarketType.market_type_id == market_type_id).first()
    if not market_type:
        raise HTTPException(status_code=404, detail="Market type not found")
    return market_type
