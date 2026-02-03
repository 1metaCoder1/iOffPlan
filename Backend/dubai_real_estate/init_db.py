import sys
import os

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.connection import engine, Base
from app.database.models import *

if __name__ == "__main__":
    try:
        # Создаем все таблицы
        Base.metadata.create_all(bind=engine)
        print("✅ Все таблицы успешно созданы!")
    except Exception as e:
        print(f"❌ Ошибка при создании таблиц: {e}")