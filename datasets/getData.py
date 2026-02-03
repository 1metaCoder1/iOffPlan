import pandas as pd
from sqlalchemy import create_engine, text
from tabulate import tabulate

# ==================== НАСТРОЙКИ ====================
DB_USER = "user"
DB_PASS = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "real_estate"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True
)

tables = [
    "lkp_areas",
    "lkp_market_types",
    "lkp_transaction_groups",
    "lkp_transaction_procedures",
    "valuation",
    "rent_contracts",
    "units",
    "buildings",
    "projects",
    "transactions"
]

def inspect_table(table_name):
    print(f"\n{'='*120}")
    print(f"📋 ТАБЛИЦА: {table_name.upper()}")
    print(f"{'='*120}")

    try:
        # 1. Структура колонок
        query_columns = text("""
            SELECT 
                column_name,
                data_type,
                is_nullable,
                character_maximum_length,
                numeric_precision,
                numeric_scale
            FROM information_schema.columns 
            WHERE table_name = :table_name
            ORDER BY ordinal_position;
        """)
        
        df_columns = pd.read_sql(query_columns, engine, params={"table_name": table_name})
        
        print("\nСтруктура колонок:")
        print(tabulate(df_columns, headers='keys', tablefmt='pretty', showindex=False))

        # 2. Первые 5 записей
        query_data = text(f"SELECT * FROM {table_name} LIMIT 5")
        df_data = pd.read_sql(query_data, engine)

        print(f"\nПервые 5 записей ({len(df_data)} строк):")
        if len(df_data) > 0:
            print(tabulate(df_data, headers='keys', tablefmt='pretty', showindex=False))
        else:
            print("Таблица пуста.")

        # Количество строк в таблице
        count = pd.read_sql(text(f"SELECT COUNT(*) as total FROM {table_name}"), engine).iloc[0]['total']
        print(f"\nВсего строк в таблице: {count:,}")

    except Exception as e:
        print(f"❌ Ошибка при работе с таблицей {table_name}: {e}")

# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    print("🔍 Начинаем анализ всех таблиц...\n")
    for table in tables:
        inspect_table(table)
        print("\n" + "-"*80)
    
    print("\n✅ Анализ всех таблиц завершён!")