import pandas as pd
from pathlib import Path

folder = r"C:\Users\User\Desktop\DubaiProject\datasets"

csv_files = [
    "Lkp_Areas.csv",
    "Valuation.csv",
    "Rent_Contracts.csv",
    "Units.csv",
    "Buildings.csv",
    "Projects.csv",
    "Lkp_Transaction_Groups.csv",
    "Transactions.csv",
    "Lkp_Transaction_Procedures.csv",
    "Lkp_Market_Types.csv"
]

for filename in csv_files:
    filepath = Path(folder) / filename
    if not filepath.exists():
        print(f"❌ Файл не найден: {filename}")
        continue

    try:
        # Читаем только первые 10 строк
        df = pd.read_csv(filepath, nrows=10, low_memory=False)
        
        print(f"\n{'='*100}")
        print(f"📄 ФАЙЛ: {filename}")
        print(f"Всего строк в файле: {pd.read_csv(filepath, usecols=[0]).shape[0]:,}")
        print(f"Колонок: {len(df.columns)}")
        print(f"Колонки: {list(df.columns)}")
        print(f"\nПервые 10 строк:")
        print(df.to_string(index=False))
        print(f"\nТипы колонок (dtypes):")
        print(df.dtypes)
        print(f"{'='*100}")
    except Exception as e:
        print(f"Ошибка чтения {filename}: {e}")