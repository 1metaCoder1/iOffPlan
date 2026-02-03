from sqlalchemy import Column, BigInteger, Text, Date, Numeric, Integer, SmallInteger, String, TIMESTAMP, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LkpArea(Base):
    __tablename__ = "lkp_areas"

    area_id = Column(BigInteger, primary_key=True)
    name_en = Column(Text)
    name_ar = Column(Text)
    municipality_number = Column(String)


class LkpMarketType(Base):
    __tablename__ = "lkp_market_types"

    market_type_id = Column(BigInteger, primary_key=True)
    name_ar = Column(Text)
    name_en = Column(Text)


class LkpTransactionGroup(Base):
    __tablename__ = "lkp_transaction_groups"

    group_id = Column(BigInteger, primary_key=True)
    name_ar = Column(Text)
    name_en = Column(Text)


class LkpTransactionProcedure(Base):
    __tablename__ = "lkp_transaction_procedures"

    group_id = Column(BigInteger, primary_key=True)
    procedure_id = Column(BigInteger, primary_key=True)
    is_pre_registration = Column(SmallInteger)
    name_ar = Column(Text)
    name_en = Column(Text)


class Valuation(Base):
    __tablename__ = "valuation"

    # Первичные ключи (составной)
    procedure_id = Column(SmallInteger, primary_key=True)
    procedure_year = Column(Integer, primary_key=True)
    procedure_number = Column(BigInteger, primary_key=True)
    
    # Денежные значения с 2 знаками после запятой
    property_total_value = Column(Numeric(18, 2))
    actual_worth = Column(Numeric(18, 2))
    
    # Площади с 2 знаками после запятой
    actual_area = Column(Numeric(18, 2))
    procedure_area = Column(Numeric(18, 2))
    
    # Текстовые поля с ограничениями длины
    procedure_name_ar = Column(String(100))
    procedure_name_en = Column(String(100))
    
    area_id = Column(BigInteger)
    area_name_ar = Column(String(200))
    area_name_en = Column(String(200))
    
    instance_date = Column(Date)  # TIMESTAMP(6) преобразован в Date
    
    row_status_code = Column(String(100))
    
    property_type_id = Column(Integer)  # NUMBER(4) -> Integer
    property_type_ar = Column(String(50))
    property_type_en = Column(String(50))
    
    property_sub_type_id = Column(Integer)  # NUMBER(4) -> Integer
    property_sub_type_ar = Column(String(50))
    property_sub_type_en = Column(String(50))
    
    # Индексы для улучшения производительности
    __table_args__ = (
        Index('idx_valuation_area_id', 'area_id'),
        Index('idx_valuation_instance_date', 'instance_date'),
        Index('idx_valuation_property_type_id', 'property_type_id'),
        Index('idx_valuation_row_status_code', 'row_status_code'),
    )


class Unit(Base):
    __tablename__ = "units"

    # Все ID поля как NUMERIC для совместимости
    property_id = Column(Numeric(30, 0), primary_key=True)
    area_id = Column(Numeric(30, 0))
    zone_id = Column(Numeric(10, 0))
    area_name_ar = Column(Text)
    area_name_en = Column(Text)
    
    land_number = Column(String(100))
    land_sub_number = Column(Numeric(30, 0))
    building_number = Column(String(100))
    unit_number = Column(String(100))
    
    unit_balcony_area = Column(Numeric(10, 2))
    unit_parking_number = Column(Text)
    parking_allocation_type = Column(Numeric(30, 0))
    parking_allocation_type_ar = Column(String(100))
    parking_allocation_type_en = Column(String(100))
    
    common_area = Column(Numeric(20, 4))
    actual_common_area = Column(Numeric(30, 0))
    floor = Column(String(40))
    
    rooms = Column(Numeric(10, 0))
    rooms_ar = Column(String(60))
    rooms_en = Column(String(60))
    actual_area = Column(Numeric(18, 2))
    
    property_type_id = Column(Numeric(10, 0))
    property_type_ar = Column(String(50))
    property_type_en = Column(String(50))
    property_sub_type_id = Column(Numeric(10, 0))
    property_sub_type_ar = Column(String(50))
    property_sub_type_en = Column(String(50))
    
    parent_property_id = Column(Numeric(30, 0))
    grandparent_property_id = Column(Numeric(30, 0))
    creation_date = Column(Date)
    
    munc_zip_code = Column(String(3))
    munc_number = Column(String(10))
    parcel_id = Column(Numeric(30, 0))
    
    is_free_hold = Column(Numeric(1, 0))
    is_lease_hold = Column(Numeric(1, 0))
    is_registered = Column(Numeric(1, 0))
    
    pre_registration_number = Column(String(100))
    
    master_project_id = Column(Numeric(30, 0))
    master_project_en = Column(Text)
    master_project_ar = Column(Text)
    project_id = Column(Numeric(30, 0))
    project_name_ar = Column(String(200))
    project_name_en = Column(String(200))
    
    land_type_id = Column(Numeric(30, 0))
    land_type_ar = Column(String(50))
    land_type_en = Column(String(50))
    
    # Индексы для улучшения производительности
    __table_args__ = (
        Index('idx_units_area_id', 'area_id'),
        Index('idx_units_project_id', 'project_id'),
        Index('idx_units_parent_property_id', 'parent_property_id'),
        Index('idx_units_building_number', 'building_number'),
    )

class Building(Base):
    __tablename__ = "buildings"

    # ВСЕ числовые поля как NUMERIC
    property_id = Column(Numeric(30, 0), primary_key=True)  # Увеличена точность
    area_id = Column(Numeric(30, 0))
    zone_id = Column(Numeric(10, 0))
    area_name_ar = Column(Text)
    area_name_en = Column(Text)
    
    land_number = Column(String(100))
    land_sub_number = Column(Numeric(30, 0))
    building_number = Column(String(100))
    
    common_area = Column(Numeric(20, 4))
    actual_common_area = Column(Numeric(20, 4))
    built_up_area = Column(Numeric(10, 2))
    actual_area = Column(Numeric(18, 2))
    
    floors = Column(String(40))
    rooms = Column(Numeric(10, 0))
    rooms_ar = Column(String(60))
    rooms_en = Column(String(60))
    car_parks = Column(Numeric(10, 0))
    
    is_lease_hold = Column(Numeric(1, 0))
    is_registered = Column(Numeric(1, 0))
    is_free_hold = Column(Numeric(1, 0))
    
    pre_registration_number = Column(String(100))
    
    master_project_id = Column(Numeric(30, 0))
    master_project_en = Column(Text)
    master_project_ar = Column(Text)
    project_id = Column(Numeric(30, 0))
    project_name_ar = Column(Text)
    project_name_en = Column(Text)
    
    land_type_id = Column(Numeric(10, 0))
    land_type_ar = Column(Text)
    land_type_en = Column(Text)
    
    bld_levels = Column(Numeric(10, 0))
    shops = Column(Numeric(10, 0))
    flats = Column(Numeric(10, 0))
    offices = Column(Numeric(10, 0))
    swimming_pools = Column(Numeric(4, 0))
    elevators = Column(Numeric(4, 0))
    
    property_type_id = Column(Numeric(10, 0))
    property_type_ar = Column(Text)
    property_type_en = Column(Text)
    property_sub_type_id = Column(Numeric(10, 0))
    property_sub_type_ar = Column(Text)
    property_sub_type_en = Column(Text)
    
    parent_property_id = Column(Numeric(30, 0))
    creation_date = Column(Date)
    parcel_id = Column(Numeric(30, 0))
    
    __table_args__ = (
        Index('idx_buildings_area_id', 'area_id'),
        Index('idx_buildings_project_id', 'project_id'),
        Index('idx_buildings_property_type_id', 'property_type_id'),
    )


class Project(Base):
    __tablename__ = "projects"

    # Первичный ключ
    project_id = Column(Numeric(10, 0), primary_key=True)
    
    # Основная информация
    project_number = Column(Numeric(10, 0))
    project_name = Column(String(200))
    
    # Информация о разработчике
    developer_id = Column(Numeric(10, 0))
    developer_number = Column(Numeric(20, 0))
    developer_name = Column(String(200))
    
    # Информация о главном разработчике
    master_developer_id = Column(Numeric(10, 0))
    master_developer_number = Column(Numeric(20, 0))
    master_developer_name = Column(String(200))
    
    # Даты проекта
    project_start_date = Column(Date)
    project_end_date = Column(Date)
    
    # Тип проекта
    project_type_id = Column(Numeric(20, 0))
    project_type_ar = Column(String(100))
    
    # Классификация проекта
    project_classification_id = Column(Numeric(10, 0))
    project_classification_ar = Column(String(50))
    
    # Информация о гарантийном агенте
    escrow_agent_id = Column(Numeric(10, 0))
    escrow_agent_name = Column(String(200))
    
    # Статус проекта
    project_status = Column(String(200))
    project_status_ar = Column(String(100))
    
    # Процент завершения
    percent_completed = Column(Numeric(10, 3))
    
    # Дополнительные даты
    completion_date = Column(Date)
    cancellation_date = Column(Date)
    
    # Описание проекта
    project_description_ar = Column(String(2000))
    project_description_en = Column(String(2000))
    
    # Связанная собственность
    property_id = Column(Numeric(10, 0))
    
    # Район
    area_id = Column(Numeric(10, 0))
    area_name_ar = Column(String(200))
    area_name_en = Column(String(200))
    
    # ИНДУСЫ
    __table_args__ = (
        Index('idx_projects_area_id', 'area_id'),
        Index('idx_projects_developer_id', 'developer_id'),
        Index('idx_projects_master_developer_id', 'master_developer_id'),
        Index('idx_projects_project_status', 'project_status'),
        Index('idx_projects_project_start_date', 'project_start_date'),
    )


class Transaction(Base):
    __tablename__ = "transactions"

    # Первичный ключ - transaction_id как строка
    transaction_id = Column(String(100), primary_key=True)
    
    # Дата
    instance_date = Column(Date)
    
    # Транзакционные группы
    trans_group_id = Column(Numeric(3, 0))
    trans_group_en = Column(String(200))
    trans_group_ar = Column(String(200))
    
    # Процедура
    procedure_id = Column(Numeric(3, 0))
    procedure_name_en = Column(String(200))
    procedure_name_ar = Column(String(200))
    
    # Тип собственности
    property_type_id = Column(Numeric(4, 0))
    property_type_en = Column(String(50))
    property_type_ar = Column(String(50))
    
    # Подтип собственности
    property_sub_type_id = Column(Numeric(10, 0))
    property_sub_type_en = Column(String(100))
    property_sub_type_ar = Column(String(100))
    
    # Использование собственности
    property_usage_en = Column(String(100))
    property_usage_ar = Column(String(100))
    
    # Район
    area_id = Column(Numeric(10, 0))
    area_name_en = Column(String(200))
    area_name_ar = Column(String(200))
    
    # Финансовые значения
    trans_value = Column(Numeric(20, 2))
    meter_sale_price = Column(Numeric(18, 2))
    actual_worth = Column(Numeric(20, 2))
    rent_value = Column(Numeric(20, 2))
    meter_rent_price = Column(Numeric(20, 2))
    
    # Стороны сделки
    no_of_parties_role_1 = Column(Numeric(3, 0))
    party_type_role_1_en = Column(String(100))
    party_type_role_1_ar = Column(String(100))
    
    no_of_parties_role_2 = Column(Numeric(3, 0))
    party_type_role_2_en = Column(String(100))
    party_type_role_2_ar = Column(String(100))
    
    # Новая колонка из спецификации
    no_of_parties_role_3 = Column(Numeric(3, 0))
    
    # Проекты
    master_project_en = Column(String(200))
    master_project_ar = Column(String(200))
    project_number = Column(Numeric(30, 0))
    project_name_en = Column(String(200))
    project_name_ar = Column(String(200))
    
    # Комнаты
    rooms_en = Column(String(200))
    rooms_ar = Column(String(200))
    
    # Парковка (изменили название с parking на has_parking)
    has_parking = Column(Numeric(1, 0))  # 0=No, 1=Yes
    
    # Ближайшие объекты
    nearest_landmark_en = Column(String(200))
    nearest_landmark_ar = Column(String(200))
    nearest_metro_en = Column(String(201))
    nearest_metro_ar = Column(String(200))
    nearest_mall_en = Column(String(203))
    nearest_mall_ar = Column(String(202))
    
    # Права собственности
    is_free_hold = Column(Numeric(1, 0))
    
    # Тип регистрации
    reg_type_id = Column(Numeric(1, 0))
    reg_type_en = Column(String(100))
    reg_type_ar = Column(String(100))
    
    # Площади (добавили новое поле из спецификации)
    procedure_area = Column(Numeric(18, 2))  # The area in square meter
    
    # Новые поля из спецификации
    building_name_en = Column(String(200))
    building_name_ar = Column(String(200))
    
    # Старые поля для совместимости (оставляем, но они не из спецификации)
    trans_size_sqft = Column(Numeric(18, 2))
    trans_size_sqm = Column(Numeric(18, 2))
    actual_area_sqft = Column(Numeric(18, 2))
    actual_area_sqm = Column(Numeric(18, 2))
    
    # Индексы для улучшения производительности
    __table_args__ = (
        Index('idx_transactions_instance_date', 'instance_date'),
        Index('idx_transactions_area_id', 'area_id'),
        Index('idx_transactions_property_type_id', 'property_type_id'),
        Index('idx_transactions_trans_group_id', 'trans_group_id'),
        Index('idx_transactions_procedure_id', 'procedure_id'),
    )