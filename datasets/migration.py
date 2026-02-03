import pandas as pd
import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, Numeric, BigInteger, SmallInteger, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import re
from pathlib import Path
import time

# Настройки
DATA_FOLDER = r"C:\Users\User\Desktop\DubaiProject\datasets"
DB_USER = "user"
DB_PASS = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "real_estate"
DB_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Модели данных
Base = declarative_base()

class LkpArea(Base):
    __tablename__ = 'lkp_areas'
    area_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name_en = Column(Text)
    name_ar = Column(Text)
    municipality_number = Column(String(3))

class LkpMarketType(Base):
    __tablename__ = 'lkp_market_types'
    market_type_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name_ar = Column(Text)
    name_en = Column(Text)

class LkpTransactionGroup(Base):
    __tablename__ = 'lkp_transaction_groups'
    group_id = Column(BigInteger, primary_key=True, autoincrement=True)
    name_ar = Column(Text)
    name_en = Column(Text)

class LkpTransactionProcedure(Base):
    __tablename__ = 'lkp_transaction_procedures'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(BigInteger)
    procedure_id = Column(BigInteger)
    is_pre_registration = Column(SmallInteger)
    name_ar = Column(Text)
    name_en = Column(Text)

class Valuation(Base):
    __tablename__ = 'valuation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    procedure_id = Column(SmallInteger)
    procedure_year = Column(Integer)
    procedure_number = Column(BigInteger)
    property_total_value = Column(Numeric(18, 2))
    procedure_name_ar = Column(Text)
    procedure_name_en = Column(Text)
    area_id = Column(BigInteger)
    area_name_ar = Column(Text)
    area_name_en = Column(Text)
    actual_area = Column(Numeric(18, 2))
    instance_date = Column(Date)
    actual_worth = Column(Numeric(18, 2))
    row_status_code = Column(String(100))
    procedure_area = Column(Numeric(18, 2))
    property_type_id = Column(Integer)
    property_type_ar = Column(Text)
    property_type_en = Column(Text)
    property_sub_type_id = Column(Integer)
    property_sub_type_ar = Column(Text)
    property_sub_type_en = Column(Text)

class Unit(Base):
    __tablename__ = 'units'
    property_id = Column(BigInteger, primary_key=True)
    area_id = Column(BigInteger)
    zone_id = Column(Integer)
    area_name_ar = Column(Text)
    area_name_en = Column(Text)
    land_number = Column(String(100))
    land_sub_number = Column(BigInteger)
    building_number = Column(String(100))
    unit_number = Column(String(100))
    unit_balcony_area = Column(Numeric(10, 2))
    unit_parking_number = Column(Text)
    parking_allocation_type = Column(Integer)
    parking_allocation_type_ar = Column(Text)
    parking_allocation_type_en = Column(Text)
    common_area = Column(Numeric(20, 4))
    actual_common_area = Column(Numeric)
    floor = Column(String(40))
    rooms = Column(Integer)
    rooms_ar = Column(String(60))
    rooms_en = Column(String(60))
    actual_area = Column(Numeric(18, 2))
    property_type_id = Column(Integer)
    property_type_ar = Column(Text)
    property_type_en = Column(Text)
    property_sub_type_id = Column(Integer)
    property_sub_type_ar = Column(Text)
    property_sub_type_en = Column(Text)
    parent_property_id = Column(BigInteger)
    grandparent_property_id = Column(BigInteger)
    creation_date = Column(Date)
    munc_zip_code = Column(String(3))
    munc_number = Column(String(10))
    parcel_id = Column(BigInteger)
    is_free_hold = Column(SmallInteger)
    is_lease_hold = Column(SmallInteger)
    is_registered = Column(SmallInteger)
    pre_registration_number = Column(String(100))
    master_project_id = Column(BigInteger)
    master_project_en = Column(Text)
    master_project_ar = Column(Text)
    project_id = Column(BigInteger)
    project_name_ar = Column(Text)
    project_name_en = Column(Text)
    land_type_id = Column(BigInteger)
    land_type_ar = Column(Text)
    land_type_en = Column(Text)

class Building(Base):
    __tablename__ = 'buildings'
    property_id = Column(BigInteger, primary_key=True)
    area_id = Column(BigInteger)
    zone_id = Column(Integer)
    area_name_ar = Column(Text)
    area_name_en = Column(Text)
    land_number = Column(String(100))
    land_sub_number = Column(BigInteger)
    building_number = Column(String(100))
    common_area = Column(Numeric(20, 4))
    actual_common_area = Column(Numeric)
    floors = Column(String(40))
    rooms = Column(Integer)
    rooms_ar = Column(String(60))
    rooms_en = Column(String(60))
    car_parks = Column(Integer)
    built_up_area = Column(Numeric(10, 2))
    is_lease_hold = Column(SmallInteger)
    is_registered = Column(SmallInteger)
    pre_registration_number = Column(String(100))
    master_project_id = Column(BigInteger)
    master_project_en = Column(Text)
    master_project_ar = Column(Text)
    project_id = Column(BigInteger)
    project_name_ar = Column(Text)
    project_name_en = Column(Text)
    land_type_id = Column(Integer)
    land_type_ar = Column(Text)
    land_type_en = Column(Text)
    bld_levels = Column(Integer)
    shops = Column(Integer)
    flats = Column(Integer)
    offices = Column(Integer)
    swimming_pools = Column(SmallInteger)
    elevators = Column(SmallInteger)
    actual_area = Column(Numeric(18, 2))
    property_type_id = Column(Integer)
    property_type_ar = Column(Text)
    property_type_en = Column(Text)
    property_sub_type_id = Column(Integer)
    property_sub_type_ar = Column(Text)
    property_sub_type_en = Column(Text)
    parent_property_id = Column(BigInteger)
    creation_date = Column(Date)
    parcel_id = Column(BigInteger)
    is_free_hold = Column(SmallInteger)

class Project(Base):
    __tablename__ = 'projects'
    project_id = Column(BigInteger, primary_key=True, autoincrement=True)
    project_number = Column(BigInteger)
    project_name = Column(Text)
    developer_id = Column(BigInteger)
    developer_number = Column(BigInteger)
    developer_name = Column(Text)
    master_developer_id = Column(BigInteger)
    master_developer_number = Column(BigInteger)
    master_developer_name = Column(Text)
    project_start_date = Column(Date)
    project_end_date = Column(Date)
    project_type_id = Column(BigInteger)
    project_type_ar = Column(Text)
    project_classification_id = Column(BigInteger)
    project_classification_ar = Column(Text)
    escrow_agent_id = Column(BigInteger)
    escrow_agent_name = Column(Text)
    project_status = Column(Text)
    project_status_ar = Column(Text)
    percent_completed = Column(Numeric(10, 3))
    completion_date = Column(Date)
    cancellation_date = Column(Date)
    project_description_ar = Column(Text)
    project_description_en = Column(Text)
    property_id = Column(BigInteger)
    area_id = Column(BigInteger)
    area_name_ar = Column(Text)
    area_name_en = Column(Text)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(BigInteger)
    instance_date = Column(Date)
    trans_group_id = Column(BigInteger)
    trans_group_en = Column(Text)
    trans_group_ar = Column(Text)
    procedure_id = Column(BigInteger)
    procedure_name_en = Column(Text)
    procedure_name_ar = Column(Text)
    property_type_id = Column(Integer)
    property_type_en = Column(Text)
    property_type_ar = Column(Text)
    property_sub_type_id = Column(Integer)
    property_sub_type_en = Column(Text)
    property_sub_type_ar = Column(Text)
    property_usage_en = Column(Text)
    property_usage_ar = Column(Text)
    area_id = Column(BigInteger)
    area_name_en = Column(Text)
    area_name_ar = Column(Text)
    trans_value = Column(Numeric(18, 2))
    meter_sale_price = Column(Numeric(18, 2))
    actual_worth = Column(Numeric(18, 2))
    rent_value = Column(Numeric(18, 2))
    meter_rent_price = Column(Numeric(18, 2))
    no_of_parties_role_1 = Column(Integer)
    party_type_role_1_en = Column(Text)
    party_type_role_1_ar = Column(Text)
    no_of_parties_role_2 = Column(Integer)
    party_type_role_2_en = Column(Text)
    party_type_role_2_ar = Column(Text)
    master_project_en = Column(Text)
    master_project_ar = Column(Text)
    project_number = Column(BigInteger)
    project_name_en = Column(Text)
    project_name_ar = Column(Text)
    rooms_en = Column(Text)
    rooms_ar = Column(Text)
    parking = Column(SmallInteger)
    nearest_landmark_en = Column(Text)
    nearest_landmark_ar = Column(Text)
    nearest_metro_en = Column(Text)
    nearest_metro_ar = Column(Text)
    nearest_mall_en = Column(Text)
    nearest_mall_ar = Column(Text)
    is_free_hold = Column(SmallInteger)
    reg_type_id = Column(SmallInteger)
    reg_type_en = Column(Text)
    reg_type_ar = Column(Text)
    trans_size_sqft = Column(Numeric(18, 2))
    trans_size_sqm = Column(Numeric(18, 2))
    actual_area_sqft = Column(Numeric(18, 2))
    actual_area_sqm = Column(Numeric(18, 2))

# Функция очистки данных
def clean_value(value, expected_type):
    if value is None or value == '' or str(value).strip().lower() in ['null', 'nan', 'none', '\"\"']:
        return None

    value_str = str(value).strip()

    if value_str.startswith('"') and value_str.endswith('"'):
        value_str = value_str[1:-1]

    if not value_str:
        return None

    if expected_type in ['INTEGER', 'BIGINT', 'SMALLINT', 'NUMERIC', 'DECIMAL']:
        cleaned = re.sub(r'[^\d.-]', '', value_str.replace(',', '.'))
        if not cleaned:
            return None
        try:
            if expected_type in ['INTEGER', 'BIGINT', 'SMALLINT']:
                return int(float(cleaned))
            else:
                return float(cleaned)
        except (ValueError, AttributeError):
            return None

    elif expected_type in ['DATE', 'TIMESTAMP']:
        date_str = value_str.replace('"', '')
        date_formats = ['%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%m-%d-%Y', '%d.%m.%Y', '%Y.%m.%d']
        for fmt in date_formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        return None

    else:
        return value_str

# Основная функция импорта
def import_csv_to_postgres(data_folder, db_uri):
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    files_to_import = [
        ("Lkp_Areas.csv", LkpArea),
        ("Lkp_Market_Types.csv", LkpMarketType),
        ("Lkp_Transaction_Groups.csv", LkpTransactionGroup),
        ("Lkp_Transaction_Procedures.csv", LkpTransactionProcedure),
        ("Valuation.csv", Valuation),
        ("Units.csv", Unit),
        ("Buildings.csv", Building),
        ("Projects.csv", Project),
        ("Transactions.csv", Transaction),
    ]

    for filename, model in files_to_import:
        filepath = Path(data_folder) / filename
        if not filepath.exists():
            print(f"❌ Не найден: {filename}")
            continue

        print(f"\n📥 Импорт {filename} → {model.__tablename__}")
        start_time = time.time()

        try:
            if filename == "Units.csv":
                df = pd.read_csv(filepath, encoding='utf-8-sig', skiprows=2, dtype={
                    'property_id': 'Int64',
                    'area_id': 'Int64',
                    'zone_id': 'Int64',
                    'land_sub_number': 'Int64',
                    'parking_allocation_type': 'Int64',
                    'rooms': 'Int64',
                    'property_type_id': 'Int64',
                    'property_sub_type_id': 'Int64',
                    'parent_property_id': 'Int64',
                    'grandparent_property_id': 'Int64',
                    'parcel_id': 'Int64',
                })
            else:
                df = pd.read_csv(filepath, encoding='utf-8-sig', skiprows=2)

            for col in df.columns:
                col_type = str(next(iter([c.type.__visit_name__ for c in model.__table__.columns if c.name == col]), 'TEXT'))
                df[col] = df[col].apply(lambda x: clean_value(x, col_type))

            df.dropna(how='all', inplace=True)

            records = df.to_dict('records')
            session.bulk_insert_mappings(model, records)
            session.commit()

            count = session.query(model).count()
            print(f"📊 Импортировано строк в БД: {count}")

        except Exception as e:
            print(f"❌ Ошибка при импорте {filename}: {e}")
            session.rollback()

        elapsed = time.time() - start_time
        print(f"⏱️ Готово за {elapsed:.1f} сек")

    session.close()
    print("\n🎉 Все таблицы импортированы!")

if __name__ == "__main__":
    import_csv_to_postgres(DATA_FOLDER, DB_URI)
