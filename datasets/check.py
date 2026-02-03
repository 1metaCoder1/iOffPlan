import pandas as pd
from sqlalchemy import create_engine, text

# ==================== НАСТРОЙКИ ПОДКЛЮЧЕНИЯ ====================
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

def show_columns_simple(table_name):
    query = text("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = :table_name
        ORDER BY ordinal_position;
    """)
    df = pd.read_sql(query, engine, params={"table_name": table_name})
    print(f"\n--- {table_name.upper()} ---")
    for _, row in df.iterrows():
        print(f"{row['column_name']:<30} | {row['data_type']}")

if __name__ == "__main__":
    print("📋 Структура таблиц (колонка | тип данных):\n")
    for table in tables:
        show_columns_simple(table)