from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.connection import get_db
from app.database.models import LkpTransactionProcedure

router = APIRouter()

@router.get("/latest")
def get_latest_transaction_procedures(
    limit: int = Query(10, ge=1, le=1000, description="Количество записей"),
    db: Session = Depends(get_db)
):
    """Вернуть N последних записей"""
    procedures = db.query(LkpTransactionProcedure).order_by(
        desc(LkpTransactionProcedure.group_id), 
        desc(LkpTransactionProcedure.procedure_id)
    ).limit(limit).all()
    return {"total": len(procedures), "transaction_procedures": procedures}

@router.get("/{group_id}/{procedure_id}")
def get_transaction_procedure_by_id(
    group_id: int,
    procedure_id: int,
    db: Session = Depends(get_db)
):
    """Вернуть запись по ID"""
    procedure = db.query(LkpTransactionProcedure).filter(
        LkpTransactionProcedure.group_id == group_id,
        LkpTransactionProcedure.procedure_id == procedure_id
    ).first()
    if not procedure:
        raise HTTPException(status_code=404, detail="Transaction procedure not found")
    return procedure
