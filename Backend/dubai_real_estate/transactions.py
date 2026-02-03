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

# Импортируем модель Valuation
from app.database.models import Base, Valuation

# Настройки
DATA_FOLDER = r"C:\Users\User\Desktop\DubaiProject\datasets"
DB_URI = "postgresql://user:password@localhost:5432/real_estate"

def convert_float_to_decimal(value, decimal_places=2):
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
    """Безопасное преобразование даты"""
    if pd.isna(value) or value is None:
        return None
    
    if isinstance(value, str):
        value_str = value.strip().replace('"', '')
        if value_str == '':
            return None
        
        # Пробуем разные форматы даты
        try:
            # Для TIMESTAMP формата
            if ' ' in value_str:
                return pd.to_datetime(value_str, errors='coerce').date()
            else:
                return pd.to_datetime(value_str, dayfirst=True, errors='coerce').date()
        except:
            return None
    
    return None

def migrate_valuation_final():
    """Финальная миграция таблицы valuation"""
    
    engine = create_engine(DB_URI)
    
    # Удаляем и создаем таблицу с новыми типами
    print("🔄 Удаляем и создаем таблицу valuation...")
    # Используем Base.metadata для работы с таблицей
    Base.metadata.drop_all(engine, tables=[Valuation.__table__], checkfirst=True)
    Base.metadata.create_all(engine, tables=[Valuation.__table__])
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Проверяем разные варианты имени файла
    possible_names = ["Valuation.csv", "valuation.csv", "DLD_Valuation.csv", "dld_valuation.csv", "VALUATION.CSV"]
    filepath = None
    
    for name in possible_names:
        path = Path(DATA_FOLDER) / name
        if path.exists():
            filepath = path
            print(f"📁 Найден файл: {filepath}")
            break
    
    if not filepath:
        print(f"❌ Файл valuation не найден в {DATA_FOLDER}")
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
            'procedure_id': ['procedure_id', 'procedureid', 'proc_id'],
            'procedure_year': ['procedure_year', 'proceduryear', 'proc_year', 'year'],
            'procedure_number': ['procedure_number', 'procedurenumber', 'proc_number', 'procno'],
            'property_total_value': ['property_total_value', 'propertytotalvalue', 'total_value'],
            'procedure_name_ar': ['procedure_name_ar', 'procedurename_ar', 'procname_ar'],
            'procedure_name_en': ['procedure_name_en', 'procedurename_en', 'procname_en'],
            'area_id': ['area_id', 'areaid'],
            'area_name_ar': ['area_name_ar', 'areaname_ar', 'area_ar'],
            'area_name_en': ['area_name_en', 'areaname_en', 'area_en'],
            'actual_area': ['actual_area', 'actualarea'],
            'instance_date': ['instance_date', 'instancedate', 'date'],
            'actual_worth': ['actual_worth', 'actualworth'],
            'row_status_code': ['row_status_code', 'rowstatuscode', 'status'],
            'procedure_area': ['procedure_area', 'procedurearea'],
            'property_type_id': ['property_type_id', 'propertytypeid'],
            'property_type_ar': ['property_type_ar', 'propertytype_ar'],
            'property_type_en': ['property_type_en', 'propertytype_en'],
            'property_sub_type_id': ['property_sub_type_id', 'propertysubtypeid'],
            'property_sub_type_ar': ['property_sub_type_ar', 'propertysubtype_ar'],
            'property_sub_type_en': ['property_sub_type_en', 'propertysubtype_en'],
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
            # Первичные ключи
            'procedure_id': 0,  # SMALLINT
            'procedure_year': 0,  # INTEGER
            'procedure_number': 0,  # BIGINT
            
            # Денежные значения
            'property_total_value': 2,
            'actual_worth': 2,
            
            # Площади
            'actual_area': 2,
            'procedure_area': 2,
            
            # ID
            'area_id': 0,  # BIGINT
            'property_type_id': 0,  # INTEGER (NUMBER(4))
            'property_sub_type_id': 0,  # INTEGER (NUMBER(4))
        }
        
        # Конвертируем все числовые поля в Decimal
        for col, decimal_places in numeric_fields.items():
            if col in df.columns:
                df[col] = df[col].apply(lambda x: convert_float_to_decimal(x, decimal_places))
                non_null = df[col].notna().sum()
                print(f"  {col}: {non_null} непустых значений")
        
        # Дата
        if 'instance_date' in df.columns:
            df['instance_date'] = df['instance_date'].apply(convert_date_safe)
            non_null_dates = df['instance_date'].notna().sum()
            print(f"  instance_date: {non_null_dates} валидных дат")
        
        # Текстовые поля с максимальными длинами
        text_fields = {
            'procedure_name_ar': 100,
            'procedure_name_en': 100,
            'area_name_ar': 200,
            'area_name_en': 200,
            'row_status_code': 100,
            'property_type_ar': 50,
            'property_type_en': 50,
            'property_sub_type_ar': 50,
            'property_sub_type_en': 50,
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
        
        # Удаляем записи без всех трех первичных ключей
        initial_count = len(df)
        pk_columns = [col for col in ['procedure_id', 'procedure_year', 'procedure_number'] if col in df.columns]
        if pk_columns:
            df = df.dropna(subset=pk_columns, how='any')
            removed_no_pk = initial_count - len(df)
            print(f"📊 Удалено записей без первичных ключей: {removed_no_pk}")
        
        # Удаляем дубликаты по составному первичному ключу
        if len(pk_columns) >= 2:  # Минимум 2 колонки для составного ключа
            df = df.drop_duplicates(subset=pk_columns, keep='first')
            removed_duplicates = initial_count - removed_no_pk - len(df)
            print(f"📊 Удалено дубликатов по PK: {removed_duplicates}")
        else:
            removed_duplicates = 0
            print("⚠️ Недостаточно колонок для составного первичного ключа")
        
        print(f"📊 После очистки осталось: {len(df)} записей")
        
        # Проверяем первые записи
        if len(df) > 0:
            print("\n🔍 Проверка примеров данных:")
            for i in range(min(3, len(df))):
                print(f"\nЗапись {i+1}:")
                row = df.iloc[i]
                for col in ['procedure_id', 'procedure_year', 'procedure_number', 'procedure_name_en', 'instance_date']:
                    if col in df.columns:
                        val = row[col]
                        if val is not None:
                            print(f"  {col}: {val} (тип: {type(val).__name__})")
                        else:
                            print(f"  {col}: None")
        
        # Вставляем данные порциями
        print("\n📥 Вставка данных в БД...")
        
        batch_size = 1000
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
                
                session.bulk_insert_mappings(Valuation, clean_batch)
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
                            valuation = Valuation(**record)
                            session.add(valuation)
                            session.commit()
                            inserted_count += 1
                            batch_inserted += 1
                        except Exception as e2:
                            session.rollback()
                            error_msg2 = str(e2)[:100]
                            # Если это ошибка дублирования, просто пропускаем
                            if "duplicate key" not in error_msg2.lower() and "unique violation" not in error_msg2.lower():
                                failed_records.append({
                                    'procedure_id': record.get('procedure_id'),
                                    'procedure_year': record.get('procedure_year'),
                                    'procedure_number': record.get('procedure_number'),
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
                print(f"    PK=({err['procedure_id']},{err['procedure_year']},{err['procedure_number']}): {err['error']}")
        
        # Проверяем результат
        count = session.query(Valuation).count()
        print(f"\n📊 Всего записей в таблице valuation: {count:,}")
        
        # Проверяем несколько записей из БД
        print("\n🔍 Проверка данных в БД:")
        if count > 0:
            test_records = session.query(Valuation).order_by(
                Valuation.procedure_year, Valuation.procedure_number
            ).limit(3).all()
            for rec in test_records:
                print(f"\n  PK: ({rec.procedure_id},{rec.procedure_year},{rec.procedure_number})")
                print(f"  procedure_name_en: {rec.procedure_name_en}")
                print(f"  property_total_value: {rec.property_total_value} (тип: {type(rec.property_total_value).__name__})")
                print(f"  instance_date: {rec.instance_date}")
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
    migrate_valuation_final()