from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.v1.transactions import transaction_to_dict
from sqlalchemy.orm import Session, aliased
from sqlalchemy import desc, func, and_, or_, case, text
from sqlalchemy.sql import exists

from app.database.connection import get_db
from app.database.models import Unit, Transaction, Valuation, Project

router = APIRouter()

# Поля юнита в правильном порядке
UNIT_FIELDS = [
    "property_id",
    "area_id",
    "zone_id",
    "area_name_ar",
    "area_name_en",
    "land_number",
    "land_sub_number",
    "building_number",
    "unit_number",
    "unit_balcony_area",
    "unit_parking_number",
    "parking_allocation_type",
    "parking_allocation_type_ar",
    "parking_allocation_type_en",
    "common_area",
    "actual_common_area",
    "floor",
    "rooms",
    "rooms_ar",
    "rooms_en",
    "actual_area",
    "property_type_id",
    "property_type_ar",
    "property_type_en",
    "property_sub_type_id",
    "property_sub_type_ar",
    "property_sub_type_en",
    "parent_property_id",
    "grandparent_property_id",
    "creation_date",
    "munc_zip_code",
    "munc_number",
    "parcel_id",
    "is_free_hold",
    "is_lease_hold",
    "is_registered",
    "pre_registration_number",
    "master_project_id",
    "master_project_en",
    "master_project_ar",
    "project_id",
    "project_name_ar",
    "project_name_en",
    "land_type_id",
    "land_type_ar",
    "land_type_en",
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


def unit_to_dict(u: Unit) -> dict:
    """Преобразовать Unit в словарь"""
    return {key: _serialize_value(getattr(u, key, None)) for key in UNIT_FIELDS if hasattr(u, key)}


@router.get("/latest")
def get_latest_units(
    limit: int = Query(10, ge=1, le=1000, description="Количество записей"),
    include_transactions: bool = Query(False, description="Включить последние транзакции"),
    db: Session = Depends(get_db),
):
    """Получить последние N юнитов"""
    units = db.query(Unit).order_by(desc(Unit.property_id)).limit(limit).all()
    
    result = []
    for unit in units:
        unit_data = unit_to_dict(unit)
        
        if include_transactions and unit.area_id and unit.building_number:
            # Ищем похожие транзакции
            similar_transactions = db.query(Transaction).filter(
                and_(
                    Transaction.area_id == unit.area_id,
                    or_(
                        Transaction.building_name_en.ilike(f"%{unit.building_number}%"),
                        and_(
                            Transaction.rooms_en.isnot(None),
                            Transaction.rooms_en == unit.rooms_en
                        )
                    )
                )
            ).order_by(desc(Transaction.instance_date)).limit(5).all()
            
            unit_data["recent_transactions"] = [
                {
                    "transaction_id": t.transaction_id,
                    "instance_date": t.instance_date.isoformat() if t.instance_date else None,
                    "trans_value": float(t.trans_value) if t.trans_value else None,
                    "meter_sale_price": float(t.meter_sale_price) if t.meter_sale_price else None,
                    "trans_group_en": t.trans_group_en
                }
                for t in similar_transactions
            ]
        
        result.append(unit_data)
    
    return {"total": len(result), "units": result}


@router.get("/{property_id}")
def get_unit_by_id(
    property_id: int,
    include_details: bool = Query(True, description="Включить подробную информацию"),
    include_transactions: bool = Query(False, description="Включить историю транзакций"),
    include_valuation: bool = Query(False, description="Включить данные оценки"),
    include_project: bool = Query(False, description="Включить информацию о проекте"),
    db: Session = Depends(get_db),
):
    """Получить юнит по ID с дополнительной информацией"""
    unit = db.query(Unit).filter(Unit.property_id == property_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Юнит не найден")
    
    result = unit_to_dict(unit)
    
    # Дополнительная информация о проекте
    if include_project and unit.project_id:
        project = db.query(Project).filter(Project.project_id == unit.project_id).first()
        if project:
            result["project_details"] = {
                "project_name": project.project_name,
                "developer_name": project.developer_name,
                "master_developer_name": project.master_developer_name,
                "project_status": project.project_status,
                "percent_completed": float(project.percent_completed) if project.percent_completed else None,
                "completion_date": project.completion_date.isoformat() if project.completion_date else None,
            }
    
    # История транзакций для этого юнита/здания
    if include_transactions:
        transactions = []
        
        # Поиск транзакций по различным критериям
        if unit.building_number and unit.area_id:
            # 1. По зданию и району
            building_transactions = db.query(Transaction).filter(
                and_(
                    Transaction.area_id == unit.area_id,
                    Transaction.building_name_en.ilike(f"%{unit.building_number}%")
                )
            ).order_by(desc(Transaction.instance_date)).limit(20).all()
            
            for t in building_transactions:
                transactions.append({
                    "transaction_id": t.transaction_id,
                    "instance_date": t.instance_date.isoformat() if t.instance_date else None,
                    "trans_value": float(t.trans_value) if t.trans_value else None,
                    "meter_sale_price": float(t.meter_sale_price) if t.meter_sale_price else None,
                    "trans_group_en": t.trans_group_en,
                    "property_type_en": t.property_type_en,
                    "match_type": "building_and_area"
                })
        
        if unit.project_id:
            # 2. По проекту
            project_transactions = db.query(Transaction).filter(
                Transaction.project_number == unit.project_id
            ).order_by(desc(Transaction.instance_date)).limit(10).all()
            
            for t in project_transactions:
                if t.transaction_id not in [tr["transaction_id"] for tr in transactions]:
                    transactions.append({
                        "transaction_id": t.transaction_id,
                        "instance_date": t.instance_date.isoformat() if t.instance_date else None,
                        "trans_value": float(t.trans_value) if t.trans_value else None,
                        "meter_sale_price": float(t.meter_sale_price) if t.meter_sale_price else None,
                        "trans_group_en": t.trans_group_en,
                        "property_type_en": t.property_type_en,
                        "match_type": "project"
                    })
        
        if unit.actual_area and unit.rooms:
            # 3. По площади и количеству комнат (примерные совпадения)
            area_transactions = db.query(Transaction).filter(
                and_(
                    Transaction.actual_area_sqm.between(
                        float(unit.actual_area) * 0.8, 
                        float(unit.actual_area) * 1.2
                    ) if unit.actual_area else True,
                    Transaction.rooms_en == unit.rooms_en if unit.rooms_en else True
                )
            ).order_by(desc(Transaction.instance_date)).limit(5).all()
            
            for t in area_transactions:
                if t.transaction_id not in [tr["transaction_id"] for tr in transactions]:
                    transactions.append({
                        "transaction_id": t.transaction_id,
                        "instance_date": t.instance_date.isoformat() if t.instance_date else None,
                        "trans_value": float(t.trans_value) if t.trans_value else None,
                        "meter_sale_price": float(t.meter_sale_price) if t.meter_sale_price else None,
                        "trans_group_en": t.trans_group_en,
                        "property_type_en": t.property_type_en,
                        "match_type": "similar_properties"
                    })
        
        # Сортируем по дате
        transactions.sort(key=lambda x: x["instance_date"] or "", reverse=True)
        result["transaction_history"] = transactions[:30]  # Ограничиваем 30 записями
    
    # Данные оценки
    if include_valuation and unit.area_id and unit.actual_area:
        # Ищем оценки для похожих объектов в том же районе
        valuations = db.query(Valuation).filter(
            and_(
                Valuation.area_id == unit.area_id,
                Valuation.property_type_en == unit.property_type_en,
                Valuation.actual_area.between(
                    float(unit.actual_area) * 0.7,
                    float(unit.actual_area) * 1.3
                ) if unit.actual_area else True
            )
        ).order_by(desc(Valuation.instance_date)).limit(5).all()
        
        result["valuation_comparables"] = [
            {
                "procedure_number": v.procedure_number,
                "instance_date": v.instance_date.isoformat() if v.instance_date else None,
                "property_total_value": float(v.property_total_value) if v.property_total_value else None,
                "actual_worth": float(v.actual_worth) if v.actual_worth else None,
                "actual_area": float(v.actual_area) if v.actual_area else None,
                "price_per_sqm": float(v.property_total_value / v.actual_area) 
                if v.property_total_value and v.actual_area else None
            }
            for v in valuations
        ]
    
    # Расчет примерной стоимости на основе сравнимых продаж
    if include_details and result.get("transaction_history"):
        sale_transactions = [t for t in result["transaction_history"] 
                           if t.get("trans_group_en") == "Sales" and t.get("meter_sale_price")]
        
        if sale_transactions:
            avg_price_per_sqm = sum(t["meter_sale_price"] for t in sale_transactions) / len(sale_transactions)
            if unit.actual_area:
                result["estimated_value"] = {
                    "price_per_sqm": avg_price_per_sqm,
                    "total_value": avg_price_per_sqm * float(unit.actual_area),
                    "based_on_transactions": len(sale_transactions),
                    "confidence": "medium" if len(sale_transactions) >= 3 else "low"
                }
    
    return result


@router.get("/by-project/{project_id}")
def get_units_by_project(
    project_id: int,
    building_number: Optional[str] = Query(None, description="Фильтр по номеру здания в проекте"),
    property_type: Optional[str] = Query(None, description="Тип недвижимости (apartment, office, shop и т.д.)"),
    min_area: Optional[float] = Query(None, ge=0, description="Минимальная площадь (кв.м)"),
    max_area: Optional[float] = Query(None, ge=0, description="Максимальная площадь (кв.м)"),
    min_rooms: Optional[int] = Query(None, ge=0, description="Минимальное количество комнат"),
    max_rooms: Optional[int] = Query(None, ge=0, description="Максимальное количество комнат"),
    has_parking: Optional[bool] = Query(None, description="Наличие парковки"),
    is_freehold: Optional[bool] = Query(None, description="Freehold собственность"),
    floor: Optional[str] = Query(None, description="Номер этажа или диапазон (например: '5' или '1-10')"),
    unit_number: Optional[str] = Query(None, description="Номер юнита"),
    include_statistics: bool = Query(True, description="Включить статистику по проекту"),
    include_project_info: bool = Query(True, description="Включить информацию о проекте"),
    include_transactions: bool = Query(False, description="Включить последние транзакции по проекту"),
    sort_by: str = Query("unit_number", description="Сортировка: unit_number, actual_area, rooms, floor, building_number"),
    sort_order: str = Query("asc", description="Порядок сортировки: asc, desc"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(50, ge=1, le=200, description="Количество записей на странице"),
    db: Session = Depends(get_db),
):
    """Получить все юниты в проекте с расширенной фильтрацией"""
    
    # Сначала проверяем существование проекта
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    # Начинаем с базового запроса по project_id
    query = db.query(Unit).filter(Unit.project_id == project_id)
    
    # Дополнительные фильтры
    if building_number:
        query = query.filter(Unit.building_number.ilike(f"%{building_number}%"))
    
    if property_type:
        query = query.filter(
            or_(
                Unit.property_type_en.ilike(f"%{property_type}%"),
                Unit.property_sub_type_en.ilike(f"%{property_type}%"),
                Unit.property_type_ar.ilike(f"%{property_type}%"),
                Unit.property_sub_type_ar.ilike(f"%{property_type}%")
            )
        )
    
    if min_area is not None:
        query = query.filter(Unit.actual_area >= Decimal(str(min_area)))
    if max_area is not None:
        query = query.filter(Unit.actual_area <= Decimal(str(max_area)))
    
    if min_rooms is not None:
        query = query.filter(Unit.rooms >= min_rooms)
    if max_rooms is not None:
        query = query.filter(Unit.rooms <= max_rooms)
    
    if has_parking is not None:
        if has_parking:
            query = query.filter(
                and_(
                    Unit.unit_parking_number.isnot(None),
                    Unit.unit_parking_number != '',
                    Unit.unit_parking_number != '0'
                )
            )
        else:
            query = query.filter(
                or_(
                    Unit.unit_parking_number.is_(None),
                    Unit.unit_parking_number == '',
                    Unit.unit_parking_number == '0'
                )
            )
    
    if is_freehold is not None:
        query = query.filter(Unit.is_free_hold == (1 if is_freehold else 0))
    
    if floor:
        if '-' in floor:
            try:
                floor_start, floor_end = map(str.strip, floor.split('-'))
                query = query.filter(
                    and_(
                        Unit.floor >= floor_start,
                        Unit.floor <= floor_end
                    )
                )
            except:
                pass
        else:
            query = query.filter(Unit.floor == floor)
    
    if unit_number:
        query = query.filter(Unit.unit_number.ilike(f"%{unit_number}%"))
    
    # Подсчет общего количества
    total_count = query.count()
    
    # Сортировка
    sort_column = {
        "unit_number": Unit.unit_number,
        "actual_area": Unit.actual_area,
        "rooms": Unit.rooms,
        "floor": Unit.floor,
        "building_number": Unit.building_number,
        "property_id": Unit.property_id
    }.get(sort_by, Unit.unit_number)
    
    if sort_order.lower() == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(sort_column)
    
    # Пагинация
    offset = (page - 1) * limit
    units = query.offset(offset).limit(limit).all()
    
    # Основной результат
    result = {
        "project_info": {
            "project_id": project_id,
            "project_name": project.project_name,
            "developer_name": project.developer_name,
            "total_units_in_project": total_count,
            "units_on_page": len(units),
            "pagination": {
                "page": page,
                "limit": limit,
                "total_pages": (total_count + limit - 1) // limit if limit > 0 else 0,
                "has_previous": page > 1,
                "has_next": page * limit < total_count
            }
        },
        "units": [unit_to_dict(u) for u in units]
    }
    
    # Информация о проекте
    if include_project_info:
        result["project_info"].update({
            "developer_id": project.developer_id,
            "master_developer_name": project.master_developer_name,
            "project_status": project.project_status,
            "percent_completed": float(project.percent_completed) if project.percent_completed else None,
            "completion_date": project.completion_date.isoformat() if project.completion_date else None,
            "project_start_date": project.project_start_date.isoformat() if project.project_start_date else None,
            "area_name_en": project.area_name_en,
            "area_name_ar": project.area_name_ar
        })
    
    # Статистика по проекту
    if include_statistics and units:
        # Базовые статистики
        type_stats = {}
        building_stats = {}
        room_stats = {}
        area_stats = []
        floor_stats = {}
        parking_stats = {"with_parking": 0, "without_parking": 0}
        
        for unit in units:
            # Статистика по типам
            unit_type = unit.property_sub_type_en or unit.property_type_en or "Unknown"
            type_stats[unit_type] = type_stats.get(unit_type, 0) + 1
            
            # Статистика по зданиям
            building_num = unit.building_number or "Unknown"
            building_stats[building_num] = building_stats.get(building_num, 0) + 1
            
            # Статистика по комнатам
            rooms = unit.rooms if unit.rooms is not None else 0
            room_stats[str(rooms)] = room_stats.get(str(rooms), 0) + 1
            
            # Статистика по площади
            if unit.actual_area:
                area_stats.append(float(unit.actual_area))
            
            # Статистика по этажам
            floor_level = unit.floor or "Unknown"
            floor_stats[floor_level] = floor_stats.get(floor_level, 0) + 1
            
            # Статистика по парковке
            if unit.unit_parking_number and unit.unit_parking_number not in ['', '0']:
                parking_stats["with_parking"] += 1
            else:
                parking_stats["without_parking"] += 1
        
        result["project_info"]["statistics"] = {
            "unit_types_distribution": type_stats,
            "buildings_distribution": building_stats,
            "rooms_distribution": room_stats,
            "floors_distribution": floor_stats,
            "parking_distribution": parking_stats,
            "area_summary": {
                "total_area": sum(area_stats) if area_stats else 0,
                "average_area": sum(area_stats) / len(area_stats) if area_stats else 0,
                "minimum_area": min(area_stats) if area_stats else 0,
                "maximum_area": max(area_stats) if area_stats else 0,
                "median_area": sorted(area_stats)[len(area_stats)//2] if area_stats else 0
            },
            "completion_analysis": {
                "freehold_units": sum(1 for u in units if u.is_free_hold == 1),
                "leasehold_units": sum(1 for u in units if u.is_lease_hold == 1),
                "registered_units": sum(1 for u in units if u.is_registered == 1)
            }
        }
    
    # Информация о транзакциях по проекту
    if include_transactions:
        # Получаем транзакции связанные с этим проектом
        transactions = db.query(Transaction).filter(
            Transaction.project_number == project_id
        ).order_by(desc(Transaction.instance_date)).limit(20).all()
        
        result["project_transactions"] = {
            "total_transactions": len(transactions),
            "recent_transactions": [
                {
                    "transaction_id": t.transaction_id,
                    "instance_date": t.instance_date.isoformat() if t.instance_date else None,
                    "trans_value": float(t.trans_value) if t.trans_value else None,
                    "meter_sale_price": float(t.meter_sale_price) if t.meter_sale_price else None,
                    "trans_group_en": t.trans_group_en,
                    "property_type_en": t.property_type_en,
                    "area_sqm": float(t.actual_area_sqm) if t.actual_area_sqm else None
                }
                for t in transactions
            ],
            "price_analysis": {
                "avg_price_per_sqm": (
                    sum(float(t.meter_sale_price) for t in transactions if t.meter_sale_price) / 
                    len([t for t in transactions if t.meter_sale_price])
                ) if any(t.meter_sale_price for t in transactions) else None,
                "total_transaction_value": sum(float(t.trans_value) for t in transactions if t.trans_value),
                "transaction_types": {
                    "sales": sum(1 for t in transactions if t.trans_group_en == "Sales"),
                    "mortgages": sum(1 for t in transactions if t.trans_group_en == "Mortgages"),
                    "gifts": sum(1 for t in transactions if t.trans_group_en == "Gifts")
                }
            }
        }
    
    return result

@router.get("/search")
def search_units(
    area_id: Optional[int] = Query(None, description="ID района"),
    min_area: Optional[float] = Query(None, ge=0, description="Минимальная площадь"),
    max_area: Optional[float] = Query(None, ge=0, description="Максимальная площадь"),
    min_rooms: Optional[int] = Query(None, ge=0, description="Минимальное количество комнат"),
    max_rooms: Optional[int] = Query(None, ge=0, description="Максимальное количество комнат"),
    property_type: Optional[str] = Query(None, description="Тип недвижимости"),
    project_id: Optional[int] = Query(None, description="ID проекта"),
    has_parking: Optional[bool] = Query(None, description="Наличие парковки"),
    is_freehold: Optional[bool] = Query(None, description="Freehold собственность"),
    limit: int = Query(50, ge=1, le=500, description="Лимит результатов"),
    db: Session = Depends(get_db),
):
    """Расширенный поиск юнитов"""
    query = db.query(Unit)
    
    # Применяем фильтры
    if area_id:
        query = query.filter(Unit.area_id == area_id)
    
    if min_area is not None:
        query = query.filter(Unit.actual_area >= Decimal(str(min_area)))
    
    if max_area is not None:
        query = query.filter(Unit.actual_area <= Decimal(str(max_area)))
    
    if min_rooms is not None:
        query = query.filter(Unit.rooms >= min_rooms)
    
    if max_rooms is not None:
        query = query.filter(Unit.rooms <= max_rooms)
    
    if property_type:
        query = query.filter(
            or_(
                Unit.property_type_en == property_type,
                Unit.property_sub_type_en == property_type
            )
        )
    
    if project_id:
        query = query.filter(Unit.project_id == project_id)
    
    if has_parking is not None:
        if has_parking:
            query = query.filter(
                and_(
                    Unit.unit_parking_number.isnot(None),
                    Unit.unit_parking_number != '',
                    Unit.unit_parking_number != '0'
                )
            )
        else:
            query = query.filter(
                or_(
                    Unit.unit_parking_number.is_(None),
                    Unit.unit_parking_number == '',
                    Unit.unit_parking_number == '0'
                )
            )
    
    if is_freehold is not None:
        query = query.filter(Unit.is_free_hold == (1 if is_freehold else 0))
    
    units = query.order_by(desc(Unit.property_id)).limit(limit).all()
    
    return {
        "total_found": len(units),
        "filters_applied": {
            "area_id": area_id,
            "min_area": min_area,
            "max_area": max_area,
            "min_rooms": min_rooms,
            "max_rooms": max_rooms,
            "property_type": property_type,
            "project_id": project_id,
            "has_parking": has_parking,
            "is_freehold": is_freehold
        },
        "units": [unit_to_dict(u) for u in units]
    }


@router.get("/price-estimate/{property_id}")
def get_price_estimate(
    property_id: int,
    comparable_range: float = Query(0.2, ge=0.05, le=0.5, description="Диапазон сравнения (±20% по умолчанию)"),
    months_back: int = Query(12, ge=1, le=60, description="Период анализа в месяцах"),
    db: Session = Depends(get_db),
):
    """Получить оценку стоимости юнита на основе сравнимых продаж"""
    unit = db.query(Unit).filter(Unit.property_id == property_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Юнит не найден")
    
    if not unit.actual_area:
        raise HTTPException(status_code=400, detail="Не указана площадь юнита")
    
    # Определяем параметры для поиска сравнимых объектов
    unit_area = float(unit.actual_area)
    min_area = unit_area * (1 - comparable_range)
    max_area = unit_area * (1 + comparable_range)
    
    # Дата начала периода
    end_date = date.today()
    start_date = end_date - timedelta(days=months_back * 30)
    
    # Ищем сравнимые транзакции
    comparable_transactions = db.query(Transaction).filter(
        and_(
            Transaction.instance_date >= start_date,
            Transaction.instance_date <= end_date,
            Transaction.trans_group_en == 'Sales',
            Transaction.meter_sale_price.isnot(None),
            Transaction.actual_area_sqm.isnot(None),
            Transaction.actual_area_sqm.between(min_area, max_area),
            Transaction.area_id == unit.area_id,
            Transaction.property_type_en == unit.property_type_en
        )
    ).order_by(desc(Transaction.instance_date)).all()
    
    if not comparable_transactions:
        # Расширяем поиск
        comparable_transactions = db.query(Transaction).filter(
            and_(
                Transaction.instance_date >= start_date,
                Transaction.instance_date <= end_date,
                Transaction.trans_group_en == 'Sales',
                Transaction.meter_sale_price.isnot(None),
                Transaction.actual_area_sqm.isnot(None),
                Transaction.actual_area_sqm.between(min_area * 0.8, max_area * 1.2),
                Transaction.area_id == unit.area_id
            )
        ).order_by(desc(Transaction.instance_date)).limit(10).all()
    
    # Анализируем данные
    if comparable_transactions:
        prices_per_sqm = [float(t.meter_sale_price) for t in comparable_transactions if t.meter_sale_price]
        transaction_dates = [t.instance_date for t in comparable_transactions if t.instance_date]
        transaction_values = [float(t.trans_value) for t in comparable_transactions if t.trans_value]
        
        avg_price_per_sqm = sum(prices_per_sqm) / len(prices_per_sqm)
        estimated_value = avg_price_per_sqm * unit_area
        
        # Рассчитываем тренд
        recent_transactions = [t for t in comparable_transactions 
                             if t.instance_date and (end_date - t.instance_date).days <= 90]
        older_transactions = [t for t in comparable_transactions 
                            if t.instance_date and (end_date - t.instance_date).days > 90]
        
        recent_avg = sum(float(t.meter_sale_price) for t in recent_transactions) / len(recent_transactions) \
            if recent_transactions else None
        older_avg = sum(float(t.meter_sale_price) for t in older_transactions) / len(older_transactions) \
            if older_transactions else None
        
        trend = "stable"
        if recent_avg and older_avg:
            if recent_avg > older_avg * 1.05:
                trend = "increasing"
            elif recent_avg < older_avg * 0.95:
                trend = "decreasing"
        
        return {
            "unit_info": {
                "property_id": property_id,
                "area": unit_area,
                "area_id": unit.area_id,
                "property_type": unit.property_type_en
            },
            "analysis_period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "months": months_back
            },
            "comparable_data": {
                "transactions_found": len(comparable_transactions),
                "avg_price_per_sqm": avg_price_per_sqm,
                "min_price_per_sqm": min(prices_per_sqm) if prices_per_sqm else None,
                "max_price_per_sqm": max(prices_per_sqm) if prices_per_sqm else None,
                "price_volatility": (max(prices_per_sqm) - min(prices_per_sqm)) / avg_price_per_sqm 
                if prices_per_sqm and len(prices_per_sqm) > 1 else None
            },
            "price_estimate": {
                "estimated_value": estimated_value,
                "price_per_sqm": avg_price_per_sqm,
                "confidence": "high" if len(comparable_transactions) >= 5 else 
                            "medium" if len(comparable_transactions) >= 3 else "low",
                "trend": trend,
                "recommended_price_range": {
                    "low": estimated_value * 0.9,
                    "high": estimated_value * 1.1
                }
            },
            "recent_comparables": [
                {
                    "transaction_id": t.transaction_id,
                    "date": t.instance_date.isoformat() if t.instance_date else None,
                    "price_per_sqm": float(t.meter_sale_price) if t.meter_sale_price else None,
                    "total_value": float(t.trans_value) if t.trans_value else None,
                    "area": float(t.actual_area_sqm) if t.actual_area_sqm else None
                }
                for t in comparable_transactions[:5]
            ]
        }
    
    return {
        "unit_info": {
            "property_id": property_id,
            "area": unit_area,
            "area_id": unit.area_id,
            "property_type": unit.property_type_en
        },
        "message": "Недостаточно данных для оценки",
        "suggestions": [
            "Расширьте диапазон поиска",
            "Увеличьте период анализа",
            "Используйте данные оценки (valuation) вместо транзакций"
        ]
    }


@router.get("/{property_id}/transaction-history")
def get_unit_transaction_history(
    property_id: int,
    include_related: bool = Query(True, description="Включить связанные транзакции (по тому же зданию)"),
    include_similar: bool = Query(False, description="Включить транзакции похожих юнитов"),
    min_score: int = Query(3, ge=0, le=10, description="Минимальный балл соответствия (0-10)"),
    limit: int = Query(20, ge=1, le=100, description="Лимит результатов"),
    db: Session = Depends(get_db),
):
    """Получить историю транзакций для конкретного юнита"""
    unit = db.query(Unit).filter(Unit.property_id == property_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Юнит не найден")
    
    transactions = []
    direct_matches = []
    building_transactions = []
    similar_transactions = []
    
    # Получаем базовую информацию о юните
    unit_info = {
        "property_id": property_id,
        "building_number": unit.building_number,
        "unit_number": unit.unit_number,
        "area": float(unit.actual_area) if unit.actual_area else None,
        "rooms": unit.rooms,
        "property_type_en": unit.property_type_en,
        "property_sub_type_en": unit.property_sub_type_en,
        "project_id": unit.project_id,
        "area_id": unit.area_id,
    }
    
    # 1. Попробуем найти прямые соответствия по различным критериям
    if unit.building_number and unit.area_id:
        # Ищем транзакции в том же здании и районе
        building_query = db.query(Transaction).filter(
            and_(
                Transaction.area_id == unit.area_id,
                or_(
                    Transaction.building_name_en.ilike(f"%{unit.building_number}%"),
                    Transaction.building_name_ar.ilike(f"%{unit.building_number}%")
                )
            )
        )
        
        # Фильтруем по этажу (если указан этаж юнита)
        if unit.floor and unit.floor.isdigit():
            building_query = building_query.filter(
                Transaction.building_name_en.ilike(f"%{unit.floor}%") |
                Transaction.building_name_ar.ilike(f"%{unit.floor}%")
            )
        
        building_tx = building_query.order_by(desc(Transaction.instance_date)).limit(50).all()
        
        for tx in building_tx:
            score = 0
            match_reasons = []
            
            # Проверяем номер юнита в названии здания
            if unit.unit_number:
                if unit.unit_number in (tx.building_name_en or ""):
                    score += 4
                    match_reasons.append("unit_number_in_building_name")
                elif unit.unit_number in (tx.building_name_ar or ""):
                    score += 4
                    match_reasons.append("unit_number_in_building_name_ar")
            
            # Проверяем соответствие по количеству комнат
            if unit.rooms and tx.rooms_en:
                # Извлекаем число из строки "2 B/R"
                import re
                room_match = re.search(r'(\d+)', tx.rooms_en)
                if room_match:
                    tx_rooms = int(room_match.group(1))
                    if tx_rooms == unit.rooms:
                        score += 3
                        match_reasons.append("exact_room_match")
                    elif abs(tx_rooms - unit.rooms) <= 1:
                        score += 2
                        match_reasons.append("similar_room_match")
            
            # Проверяем соответствие по площади
            if unit.actual_area and tx.actual_area_sqm:
                unit_area = float(unit.actual_area)
                tx_area = float(tx.actual_area_sqm)
                area_diff = abs(tx_area - unit_area)
                
                if area_diff < 5:  # Разница менее 5 кв.м
                    score += 3
                    match_reasons.append("exact_area_match")
                elif area_diff < 15:  # Разница менее 15 кв.м
                    score += 2
                    match_reasons.append("similar_area_match")
                elif area_diff < 30:  # Разница менее 30 кв.м
                    score += 1
                    match_reasons.append("approximate_area_match")
            
            # Проверяем тип недвижимости
            if unit.property_sub_type_en and tx.property_sub_type_en:
                if unit.property_sub_type_en == tx.property_sub_type_en:
                    score += 2
                    match_reasons.append("same_property_type")
            
            # Проверяем проект
            if unit.project_id and tx.project_number:
                if unit.project_id == tx.project_number:
                    score += 2
                    match_reasons.append("same_project")
            
            tx_dict = transaction_to_dict(tx)
            tx_dict.update({
                "match_score": score,
                "match_reasons": match_reasons,
                "match_type": "building_match"
            })
            
            if score >= min_score:
                direct_matches.append(tx_dict)
            elif include_related:
                building_transactions.append(tx_dict)
    
    # 2. Ищем транзакции похожих юнитов (если нужно)
    if include_similar and unit.area_id and unit.actual_area:
        # Ищем транзакции юнитов с похожей площадью в том же районе
        unit_area = float(unit.actual_area)
        similar_query = db.query(Transaction).filter(
            and_(
                Transaction.area_id == unit.area_id,
                Transaction.property_type_en == "Unit",  # Только юниты
                Transaction.actual_area_sqm.isnot(None),
                Transaction.actual_area_sqm.between(unit_area * 0.7, unit_area * 1.3),
                Transaction.property_sub_type_en == unit.property_sub_type_en
            )
        ).order_by(desc(Transaction.instance_date)).limit(20).all()
        
        for tx in similar_query:
            score = 0
            match_reasons = []
            
            # Балл за похожую площадь
            if tx.actual_area_sqm:
                area_diff = abs(float(tx.actual_area_sqm) - unit_area)
                if area_diff < 10:
                    score += 3
                    match_reasons.append("similar_area")
            
            # Балл за тот же тип недвижимости
            if tx.property_sub_type_en == unit.property_sub_type_en:
                score += 2
                match_reasons.append("same_property_subtype")
            
            # Балл за тот же район
            score += 1
            match_reasons.append("same_area")
            
            tx_dict = transaction_to_dict(tx)
            tx_dict.update({
                "match_score": score,
                "match_reasons": match_reasons,
                "match_type": "similar_unit_match"
            })
            
            if score >= min_score:
                similar_transactions.append(tx_dict)
    
    # Собираем все транзакции
    transactions = direct_matches + building_transactions + similar_transactions
    
    # Убираем дубликаты (по transaction_id)
    seen = set()
    unique_transactions = []
    for tx in transactions:
        if tx["transaction_id"] not in seen:
            seen.add(tx["transaction_id"])
            unique_transactions.append(tx)
    
    # Сортируем по дате и баллу соответствия
    unique_transactions.sort(
        key=lambda x: (
            x.get("instance_date") or "", 
            x.get("match_score", 0)
        ), 
        reverse=True
    )
    
    # Ограничиваем результат
    unique_transactions = unique_transactions[:limit]
    
    return {
        "unit_info": unit_info,
        "search_parameters": {
            "include_related": include_related,
            "include_similar": include_similar,
            "min_match_score": min_score,
            "limit": limit
        },
        "match_statistics": {
            "direct_matches": len(direct_matches),
            "building_transactions": len(building_transactions),
            "similar_transactions": len(similar_transactions),
            "unique_transactions": len(unique_transactions)
        },
        "transactions": unique_transactions
    }


@router.get("/market-analysis/{area_id}")
def get_market_analysis_by_area(
    area_id: int,
    property_type: Optional[str] = Query(None, description="Тип недвижимости"),
    db: Session = Depends(get_db),
):
    """Анализ рынка для юнитов в районе"""
    # Статистика по юнитам в районе
    units_query = db.query(Unit).filter(Unit.area_id == area_id)
    if property_type:
        units_query = units_query.filter(Unit.property_type_en == property_type)
    
    units = units_query.all()
    
    # Статистика по транзакциям в районе
    transactions_query = db.query(Transaction).filter(
        and_(
            Transaction.area_id == area_id,
            Transaction.trans_group_en == 'Sales',
            Transaction.meter_sale_price.isnot(None)
        )
    )
    
    if property_type:
        transactions_query = transactions_query.filter(Transaction.property_type_en == property_type)
    
    transactions = transactions_query.order_by(desc(Transaction.instance_date)).limit(100).all()
    
    # Анализ данных
    unit_types = {}
    area_stats = []
    price_stats = []
    
    for unit in units:
        unit_type = unit.property_sub_type_en or unit.property_type_en
        if unit_type:
            unit_types[unit_type] = unit_types.get(unit_type, 0) + 1
        
        if unit.actual_area:
            area_stats.append(float(unit.actual_area))
    
    for tx in transactions:
        if tx.meter_sale_price:
            price_stats.append(float(tx.meter_sale_price))
    
    # Рассчитываем средние значения
    avg_area = sum(area_stats) / len(area_stats) if area_stats else None
    avg_price = sum(price_stats) / len(price_stats) if price_stats else None
    
    return {
        "area_id": area_id,
        "property_type": property_type,
        "units_analysis": {
            "total_units": len(units),
            "unit_type_distribution": unit_types,
            "area_statistics": {
                "avg": avg_area,
                "min": min(area_stats) if area_stats else None,
                "max": max(area_stats) if area_stats else None,
                "median": sorted(area_stats)[len(area_stats)//2] if area_stats else None
            }
        },
        "transactions_analysis": {
            "total_transactions_analyzed": len(transactions),
            "price_statistics": {
                "avg_price_per_sqm": avg_price,
                "min_price": min(price_stats) if price_stats else None,
                "max_price": max(price_stats) if price_stats else None,
                "price_range": max(price_stats) - min(price_stats) if price_stats else None
            },
            "recent_activity": len([t for t in transactions 
                                  if t.instance_date and (date.today() - t.instance_date).days <= 90])
        },
        "market_indicators": {
            "supply": len(units),
            "demand": len(transactions),
            "avg_days_on_market": None,  # Нужны дополнительные данные
            "price_trend": "stable"  # Нужен анализ по времени
        }
    }