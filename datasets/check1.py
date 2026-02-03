import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import time
import math

# Настройки
DATA_FOLDER = r"C:\Users\User\Desktop\DubaiProject\datasets"
DB_URI = "postgresql://user:password@localhost:5432/real_estate"

def clean_numeric(value):
    """Очистка числовых значений с безопасным преобразованием"""
    if pd.isna(value) or value is None:
        return None
    
    # Если уже число
    if isinstance(value, (int, float)):
        if isinstance(value, float) and math.isnan(value):
            return None
        return value
    
    # Если строка
    if isinstance(value, str):
        cleaned = value.strip().replace('"', '').replace(',', '')
        if cleaned == '' or cleaned.lower() in ['null', 'nan', 'none', 'n/a']:
            return None
        
        # Пытаемся преобразовать
        try:
            # Если содержит точку - пытаемся как float
            if '.' in cleaned:
                num = float(cleaned)
                # Если целое число в float виде (1.0) - конвертируем в int
                if num.is_integer():
                    return int(num)
                return num
            else:
                return int(cleaned)
        except (ValueError, TypeError):
            # Если не получается как число, возвращаем как строку для отладки
            print(f"⚠️  Не удалось преобразовать в число: '{value}' -> '{cleaned}'")
            return None
    
    return None

def clean_date(value):
    """Очистка даты"""
    if pd.isna(value) or value is None:
        return None
    
    if isinstance(value, str):
        value_str = value.strip().replace('"', '')
        if value_str == '':
            return None
        
        # Форматы дат в CSV
        date_formats = [
            '%d-%m-%Y',    # 17-05-2003
            '%d/%m/%Y',    # 17/05/2003
            '%Y-%m-%d',    # 2003-05-17
            '%Y/%m/%d',    # 2003/05/17
            '%d.%m.%Y',    # 17.05.2003
        ]
        
        for fmt in date_formats:
            try:
                dt = pd.to_datetime(value_str, format=fmt)
                return dt.date()
            except (ValueError, TypeError):
                continue
        
        # Если не распарсилось, пробуем автоопределение
        try:
            dt = pd.to_datetime(value_str)
            return dt.date()
        except:
            return None
    
    # Если уже datetime
    if isinstance(value, pd.Timestamp):
        return value.date()
    
    return None

def clean_text(value):
    """Очистка текста"""
    if pd.isna(value) or value is None:
        return None
    
    if isinstance(value, (int, float)):
        if math.isnan(value):
            return None
        return str(value)
    
    if isinstance(value, str):
        cleaned = value.strip()
        # Убираем кавычки если есть
        if (cleaned.startswith('"') and cleaned.endswith('"')) or \
           (cleaned.startswith("'") and cleaned.endswith("'")):
            cleaned = cleaned[1:-1]
        return cleaned if cleaned else None
    
    return str(value)

def safe_bulk_insert(session, model, records, batch_size=100):
    """Безопасная пакетная вставка с обработкой ошибок"""
    inserted = 0
    errors = []
    
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        
        # Проверяем каждую запись в batch
        clean_batch = []
        for record in batch:
            try:
                # Создаем объект модели для проверки
                obj = model(**record)
                clean_batch.append(record)
            except Exception as e:
                errors.append((record.get('project_id', 'unknown'), str(e)))
                print(f"⚠️  Ошибка валидации записи project_id={record.get('project_id')}: {e}")
        
        if clean_batch:
            try:
                session.bulk_insert_mappings(model, clean_batch)
                session.commit()
                inserted += len(clean_batch)
                print(f"✅ Вставлено {min(i+batch_size, len(records))}/{len(records)} записей")
            except Exception as e:
                print(f"❌ Ошибка при пакетной вставке: {str(e)[:200]}")
                session.rollback()
                
                # Пробуем вставить построчно
                for record in clean_batch:
                    try:
                        obj = model(**record)
                        session.add(obj)
                        session.commit()
                        inserted += 1
                    except Exception as e2:
                        session.rollback()
                        errors.append((record.get('project_id', 'unknown'), str(e2)))
                        print(f"❌ Ошибка записи project_id={record.get('project_id')}: {str(e2)[:100]}")
    
    return inserted, errors

def migrate_projects():
    """Основная функция миграции"""
    engine = create_engine(DB_URI)
    
    # Импортируем модель после настройки
    from app.database.models import Base, Project
    
    # Пересоздаем таблицу
    print("🔄 Пересоздаем таблицу projects...")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    filepath = Path(DATA_FOLDER) / "Projects.csv"
    
    print(f"📖 Чтение файла: {filepath}")
    start_time = time.time()
    
    try:
        # Читаем CSV с указанием всех возможных значений NaN
        df = pd.read_csv(
            filepath, 
            encoding='utf-8-sig',
            dtype=str,  # Читаем все как строку
            keep_default_na=False,
            na_values=['', 'NULL', 'null', 'Null', 'N/A', 'n/a', 'NaN', 'nan']
        )
        
        print(f"📊 Загружено строк: {len(df)}")
        print(f"📋 Колонки: {list(df.columns)}")
        
        # Приводим названия колонок к нужному виду
        df.columns = df.columns.str.strip().str.lower()
        
        # Маппинг колонок
        column_mapping = {
            'project_id': 'project_id',
            'project_number': 'project_number',
            'project_name': 'project_name',
            'developer_id': 'developer_id',
            'developer_number': 'developer_number',
            'developer_name': 'developer_name',
            'master_developer_id': 'master_developer_id',
            'master_developer_number': 'master_developer_number',
            'master_developer_name': 'master_developer_name',
            'project_start_date': 'project_start_date',
            'project_end_date': 'project_end_date',
            'project_type_id': 'project_type_id',
            'project_type_ar': 'project_type_ar',
            'project_classification_id': 'project_classification_id',
            'project_classification_ar': 'project_classification_ar',
            'escrow_agent_id': 'escrow_agent_id',
            'escrow_agent_name': 'escrow_agent_name',
            'project_status': 'project_status',
            'project_status_ar': 'project_status_ar',
            'percent_completed': 'percent_completed',
            'completion_date': 'completion_date',
            'cancellation_date': 'cancellation_date',
            'project_description_ar': 'project_description_ar',
            'project_description_en': 'project_description_en',
            'property_id': 'property_id',
            'area_id': 'area_id',
            'area_name_ar': 'area_name_ar',
            'area_name_en': 'area_name_en',
        }
        
        # Переименовываем
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        
        # Оставляем только нужные колонки
        needed_columns = [v for k, v in column_mapping.items() if k in df.columns]
        df = df[[col for col in needed_columns if col in df.columns]]
        
        # Очистка данных
        print("🧹 Очистка данных...")
        
        # Все числовые поля
        numeric_fields = [
            'project_id', 'project_number', 'developer_id', 'developer_number',
            'master_developer_id', 'master_developer_number', 'project_type_id',
            'project_classification_id', 'escrow_agent_id', 'percent_completed',
            'property_id', 'area_id'
        ]
        
        for col in numeric_fields:
            if col in df.columns:
                df[col] = df[col].apply(clean_numeric)
                # Подсчет непустых значений
                non_null = df[col].notna().sum()
                print(f"  {col}: {non_null} непустых значений")
        
        # Даты
        date_fields = ['project_start_date', 'project_end_date', 'completion_date', 'cancellation_date']
        for col in date_fields:
            if col in df.columns:
                df[col] = df[col].apply(clean_date)
        
        # Текстовые поля
        text_fields = [
            'project_name', 'developer_name', 'master_developer_name',
            'project_type_ar', 'project_classification_ar', 'escrow_agent_name',
            'project_status', 'project_status_ar', 'project_description_ar',
            'project_description_en', 'area_name_ar', 'area_name_en'
        ]
        
        for col in text_fields:
            if col in df.columns:
                df[col] = df[col].apply(clean_text)
        
        # Заменяем оставшиеся NaN на None
        df = df.where(pd.notna(df), None)
        
        # Преобразуем в записи
        records = df.to_dict('records')
        
        print(f"\n💾 Готово к вставке: {len(records)} записей")
        
        # Пример первых записей
        print("\n📝 Примеры данных (первые 3 записи):")
        for i, record in enumerate(records[:3]):
            print(f"\nЗапись {i+1}:")
            for key, value in list(record.items())[:5]:  # Первые 5 полей
                print(f"  {key}: {value}")
        
        # Вставка данных
        print("\n📥 Вставка данных в БД...")
        inserted, errors = safe_bulk_insert(session, Project, records, batch_size=100)
        
        # Проверяем результат
        count = session.query(Project).count()
        
        print(f"\n📊 Результат миграции:")
        print(f"  ✅ Успешно вставлено: {inserted}")
        print(f"  ❌ Ошибок: {len(errors)}")
        print(f"  📊 Всего в БД: {count}")
        
        if errors:
            print(f"\n⚠️  Ошибки (первые 5):")
            for project_id, error in errors[:5]:
                print(f"  project_id={project_id}: {error[:100]}")
        
        # Проверяем данные в БД
        print("\n🔍 Проверка данных в БД:")
        test_records = session.query(Project).order_by(Project.project_id).limit(5).all()
        for rec in test_records:
            print(f"\n  project_id: {rec.project_id}")
            print(f"  project_name: {rec.project_name}")
            print(f"  property_id: {rec.property_id}")
            print(f"  developer_id: {rec.developer_id}")
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {str(e)}")
        import traceback
        traceback.print_exc()
        session.rollback()
    
    elapsed = time.time() - start_time
    print(f"\n⏱️  Время выполнения: {elapsed:.2f} сек")
    
    session.close()

if __name__ == "__main__":
    migrate_projects()