from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.connection import get_db
from app.database.models import LkpTransactionGroup

router = APIRouter()

@router.get("/latest")
def get_latest_transaction_groups(
    limit: int = Query(10, ge=1, le=1000, description="Количество записей"),
    db: Session = Depends(get_db)
):
    """Вернуть N последних записей"""
    groups = db.query(LkpTransactionGroup).order_by(desc(LkpTransactionGroup.group_id)).limit(limit).all()
    return {"total": len(groups), "transaction_groups": groups}

@router.get("/{group_id}")
def get_transaction_group_by_id(
    group_id: int,
    db: Session = Depends(get_db)
):
    """Вернуть запись по ID"""
    group = db.query(LkpTransactionGroup).filter(LkpTransactionGroup.group_id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Transaction group not found")
    return group
