from datetime import date, datetime, timedelta
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func, distinct

from app.database.connection import get_db
from app.database.models import Project, LkpArea

router = APIRouter()

# Порядок полей как в таблице PROJECTS
PROJECT_FIELDS = [
    "project_id",
    "project_number",
    "project_name",
    "developer_id",
    "developer_number",
    "developer_name",
    "master_developer_id",
    "master_developer_number",
    "master_developer_name",
    "project_start_date",
    "project_end_date",
    "project_type_id",
    "project_type_ar",
    "project_classification_id",
    "project_classification_ar",
    "escrow_agent_id",
    "escrow_agent_name",
    "project_status",
    "project_status_ar",
    "percent_completed",
    "completion_date",
    "cancellation_date",
    "project_description_ar",
    "project_description_en",
    "property_id",
    "area_id",
    "area_name_ar",
    "area_name_en",
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


def project_to_dict(p: Project) -> dict:
    """Преобразовать Project в словарь"""
    return {key: _serialize_value(getattr(p, key, None)) for key in PROJECT_FIELDS if hasattr(p, key)}


@router.get("/latest")
def get_latest_projects(
    limit: int = Query(10, ge=1, le=1000, description="Количество записей"),
    db: Session = Depends(get_db),
):
    """Получить последние N проектов"""
    projects = db.query(Project).order_by(desc(Project.project_id)).limit(limit).all()
    return {
        "total": len(projects),
        "projects": [project_to_dict(p) for p in projects],
    }


@router.get("/upcoming-completions")
def get_upcoming_completion_projects(
    months_ahead: int = Query(6, ge=1, le=24, description="Количество месяцев вперед"),
    area_id: int = Query(None, description="Фильтр по району"),
    developer_id: int = Query(None, description="Фильтр по застройщику"),
    status: str = Query(None, description="Фильтр по статусу проекта"),
    db: Session = Depends(get_db),
):
    """
    Получить проекты с ожидаемой датой завершения в указанном диапазоне.
    Учитывает поле completion_date, если оно заполнено, иначе project_end_date.
    """
    today = date.today()
    end_date = today + timedelta(days=months_ahead * 30)
    
    # Создаем условие для даты завершения (используем completion_date или project_end_date)
    from sqlalchemy import case
    
    # Используем completion_date, если есть, иначе project_end_date
    completion_date_expr = case(
        (Project.completion_date.isnot(None), Project.completion_date),
        else_=Project.project_end_date
    )
    
    query = db.query(Project).add_columns(completion_date_expr.label('effective_completion_date'))
    
    # Фильтр по дате завершения
    query = query.filter(
        and_(
            completion_date_expr >= today,
            completion_date_expr <= end_date
        )
    )
    
    # Дополнительные фильтры
    if area_id:
        query = query.filter(Project.area_id == area_id)
    
    if developer_id:
        query = query.filter(Project.developer_id == developer_id)
    
    if status:
        query = query.filter(Project.project_status == status)
    
    # Выполняем запрос
    results = query.order_by(completion_date_expr).all()
    
    projects = []
    for project, effective_date in results:
        project_dict = project_to_dict(project)
        project_dict['effective_completion_date'] = effective_date.isoformat() if effective_date else None
        projects.append(project_dict)
    
    return {
        "total": len(projects),
        "from_date": today.isoformat(),
        "to_date": end_date.isoformat(),
        "months_ahead": months_ahead,
        "filters": {
            "area_id": area_id,
            "developer_id": developer_id,
            "status": status
        },
        "projects": projects
    }


@router.get("/status-summary")
def get_projects_status_summary(
    db: Session = Depends(get_db),
):
    """Получить сводку по статусам проектов"""
    # Группировка по статусу
    status_summary = db.query(
        Project.project_status,
        func.count(Project.project_id).label('count')
    ).group_by(Project.project_status).all()
    
    # Общее количество проектов
    total_count = db.query(func.count(Project.project_id)).scalar()
    
    return {
        "total_projects": total_count,
        "status_summary": [
            {"status": status, "count": count}
            for status, count in status_summary if status
        ]
    }


@router.get("/by-developer/{developer_id}")
def get_projects_by_developer(
    developer_id: int,
    status: str = Query(None, description="Фильтр по статусу"),
    db: Session = Depends(get_db),
):
    """Получить все проекты указанного застройщика"""
    query = db.query(Project).filter(Project.developer_id == developer_id)
    
    if status:
        query = query.filter(Project.project_status == status)
    
    projects = query.order_by(Project.project_id).all()
    
    return {
        "developer_id": developer_id,
        "total": len(projects),
        "projects": [project_to_dict(p) for p in projects]
    }


@router.get("/by-area/{area_id}")
def get_projects_by_area(
    area_id: int,
    status: str = Query(None, description="Фильтр по статусу"),
    db: Session = Depends(get_db),
):
    """Получить все проекты в указанном районе"""
    query = db.query(Project).filter(Project.area_id == area_id)
    
    if status:
        query = query.filter(Project.project_status == status)
    
    projects = query.order_by(Project.project_id).all()
    
    return {
        "area_id": area_id,
        "total": len(projects),
        "projects": [project_to_dict(p) for p in projects]
    }


@router.get("/search")
def search_projects(
    q: str = Query(None, description="Поиск по названию проекта или застройщика"),
    status: str = Query(None, description="Фильтр по статусу"),
    min_completion: float = Query(None, ge=0, le=100, description="Минимальный процент завершения"),
    max_completion: float = Query(None, ge=0, le=100, description="Максимальный процент завершения"),
    limit: int = Query(50, ge=1, le=500, description="Лимит результатов"),
    db: Session = Depends(get_db),
):
    """Поиск проектов по различным критериям"""
    query = db.query(Project)
    
    # Поиск по тексту
    if q:
        search_pattern = f"%{q}%"
        query = query.filter(
            (Project.project_name.ilike(search_pattern)) |
            (Project.developer_name.ilike(search_pattern)) |
            (Project.master_developer_name.ilike(search_pattern))
        )
    
    # Фильтр по статусу
    if status:
        query = query.filter(Project.project_status == status)
    
    # Фильтр по проценту завершения
    if min_completion is not None:
        query = query.filter(Project.percent_completed >= Decimal(str(min_completion)))
    
    if max_completion is not None:
        query = query.filter(Project.percent_completed <= Decimal(str(max_completion)))
    
    projects = query.order_by(desc(Project.project_id)).limit(limit).all()
    
    return {
        "total_found": len(projects),
        "search_params": {
            "query": q,
            "status": status,
            "min_completion": min_completion,
            "max_completion": max_completion
        },
        "projects": [project_to_dict(p) for p in projects]
    }


@router.get("/areas/with-projects")
def get_areas_with_projects(
    db: Session = Depends(get_db),
):
    """Получить список районов с количеством проектов в каждом"""
    # Используем LkpArea для получения полного списка районов
    areas_with_counts = db.query(
        LkpArea.area_id,
        LkpArea.name_en,
        LkpArea.name_ar,
        func.count(Project.project_id).label('project_count')
    ).outerjoin(
        Project, LkpArea.area_id == Project.area_id
    ).group_by(
        LkpArea.area_id, LkpArea.name_en, LkpArea.name_ar
    ).order_by(
        LkpArea.name_en
    ).all()
    
    return {
        "total_areas": len(areas_with_counts),
        "areas": [
            {
                "area_id": area_id,
                "name_en": name_en,
                "name_ar": name_ar,
                "project_count": project_count
            }
            for area_id, name_en, name_ar, project_count in areas_with_counts
        ]
    }


@router.get("/developers/with-projects")
def get_developers_with_projects(
    limit: int = Query(20, ge=1, le=100, description="Лимит застройщиков"),
    db: Session = Depends(get_db),
):
    """Получить список застройщиков с количеством проектов"""
    developers = db.query(
        Project.developer_id,
        Project.developer_name,
        func.count(Project.project_id).label('project_count')
    ).filter(
        Project.developer_id.isnot(None)
    ).group_by(
        Project.developer_id, Project.developer_name
    ).order_by(
        desc('project_count')
    ).limit(limit).all()
    
    return {
        "total": len(developers),
        "developers": [
            {
                "developer_id": developer_id,
                "developer_name": developer_name,
                "project_count": project_count
            }
            for developer_id, developer_name, project_count in developers
        ]
    }


@router.get("/{project_id}")
def get_project_by_id(
    project_id: int,
    db: Session = Depends(get_db),
):
    """Получить проект по ID"""
    project = db.query(Project).filter(Project.project_id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return project_to_dict(project)


@router.get("/{project_id}/similar")
def get_similar_projects(
    project_id: int,
    limit: int = Query(5, ge=1, le=20, description="Количество похожих проектов"),
    db: Session = Depends(get_db),
):
    """Получить похожие проекты (по району и застройщику)"""
    # Сначала находим текущий проект
    current_project = db.query(Project).filter(Project.project_id == project_id).first()
    if not current_project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    # Ищем похожие проекты
    query = db.query(Project).filter(
        Project.project_id != project_id,
        Project.project_status == current_project.project_status
    )
    
    # По возможности фильтруем по району и застройщику
    if current_project.area_id:
        query = query.filter(Project.area_id == current_project.area_id)
    
    if current_project.developer_id:
        query = query.filter(Project.developer_id == current_project.developer_id)
    
    similar_projects = query.order_by(desc(Project.project_id)).limit(limit).all()
    
    return {
        "current_project_id": project_id,
        "similar_projects_found": len(similar_projects),
        "similar_projects": [project_to_dict(p) for p in similar_projects]
    }