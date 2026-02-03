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

# Импортируем модель Transaction
from app.database.models import Base, Transaction

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
            # Для формата DD-MM-YYYY
            return pd.to_datetime(value_str, dayfirst=True, errors='coerce').date()
        except:
            return None
    
    return None

def migrate_transactions_final():
    """Финальная миграция таблицы transactions"""
    
    engine = create_engine(DB_URI)
    
    # Удаляем и создаем таблицу с новыми типами
    print("🔄 Удаляем и создаем таблицу transactions...")
    # Используем Base.metadata для работы с таблицей
    Base.metadata.drop_all(engine, tables=[Transaction.__table__], checkfirst=True)
    Base.metadata.create_all(engine, tables=[Transaction.__table__])
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Проверяем разные варианты имени файла
    possible_names = ["Transactions.csv", "transactions.csv", "DLD_Transactions.csv", 
                      "dld_transactions.csv", "TRANSACTIONS.CSV", "Transaction.csv", "transaction.csv"]
    filepath = None
    
    for name in possible_names:
        path = Path(DATA_FOLDER) / name
        if path.exists():
            filepath = path
            print(f"📁 Найден файл: {filepath}")
            break
    
    if not filepath:
        print(f"❌ Файл transactions не найден в {DATA_FOLDER}")
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
            'transaction_id': ['transaction_id', 'transactionid', 'trans_id'],
            'instance_date': ['instance_date', 'instancedate', 'date', 'transaction_date'],
            
            # Группа транзакции
            'trans_group_id': ['trans_group_id', 'transgroupid', 'group_id'],
            'trans_group_en': ['trans_group_en', 'transgroup_en', 'group_en'],
            'trans_group_ar': ['trans_group_ar', 'transgroup_ar', 'group_ar'],
            
            # Процедура
            'procedure_id': ['procedure_id', 'procedureid'],
            'procedure_name_en': ['procedure_name_en', 'procedurename_en', 'procname_en'],
            'procedure_name_ar': ['procedure_name_ar', 'procedurename_ar', 'procname_ar'],
            
            # Тип собственности
            'property_type_id': ['property_type_id', 'propertytypeid'],
            'property_type_en': ['property_type_en', 'propertytype_en'],
            'property_type_ar': ['property_type_ar', 'propertytype_ar'],
            
            # Подтип собственности
            'property_sub_type_id': ['property_sub_type_id', 'propertysubtypeid'],
            'property_sub_type_en': ['property_sub_type_en', 'propertysubtype_en'],
            'property_sub_type_ar': ['property_sub_type_ar', 'propertysubtype_ar'],
            
            # Использование
            'property_usage_en': ['property_usage_en', 'propertyusage_en'],
            'property_usage_ar': ['property_usage_ar', 'propertyusage_ar'],
            
            # Район
            'area_id': ['area_id', 'areaid'],
            'area_name_en': ['area_name_en', 'areaname_en'],
            'area_name_ar': ['area_name_ar', 'areaname_ar'],
            
            # Финансовые
            'trans_value': ['trans_value', 'transvalue', 'transaction_value'],
            'meter_sale_price': ['meter_sale_price', 'metersaleprice'],
            'actual_worth': ['actual_worth', 'actualworth'],
            'rent_value': ['rent_value', 'rentvalue'],
            'meter_rent_price': ['meter_rent_price', 'meterrentprice'],
            
            # Стороны сделки
            'no_of_parties_role_1': ['no_of_parties_role_1', 'nopartiesrole1'],
            'party_type_role_1_en': ['party_type_role_1_en', 'partytyperole1_en'],
            'party_type_role_1_ar': ['party_type_role_1_ar', 'partytyperole1_ar'],
            
            'no_of_parties_role_2': ['no_of_parties_role_2', 'nopartiesrole2'],
            'party_type_role_2_en': ['party_type_role_2_en', 'partytyperole2_en'],
            'party_type_role_2_ar': ['party_type_role_2_ar', 'partytyperole2_ar'],
            
            'no_of_parties_role_3': ['no_of_parties_role_3', 'nopartiesrole3'],
            
            # Проекты
            'master_project_en': ['master_project_en', 'masterproject_en'],
            'master_project_ar': ['master_project_ar', 'masterproject_ar'],
            'project_number': ['project_number', 'projectnumber'],
            'project_name_en': ['project_name_en', 'projectname_en'],
            'project_name_ar': ['project_name_ar', 'projectname_ar'],
            
            # Комнаты
            'rooms_en': ['rooms_en', 'rooms_en'],
            'rooms_ar': ['rooms_ar', 'rooms_ar'],
            
            # Парковка (обрабатываем оба варианта)
            'has_parking': ['has_parking', 'hasparking', 'parking'],
            
            # Ближайшие объекты
            'nearest_landmark_en': ['nearest_landmark_en', 'nearestlandmark_en'],
            'nearest_landmark_ar': ['nearest_landmark_ar', 'nearestlandmark_ar'],
            'nearest_metro_en': ['nearest_metro_en', 'nearestmetro_en'],
            'nearest_metro_ar': ['nearest_metro_ar', 'nearestmetro_ar'],
            'nearest_mall_en': ['nearest_mall_en', 'nearestmall_en'],
            'nearest_mall_ar': ['nearest_mall_ar', 'nearestmall_ar'],
            
            # Права
            'is_free_hold': ['is_free_hold', 'isfreehold'],
            
            # Регистрация
            'reg_type_id': ['reg_type_id', 'regtypeid'],
            'reg_type_en': ['reg_type_en', 'regtype_en'],
            'reg_type_ar': ['reg_type_ar', 'regtype_ar'],
            
            # Площади
            'procedure_area': ['procedure_area', 'procedurearea'],
            'building_name_en': ['building_name_en', 'buildingname_en'],
            'building_name_ar': ['building_name_ar', 'buildingname_ar'],
            
            # Старые поля для совместимости
            'trans_size_sqft': ['trans_size_sqft', 'transsizesqft'],
            'trans_size_sqm': ['trans_size_sqm', 'transsizesqm'],
            'actual_area_sqft': ['actual_area_sqft', 'actualareasqft'],
            'actual_area_sqm': ['actual_area_sqm', 'actualareasqm'],
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
            'trans_group_id': 0,
            'procedure_id': 0,
            'property_type_id': 0,
            'property_sub_type_id': 0,
            'area_id': 0,
            
            # Количественные
            'no_of_parties_role_1': 0,
            'no_of_parties_role_2': 0,
            'no_of_parties_role_3': 0,
            'project_number': 0,
            
            # Флаги
            'has_parking': 0,
            'is_free_hold': 0,
            'reg_type_id': 0,
            
            # Денежные значения
            'trans_value': 2,
            'meter_sale_price': 2,
            'actual_worth': 2,
            'rent_value': 2,
            'meter_rent_price': 2,
            
            # Площади
            'procedure_area': 2,
            'trans_size_sqft': 2,
            'trans_size_sqm': 2,
            'actual_area_sqft': 2,
            'actual_area_sqm': 2,
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
            'transaction_id': 100,
            'trans_group_en': 200,
            'trans_group_ar': 200,
            'procedure_name_en': 200,
            'procedure_name_ar': 200,
            'property_type_en': 50,
            'property_type_ar': 50,
            'property_sub_type_en': 100,
            'property_sub_type_ar': 100,
            'property_usage_en': 100,
            'property_usage_ar': 100,
            'area_name_en': 200,
            'area_name_ar': 200,
            'party_type_role_1_en': 100,
            'party_type_role_1_ar': 100,
            'party_type_role_2_en': 100,
            'party_type_role_2_ar': 100,
            'master_project_en': 200,
            'master_project_ar': 200,
            'project_name_en': 200,
            'project_name_ar': 200,
            'rooms_en': 200,
            'rooms_ar': 200,
            'nearest_landmark_en': 200,
            'nearest_landmark_ar': 200,
            'nearest_metro_en': 201,
            'nearest_metro_ar': 200,
            'nearest_mall_en': 203,
            'nearest_mall_ar': 202,
            'reg_type_en': 100,
            'reg_type_ar': 100,
            'building_name_en': 200,
            'building_name_ar': 200,
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
        if 'transaction_id' in df.columns:
            df = df.dropna(subset=['transaction_id'], how='any')
            removed_no_pk = initial_count - len(df)
            print(f"📊 Удалено записей без первичного ключа: {removed_no_pk}")
        else:
            print("❌ Критическая ошибка: отсутствует колонка transaction_id!")
            return
        
        # Удаляем дубликаты по первичному ключу
        df = df.drop_duplicates(subset=['transaction_id'], keep='first')
        removed_duplicates = initial_count - removed_no_pk - len(df)
        print(f"📊 Удалено дубликатов по PK: {removed_duplicates}")
        
        print(f"📊 После очистки осталось: {len(df)} записей")
        
        # Проверяем первые записи
        if len(df) > 0:
            print("\n🔍 Проверка примеров данных:")
            for i in range(min(3, len(df))):
                print(f"\nЗапись {i+1}:")
                row = df.iloc[i]
                sample_cols = ['transaction_id', 'instance_date', 'trans_group_en', 'property_type_en', 'trans_value']
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
                
                session.bulk_insert_mappings(Transaction, clean_batch)
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
                            transaction = Transaction(**record)
                            session.add(transaction)
                            session.commit()
                            inserted_count += 1
                            batch_inserted += 1
                        except Exception as e2:
                            session.rollback()
                            error_msg2 = str(e2)[:100]
                            # Если это ошибка дублирования, просто пропускаем
                            if "duplicate key" not in error_msg2.lower() and "unique violation" not in error_msg2.lower():
                                failed_records.append({
                                    'transaction_id': record.get('transaction_id'),
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
                print(f"    transaction_id={err['transaction_id']}: {err['error']}")
        
        # Проверяем результат
        count = session.query(Transaction).count()
        print(f"\n📊 Всего записей в таблице transactions: {count:,}")
        
        # Проверяем несколько записей из БД
        print("\n🔍 Проверка данных в БД:")
        if count > 0:
            test_records = session.query(Transaction).order_by(
                Transaction.instance_date
            ).limit(3).all()
            for rec in test_records:
                print(f"\n  transaction_id: {rec.transaction_id}")
                print(f"  instance_date: {rec.instance_date}")
                print(f"  trans_group_en: {rec.trans_group_en}")
                print(f"  trans_value: {rec.trans_value} (тип: {type(rec.trans_value).__name__})")
                print(f"  has_parking: {rec.has_parking}")
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
    migrate_transactions_final()