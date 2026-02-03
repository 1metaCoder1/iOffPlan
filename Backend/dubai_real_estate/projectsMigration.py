import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import time
import math
from decimal import Decimal
import sys
import os

# Добавляем путь к проекту для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем модель Project
from app.database.models import Base, Project

# Настройки
DATA_FOLDER = r"C:\Users\User\Desktop\DubaiProject\datasets"
DB_URI = "postgresql://user:password@localhost:5432/real_estate"

def convert_float_to_decimal(value, decimal_places=0):
    """Конвертирует значения в Decimal с указанной точностью"""
    if pd.isna(value) or value is None:
        return None
    
    if isinstance(value, str):
        cleaned = value.strip().replace('"', '').replace(',', '')
        if cleaned == '' or cleaned.lower() in ['null', 'nan', 'none', 'na', 'n/a']:
            return None
        
        # Убираем .0 для целых чисел
        if cleaned.endswith('.0'):
            try:
                return Decimal(cleaned.rstrip('.0'))
            except:
                return None
        
        try:
            # Проверяем, является ли целым числом с дробной частью .000...
            if '.' in cleaned:
                try:
                    float_val = float(cleaned)
                    if float_val.is_integer():
                        return Decimal(str(int(float_val)))
                except:
                    pass
            
            dec_value = Decimal(cleaned)
            if decimal_places > 0:
                return round(dec_value, decimal_places)
            return dec_value
        except:
            return None
    
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        if value.is_integer():
            return Decimal(str(int(value)))
        dec_value = Decimal(str(value))
        if decimal_places > 0:
            return round(dec_value, decimal_places)
        return dec_value
    
    if isinstance(value, (int, Decimal)):
        return Decimal(str(value))
    
    return None

def convert_date_safe(value):
    """Безопасное преобразование даты в формате DD-MM-YYYY"""
    if pd.isna(value) or value is None:
        return None
    
    if isinstance(value, str):
        value_str = value.strip().replace('"', '')
        if value_str == '':
            return None
        
        # Пробуем разные форматы даты, в первую очередь DD-MM-YYYY
        try:
            return pd.to_datetime(value_str, dayfirst=True, errors='coerce').date()
        except:
            return None
    
    return None

def migrate_projects_final():
    """Финальная миграция таблицы projects"""
    
    engine = create_engine(DB_URI)
    
    # Удаляем и создаем таблицу с новыми типами
    print("🔄 Удаляем и создаем таблицу projects...")
    # Используем Base.metadata для работы с таблицей
    Base.metadata.drop_all(engine, tables=[Project.__table__], checkfirst=True)
    Base.metadata.create_all(engine, tables=[Project.__table__])
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Проверяем разные варианты имени файла
    possible_names = ["Projects.csv", "projects.csv", "DLD_Projects.csv", 
                      "dld_projects.csv", "PROJECTS.CSV", "Project.csv", "project.csv"]
    filepath = None
    
    for name in possible_names:
        path = Path(DATA_FOLDER) / name
        if path.exists():
            filepath = path
            print(f"📁 Найден файл: {filepath}")
            break
    
    if not filepath:
        print(f"❌ Файл projects не найден в {DATA_FOLDER}")
        print("Искали файлы:", possible_names)
        return
    
    print(f"📖 Чтение файла: {filepath}")
    start_time = time.time()
    
    try:
        # Читаем CSV с правильными параметрами
        df = pd.read_csv(
            filepath, 
            encoding='utf-8-sig',
            dtype=str,  # Все как строка
            keep_default_na=False,
            na_values=['', 'NULL', 'null', 'Null', 'N/A', 'n/a', 'NaN', 'nan'],
            on_bad_lines='skip',
            low_memory=False
        )
        
        print(f"📊 Найдено строк: {len(df)}")
        
        # Приводим названия колонок к нижнему регистру
        df.columns = [col.strip().lower() for col in df.columns]
        
        # Маппинг колонок (проверяем возможные варианты имен)
        column_mapping = {}
        possible_columns = {
            # Основные поля
            'project_id': ['project_id', 'projectid'],
            'project_number': ['project_number', 'projectnumber'],
            'project_name': ['project_name', 'projectname'],
            
            # Информация о разработчике
            'developer_id': ['developer_id', 'developerid'],
            'developer_number': ['developer_number', 'developernumber'],
            'developer_name': ['developer_name', 'developername'],
            
            # Информация о главном разработчике
            'master_developer_id': ['master_developer_id', 'masterdeveloperid'],
            'master_developer_number': ['master_developer_number', 'masterdevelopernumber'],
            'master_developer_name': ['master_developer_name', 'masterdevelopername'],
            
            # Даты проекта
            'project_start_date': ['project_start_date', 'projectstartdate', 'start_date'],
            'project_end_date': ['project_end_date', 'projectenddate', 'end_date'],
            
            # Тип проекта
            'project_type_id': ['project_type_id', 'projecttypeid'],
            'project_type_ar': ['project_type_ar', 'projecttype_ar'],
            
            # Классификация проекта
            'project_classification_id': ['project_classification_id', 'projectclassificationid'],
            'project_classification_ar': ['project_classification_ar', 'projectclassification_ar'],
            
            # Информация о гарантийном агенте
            'escrow_agent_id': ['escrow_agent_id', 'escrowagentid'],
            'escrow_agent_name': ['escrow_agent_name', 'escrowagentname'],
            
            # Статус проекта
            'project_status': ['project_status', 'projectstatus'],
            'project_status_ar': ['project_status_ar', 'projectstatus_ar'],
            
            # Процент завершения
            'percent_completed': ['percent_completed', 'percentcompleted', 'completion_percentage'],
            
            # Дополнительные даты
            'completion_date': ['completion_date', 'completiondate'],
            'cancellation_date': ['cancellation_date', 'cancellationdate'],
            
            # Описание проекта
            'project_description_ar': ['project_description_ar', 'projectdescription_ar'],
            'project_description_en': ['project_description_en', 'projectdescription_en'],
            
            # Связанная собственность
            'property_id': ['property_id', 'propertyid'],
            
            # Район
            'area_id': ['area_id', 'areaid'],
            'area_name_ar': ['area_name_ar', 'areaname_ar'],
            'area_name_en': ['area_name_en', 'areaname_en'],
        }
        
        # Находим соответствия
        for target_col, possible_names in possible_columns.items():
            for possible in possible_names:
                if possible in df.columns:
                    column_mapping[possible] = target_col
                    break
        
        print(f"📊 Найдено {len(column_mapping)} колонок из {len(possible_columns)} ожидаемых")
        
        # Переименовываем колонки
        df = df.rename(columns=column_mapping)
        
        # Создаем DataFrame только с нужными колонками
        needed_columns = list(possible_columns.keys())
        available_columns = [col for col in needed_columns if col in df.columns]
        
        # Если нет всех колонок, выводим предупреждение
        missing = set(needed_columns) - set(available_columns)
        if missing:
            print(f"⚠️ Отсутствуют колонки: {missing}")
        
        df = df[available_columns]
        
        # Очистка данных
        print("🧹 Очистка данных...")
        
        # Числовые поля с их точностью
        numeric_fields = {
            # ID
            'project_id': 0,
            'project_number': 0,
            'developer_id': 0,
            'developer_number': 0,
            'master_developer_id': 0,
            'master_developer_number': 0,
            'project_type_id': 0,
            'project_classification_id': 0,
            'escrow_agent_id': 0,
            'property_id': 0,
            'area_id': 0,
            
            # Процент завершения
            'percent_completed': 3,
        }
        
        # Конвертируем все числовые поля в Decimal
        for col, decimal_places in numeric_fields.items():
            if col in df.columns:
                df[col] = df[col].apply(lambda x: convert_float_to_decimal(x, decimal_places))
                non_null = df[col].notna().sum()
                print(f"  {col}: {non_null} непустых значений")
        
        # Даты
        date_fields = [
            'project_start_date', 'project_end_date', 
            'completion_date', 'cancellation_date'
        ]
        
        for date_field in date_fields:
            if date_field in df.columns:
                df[date_field] = df[date_field].apply(convert_date_safe)
                non_null_dates = df[date_field].notna().sum()
                print(f"  {date_field}: {non_null_dates} валидных дат")
        
        # Текстовые поля с максимальными длинами
        text_fields = {
            'project_name': 200,
            'developer_name': 200,
            'master_developer_name': 200,
            'project_type_ar': 100,
            'project_classification_ar': 50,
            'escrow_agent_name': 200,
            'project_status': 200,
            'project_status_ar': 100,
            'project_description_ar': 2000,
            'project_description_en': 2000,
            'area_name_ar': 200,
            'area_name_en': 200,
        }
        
        for col, max_len in text_fields.items():
            if col in df.columns:
                df[col] = df[col].fillna('').astype(str).str.strip()
                # Обрезаем до максимальной длины
                if max_len:
                    df[col] = df[col].str[:max_len]
                df[col] = df[col].replace({'': None, 'nan': None, 'None': None, 'NULL': None})
                non_null = df[col].notna().sum()
                print(f"  {col}: {non_null} непустых значений")
        
        # Заменяем NaN на None
        df = df.where(pd.notna(df), None)
        
        # Удаляем записи без первичного ключа
        initial_count = len(df)
        if 'project_id' in df.columns:
            df = df.dropna(subset=['project_id'], how='any')
            removed_no_pk = initial_count - len(df)
            print(f"📊 Удалено записей без первичного ключа: {removed_no_pk}")
        else:
            print("❌ Критическая ошибка: отсутствует колонка project_id!")
            return
        
        # Удаляем дубликаты по первичному ключу
        df = df.drop_duplicates(subset=['project_id'], keep='first')
        removed_duplicates = initial_count - removed_no_pk - len(df)
        print(f"📊 Удалено дубликатов по PK: {removed_duplicates}")
        
        print(f"📊 После очистки осталось: {len(df)} записей")
        
        # Проверяем первые записи
        if len(df) > 0:
            print("\n🔍 Проверка примеров данных:")
            for i in range(min(3, len(df))):
                print(f"\nЗапись {i+1}:")
                row = df.iloc[i]
                sample_cols = ['project_id', 'project_name', 'developer_name', 
                              'project_start_date', 'percent_completed']
                for col in sample_cols:
                    if col in df.columns:
                        val = row[col]
                        if val is not None:
                            print(f"  {col}: {val} (тип: {type(val).__name__})")
                        else:
                            print(f"  {col}: None")
        
        # Вставляем данные порциями
        print("\n📥 Вставка данных в БД...")
        
        batch_size = 500
        inserted_count = 0
        failed_records = []
        
        for i in range(0, len(df), batch_size):
            batch_df = df.iloc[i:i+batch_size]
            records = batch_df.to_dict('records')
            
            try:
                # Преобразуем записи для вставки
                clean_batch = []
                for record in records:
                    clean_record = {}
                    for key, value in record.items():
                        if value is not None:
                            # Для Decimal полей убеждаемся, что они остаются Decimal
                            if key in numeric_fields and isinstance(value, Decimal):
                                clean_record[key] = value
                            else:
                                clean_record[key] = value
                        else:
                            clean_record[key] = None
                    clean_batch.append(clean_record)
                
                session.bulk_insert_mappings(Project, clean_batch)
                session.commit()
                inserted_count += len(clean_batch)
                
                if inserted_count % 10000 == 0:
                    print(f"  ✅ Вставлено {inserted_count}/{len(df)} записей")
                
            except Exception as e:
                error_msg = str(e)[:200]
                print(f"  ❌ Ошибка при вставке batch: {error_msg}")
                session.rollback()
                
                # Если это ошибка дублирования ключа, пробуем вставить построчно
                if "duplicate key" in error_msg.lower() or "unique violation" in error_msg.lower():
                    batch_inserted = 0
                    for record in clean_batch:
                        try:
                            project = Project(**record)
                            session.add(project)
                            session.commit()
                            inserted_count += 1
                            batch_inserted += 1
                        except Exception as e2:
                            session.rollback()
                            error_msg2 = str(e2)[:100]
                            # Если это ошибка дублирования, просто пропускаем
                            if "duplicate key" not in error_msg2.lower() and "unique violation" not in error_msg2.lower():
                                failed_records.append({
                                    'project_id': record.get('project_id'),
                                    'error': error_msg2
                                })
                            continue
                    
                    if batch_inserted > 0:
                        print(f"  ⚠️  В batch вставлено {batch_inserted} из {len(clean_batch)} записей")
                else:
                    # Другие ошибки - пропускаем batch
                    print(f"  ⚠️  Пропускаем batch из-за ошибки: {error_msg}")
                    continue
        
        print(f"\n📊 Результат миграции:")
        print(f"  ✅ Успешно вставлено: {inserted_count} записей")
        print(f"  📊 Удалено без PK: {removed_no_pk}")
        print(f"  📊 Удалено дубликатов: {removed_duplicates}")
        print(f"  📊 Всего обработано: {initial_count} записей в CSV")
        
        if failed_records:
            print(f"  ❌ Ошибок (не дубликаты): {len(failed_records)}")
            for err in failed_records[:10]:
                print(f"    project_id={err['project_id']}: {err['error']}")
        
        # Проверяем результат
        count = session.query(Project).count()
        print(f"\n📊 Всего записей в таблице projects: {count:,}")
        
        # Проверяем несколько записей из БД
        print("\n🔍 Проверка данных в БД:")
        if count > 0:
            test_records = session.query(Project).order_by(
                Project.project_id
            ).limit(3).all()
            for rec in test_records:
                print(f"\n  project_id: {rec.project_id}")
                print(f"  project_name: {rec.project_name}")
                print(f"  developer_name: {rec.developer_name}")
                print(f"  project_start_date: {rec.project_start_date}")
                print(f"  percent_completed: {rec.percent_completed} (тип: {type(rec.percent_completed).__name__})")
        else:
            print("  ❌ В таблице нет записей")
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {str(e)}")
        import traceback
        traceback.print_exc()
        session.rollback()
    
    elapsed = time.time() - start_time
    print(f"\n⏱️  Время выполнения: {elapsed:.2f} сек")
    
    session.close()

if __name__ == "__main__":
    migrate_projects_final()