import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import time
import math
import numpy as np
from decimal import Decimal

# Настройки
DATA_FOLDER = r"C:\Users\User\Desktop\DubaiProject\datasets"
DB_URI = "postgresql://user:password@localhost:5432/real_estate"

def convert_float_to_decimal(value, decimal_places=0):
    """Конвертирует значения в Decimal, убирая .0 для целых чисел"""
    if pd.isna(value) or value is None:
        return None
    
    # Если это строка
    if isinstance(value, str):
        cleaned = value.strip().replace('"', '').replace(',', '')
        if cleaned == '' or cleaned.lower() in ['null', 'nan', 'none', 'na', 'n/a']:
            return None
        
        # Проверяем, заканчивается ли на .0
        if cleaned.endswith('.0'):
            # Убираем .0 и конвертируем в целое
            try:
                return Decimal(cleaned.rstrip('.0'))
            except:
                return None
        
        # Пытаемся преобразовать в Decimal
        try:
            # Убираем лишние нули в конце для целых чисел
            if '.' in cleaned:
                # Проверяем, является ли целым числом (например, 15802.000)
                try:
                    float_val = float(cleaned)
                    if float_val.is_integer():
                        return Decimal(str(int(float_val)))
                except:
                    pass
            
            # Преобразуем в Decimal
            dec_value = Decimal(cleaned)
            # Округляем до нужного количества знаков
            if decimal_places > 0:
                return round(dec_value, decimal_places)
            return dec_value
        except:
            return None
    
    # Если это float
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        # Если целое число в формате float, конвертируем в Decimal целое
        if value.is_integer():
            return Decimal(str(int(value)))
        # Округляем до нужного количества знаков
        dec_value = Decimal(str(value))
        if decimal_places > 0:
            return round(dec_value, decimal_places)
        return dec_value
    
    # Если это int
    if isinstance(value, (int, np.integer)):
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
        
        # Пробуем pandas с dayfirst=True
        try:
            return pd.to_datetime(value_str, dayfirst=True, errors='coerce').date()
        except:
            return None
    
    return None

def migrate_units_final():
    """Финальная миграция таблицы units"""
    
    from app.database.models import Base, Unit
    
    engine = create_engine(DB_URI)
    
    # Удаляем и создаем таблицу с новыми типами
    print("🔄 Удаляем и создаем таблицу units...")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Проверяем разные варианты имени файла
    possible_names = ["Units.csv", "units.csv", "DLD_Units.csv", "dld_units.csv"]
    filepath = None
    
    for name in possible_names:
        path = Path(DATA_FOLDER) / name
        if path.exists():
            filepath = path
            print(f"📁 Найден файл: {filepath}")
            break
    
    if not filepath:
        print(f"❌ Файл units не найден в {DATA_FOLDER}")
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
            on_bad_lines='skip'
        )
        
        print(f"📊 Найдено строк: {len(df)}")
        
        # Приводим названия колонок к нижнему регистру
        df.columns = [col.strip().lower() for col in df.columns]
        
        # Маппинг колонок
        column_mapping = {
            'property_id': 'property_id',
            'area_id': 'area_id',
            'zone_id': 'zone_id',
            'area_name_ar': 'area_name_ar',
            'area_name_en': 'area_name_en',
            'land_number': 'land_number',
            'land_sub_number': 'land_sub_number',
            'building_number': 'building_number',
            'unit_number': 'unit_number',
            'unit_balcony_area': 'unit_balcony_area',
            'unit_parking_number': 'unit_parking_number',
            'parking_allocation_type': 'parking_allocation_type',
            'parking_allocation_type_ar': 'parking_allocation_type_ar',
            'parking_allocation_type_en': 'parking_allocation_type_en',
            'common_area': 'common_area',
            'actual_common_area': 'actual_common_area',
            'floor': 'floor',
            'rooms': 'rooms',
            'rooms_ar': 'rooms_ar',
            'rooms_en': 'rooms_en',
            'actual_area': 'actual_area',
            'property_type_id': 'property_type_id',
            'property_type_ar': 'property_type_ar',
            'property_type_en': 'property_type_en',
            'property_sub_type_id': 'property_sub_type_id',
            'property_sub_type_ar': 'property_sub_type_ar',
            'property_sub_type_en': 'property_sub_type_en',
            'parent_property_id': 'parent_property_id',
            'grandparent_property_id': 'grandparent_property_id',
            'creation_date': 'creation_date',
            'munc_zip_code': 'munc_zip_code',
            'munc_number': 'munc_number',
            'parcel_id': 'parcel_id',
            'is_free_hold': 'is_free_hold',
            'is_lease_hold': 'is_lease_hold',
            'is_registered': 'is_registered',
            'pre_registration_number': 'pre_registration_number',
            'master_project_id': 'master_project_id',
            'master_project_en': 'master_project_en',
            'master_project_ar': 'master_project_ar',
            'project_id': 'project_id',
            'project_name_ar': 'project_name_ar',
            'project_name_en': 'project_name_en',
            'land_type_id': 'land_type_id',
            'land_type_ar': 'land_type_ar',
            'land_type_en': 'land_type_en',
        }
        
        # Переименовываем колонки
        df = df.rename(columns=column_mapping)
        
        # Оставляем только нужные колонки
        needed_columns = list(column_mapping.values())
        df = df[[col for col in needed_columns if col in df.columns]]
        
        # Очистка данных
        print("🧹 Очистка данных...")
        
        # Числовые поля с их точностью
        numeric_fields = {
            # Большие целые числа (ID)
            'property_id': 0,
            'area_id': 0,
            'zone_id': 0,
            'land_sub_number': 0,
            'parking_allocation_type': 0,
            'property_type_id': 0,
            'property_sub_type_id': 0,
            'parent_property_id': 0,
            'grandparent_property_id': 0,
            'parcel_id': 0,
            'master_project_id': 0,
            'project_id': 0,
            'land_type_id': 0,
            
            # Количественные характеристики
            'rooms': 0,
            
            # Площади с плавающей точкой
            'unit_balcony_area': 2,
            'common_area': 4,
            'actual_common_area': 0,  # NUMBER без указания точности
            'actual_area': 2,
            
            # Флаги (0 или 1)
            'is_free_hold': 0,
            'is_lease_hold': 0,
            'is_registered': 0,
        }
        
        # Конвертируем все числовые поля в Decimal
        for col, decimal_places in numeric_fields.items():
            if col in df.columns:
                df[col] = df[col].apply(lambda x: convert_float_to_decimal(x, decimal_places))
                non_null = df[col].notna().sum()
                print(f"  {col}: {non_null} значений")
        
        # Даты
        if 'creation_date' in df.columns:
            df['creation_date'] = pd.to_datetime(df['creation_date'], errors='coerce', dayfirst=True)
            df['creation_date'] = df['creation_date'].dt.date
        
        # Текстовые поля с максимальными длинами
        text_fields = {
            'area_name_ar': 200,
            'area_name_en': 200,
            'land_number': 100,
            'building_number': 100,
            'unit_number': 100,
            'unit_parking_number': 1000,
            'parking_allocation_type_ar': 100,
            'parking_allocation_type_en': 100,
            'floor': 40,
            'rooms_ar': 60,
            'rooms_en': 60,
            'property_type_ar': 50,
            'property_type_en': 50,
            'property_sub_type_ar': 50,
            'property_sub_type_en': 50,
            'munc_zip_code': 3,
            'munc_number': 10,
            'pre_registration_number': 100,
            'master_project_en': 250,
            'master_project_ar': 250,
            'project_name_ar': 200,
            'project_name_en': 200,
            'land_type_ar': 50,
            'land_type_en': 50,
        }
        
        for col, max_len in text_fields.items():
            if col in df.columns:
                df[col] = df[col].fillna('').astype(str).str.strip()
                # Обрезаем до максимальной длины
                if max_len:
                    df[col] = df[col].str[:max_len]
                df[col] = df[col].replace({'': None, 'nan': None, 'None': None, 'NULL': None})
        
        # Заменяем NaN на None
        df = df.where(pd.notna(df), None)
        
        # Удаляем дубликаты property_id во всем DataFrame
        initial_count = len(df)
        df = df.drop_duplicates(subset='property_id', keep='first')
        removed_duplicates = initial_count - len(df)
        print(f"📊 Удалено дубликатов property_id: {removed_duplicates}")
        
        print(f"📊 После очистки осталось: {len(df)} записей")
        
        # Проверяем первые записи
        if len(df) > 0:
            print("\n🔍 Проверка примеров данных:")
            for i in range(min(3, len(df))):
                print(f"\nЗапись {i+1}:")
                row = df.iloc[i]
                for col in ['property_id', 'unit_number', 'building_number', 'area_name_en', 'creation_date']:
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
                
                session.bulk_insert_mappings(Unit, clean_batch)
                session.commit()
                inserted_count += len(clean_batch)
                
                if inserted_count % 10000 == 0:
                    print(f"  ✅ Вставлено {inserted_count}/{len(df)} записей")
                
            except Exception as e:
                error_msg = str(e)[:200]
                print(f"  ❌ Ошибка при вставке batch: {error_msg}")
                session.rollback()
                
                # Если это ошибка дублирования ключа, пропускаем весь batch
                if "duplicate key" in error_msg.lower() or "unique violation" in error_msg.lower():
                    print(f"  ⚠️  Пропускаем batch из-за дублирующихся ключей")
                    # В этом случае пропускаем весь batch
                    continue
                
                # Для других ошибок пробуем вставить построчно
                batch_inserted = 0
                for record in clean_batch:
                    try:
                        unit = Unit(**record)
                        session.add(unit)
                        session.commit()
                        inserted_count += 1
                        batch_inserted += 1
                    except Exception as e2:
                        session.rollback()
                        error_msg2 = str(e2)[:100]
                        # Если это ошибка дублирования, просто пропускаем
                        if "duplicate key" not in error_msg2.lower() and "unique violation" not in error_msg2.lower():
                            failed_records.append({
                                'property_id': record.get('property_id'),
                                'error': error_msg2
                            })
                        continue
                
                if batch_inserted > 0:
                    print(f"  ⚠️  В batch вставлено {batch_inserted} из {len(clean_batch)} записей")
        
        print(f"\n📊 Результат миграции:")
        print(f"  ✅ Успешно вставлено: {inserted_count} записей")
        print(f"  📊 Удалено дубликатов: {removed_duplicates}")
        print(f"  📊 Всего обработано: {initial_count} записей в CSV")
        
        if failed_records:
            print(f"  ❌ Ошибок (не дубликаты): {len(failed_records)}")
            for err in failed_records[:10]:
                print(f"    property_id={err['property_id']}: {err['error']}")
        
        # Проверяем результат
        count = session.query(Unit).count()
        print(f"\n📊 Всего записей в таблице units: {count:,}")
        
        # Проверяем несколько записей из БД
        print("\n🔍 Проверка данных в БД:")
        if count > 0:
            test_records = session.query(Unit).order_by(Unit.property_id).limit(3).all()
            for rec in test_records:
                print(f"\n  property_id: {rec.property_id} (тип: {type(rec.property_id).__name__})")
                print(f"  unit_number: {rec.unit_number}")
                print(f"  building_number: {rec.building_number}")
                print(f"  area_name_en: {rec.area_name_en}")
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
    migrate_units_final()