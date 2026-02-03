from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_, or_, case

from app.database.connection import get_db
from app.database.models import Transaction, Unit

router = APIRouter()

TRANSACTION_FIELDS = [
    "transaction_id",
    "instance_date",
    "trans_group_id",
    "trans_group_en",
    "trans_group_ar",
    "procedure_id",
    "procedure_name_en",
    "procedure_name_ar",
    "property_type_id",
    "property_type_en",
    "property_type_ar",
    "property_sub_type_id",
    "property_sub_type_en",
    "property_sub_type_ar",
    "property_usage_en",
    "property_usage_ar",
    "area_id",
    "area_name_en",
    "area_name_ar",
    "trans_value",
    "meter_sale_price",
    "actual_worth",
    "rent_value",
    "meter_rent_price",
    "no_of_parties_role_1",
    "party_type_role_1_en",
    "party_type_role_1_ar",
    "no_of_parties_role_2",
    "party_type_role_2_en",
    "party_type_role_2_ar",
    "no_of_parties_role_3",
    "master_project_en",
    "master_project_ar",
    "project_number",
    "project_name_en",
    "project_name_ar",
    "rooms_en",
    "rooms_ar",
    "has_parking",
    "nearest_landmark_en",
    "nearest_landmark_ar",
    "nearest_metro_en",
    "nearest_metro_ar",
    "nearest_mall_en",
    "nearest_mall_ar",
    "is_free_hold",
    "reg_type_id",
    "reg_type_en",
    "reg_type_ar",
    "procedure_area",
    "building_name_en",
    "building_name_ar",
    "trans_size_sqft",
    "trans_size_sqm",
    "actual_area_sqft",
    "actual_area_sqm",
]


def _serialize_value(v):
    """Сериализация значений для JSON"""
    if v is None:
        return None
    if isinstance(v, (date, datetime)):
        return v.isoformat()
    if isinstance(v, Decimal):
        return float(v)
    return v


def transaction_to_dict(t: Transaction) -> dict:
    """Преобразовать Transaction в словарь"""
    return {key: _serialize_value(getattr(t, key, None)) for key in TRANSACTION_FIELDS if hasattr(t, key)}


@router.get("/latest")
def get_latest_transactions(
    limit: int = Query(50, ge=1, le=1000, description="Количество записей"),
    db: Session = Depends(get_db),
):
    """Получить последние транзакции"""
    transactions = db.query(Transaction).order_by(desc(Transaction.instance_date)).limit(limit).all()
    return {
        "total": len(transactions),
        "transactions": [transaction_to_dict(t) for t in transactions],
    }


@router.get("/by-property")
def get_transactions_by_property_info(
    area_id: Optional[int] = Query(None, description="ID района"),
    building_name: Optional[str] = Query(None, description="Название здания"),
    project_number: Optional[int] = Query(None, description="Номер проекта"),
    min_price: Optional[float] = Query(None, ge=0, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, ge=0, description="Максимальная цена"),
    transaction_type: Optional[str] = Query(None, description="Тип транзакции (Sales, Mortgages, Gifts)"),
    limit: int = Query(100, ge=1, le=500, description="Лимит результатов"),
    db: Session = Depends(get_db),
):
    """Поиск транзакций по характеристикам недвижимости"""
    query = db.query(Transaction)
    
    # Фильтры
    if area_id:
        query = query.filter(Transaction.area_id == area_id)
    
    if building_name:
        query = query.filter(
            or_(
                Transaction.building_name_en.ilike(f"%{building_name}%"),
                Transaction.building_name_ar.ilike(f"%{building_name}%"),
            )
        )
    
    if project_number:
        query = query.filter(Transaction.project_number == project_number)
    
    if min_price is not None:
        query = query.filter(Transaction.trans_value >= Decimal(str(min_price)))
    
    if max_price is not None:
        query = query.filter(Transaction.trans_value <= Decimal(str(max_price)))
    
    if transaction_type:
        query = query.filter(Transaction.trans_group_en == transaction_type)
    
    transactions = query.order_by(desc(Transaction.instance_date)).limit(limit).all()
    
    return {
        "total_found": len(transactions),
        "filters": {
            "area_id": area_id,
            "building_name": building_name,
            "project_number": project_number,
            "min_price": min_price,
            "max_price": max_price,
            "transaction_type": transaction_type,
        },
        "transactions": [transaction_to_dict(t) for t in transactions],
    }


@router.get("/price-trends")
def get_price_trends(
    area_id: Optional[int] = Query(None, description="ID района"),
    property_type: Optional[str] = Query(None, description="Тип недвижимости"),
    months_back: int = Query(12, ge=1, le=60, description="Количество месяцев назад"),
    db: Session = Depends(get_db),
):
    """Получить тренды цен по месяцам"""
    today = date.today()
    start_date = today - timedelta(days=months_back * 30)
    
    query = db.query(
        func.date_trunc('month', Transaction.instance_date).label('month'),
        func.avg(Transaction.meter_sale_price).label('avg_price_per_sqm'),
        func.count(Transaction.transaction_id).label('transaction_count'),
        func.avg(Transaction.trans_value).label('avg_transaction_value')
    ).filter(
        Transaction.instance_date >= start_date,
        Transaction.trans_group_en == 'Sales',  # Только продажи
        Transaction.meter_sale_price.isnot(None),
        Transaction.trans_value.isnot(None)
    )
    
    if area_id:
        query = query.filter(Transaction.area_id == area_id)
    
    if property_type:
        query = query.filter(Transaction.property_type_en == property_type)
    
    trends = query.group_by(
        func.date_trunc('month', Transaction.instance_date)
    ).order_by(
        func.date_trunc('month', Transaction.instance_date)
    ).all()
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": today.isoformat(),
            "months_back": months_back
        },
        "filters": {
            "area_id": area_id,
            "property_type": property_type
        },
        "trends": [
            {
                "month": month.strftime("%Y-%m") if month else None,
                "avg_price_per_sqm": float(avg_price_per_sqm) if avg_price_per_sqm else None,
                "transaction_count": transaction_count,
                "avg_transaction_value": float(avg_transaction_value) if avg_transaction_value else None
            }
            for month, avg_price_per_sqm, transaction_count, avg_transaction_value in trends
        ]
    }


@router.get("/{transaction_id}")
def get_transaction_by_id(
    transaction_id: str,
    db: Session = Depends(get_db),
):
    """Получить транзакцию по ID"""
    transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")
    return transaction_to_dict(transaction)