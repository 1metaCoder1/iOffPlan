import logging
import asyncio
import requests
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ⚠️ ЗАМЕНИ ТОКЕН НА НОВЫЙ ИЗ @BotFather!
TOKEN = "7547158925:AAHp05LwF4h7ZSghSCK1g7G0kSWpsswH6gI"

# Твои API ключи от Dubai Pulse (получи как описано выше)
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"

# === НАСТРОЙКА ЛОГИРОВАНИЯ ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO  # можно изменить на DEBUG для ещё большей детализации
)
logger = logging.getLogger(__name__)

def get_access_token():
    url = "https://api.dubaipulse.gov.ae/oauth/client_credential/accesstoken?grant_type=client_credentials"
    data = {
        "client_id": API_KEY,
        "client_secret": API_SECRET
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Ошибка получения токена: {response.text}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Получена команда /start от пользователя: {user.id} (@{user.username})")
    await update.message.reply_text(f"Привет, {user.first_name}! Бот работает. Команды: /transactions [from_date] [limit], /properties [area_name] [property_type] [limit]")

async def get_transactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    from_date = args[0] if len(args) > 0 else None
    limit = int(args[1]) if len(args) > 1 else 10
    
    try:
        token = get_access_token()
        url = "https://api.dubaipulse.gov.ae/open/dld/dld_transactions-open-api"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"limit": limit, "order_by": "transaction_date desc"}
        if from_date:
            params["filter"] = f"transaction_date >= {from_date}"
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if not data:
                await update.message.reply_text("Нет данных по запросу.")
                return
            # Форматируем ответ (первые 3 поля для примера)
            msg = "Последние транзакции:\n"
            for item in data:
                msg += f"ID: {item.get('transaction_id', 'N/A')}, Дата: {item.get('transaction_date', 'N/A')}, Тип: {item.get('transaction_type_en', 'N/A')}\n"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text(f"Ошибка API: {response.text}")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text(f"Ошибка: {str(e)}")

async def get_properties(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    area_name = args[0] if len(args) > 0 else None
    property_type = args[1] if len(args) > 1 else None
    limit = int(args[2]) if len(args) > 2 else 10
    
    try:
        token = get_access_token()
        url = "https://api.dubaipulse.gov.ae/open/dld/dld_land_registry-open-api"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"limit": limit}
        filter_str = []
        if area_name:
            filter_str.append(f"area_name_en like '%{area_name}%'")
        if property_type:
            filter_str.append(f"property_type_en = '{property_type}'")
        if filter_str:
            params["filter"] = " and ".join(filter_str)
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if not data:
                await update.message.reply_text("Нет данных по запросу.")
                return
            msg = "Недвижимость:\n"
            for item in data:
                msg += f"ID: {item.get('property_id', 'N/A')}, Район: {item.get('area_name_en', 'N/A')}, Тип: {item.get('property_type_en', 'N/A')}, Площадь: {item.get('actual_area', 'N/A')}\n"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text(f"Ошибка API: {response.text}")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text(f"Ошибка: {str(e)}")

def main():
    logger.info("Инициализация бота...")
   
    try:
        application = Application.builder().token(TOKEN).build()
        logger.info("Application успешно создан.")
    except Exception as e:
        logger.error(f"Ошибка при создании Application: {e}")
        return
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("transactions", get_transactions))
    application.add_handler(CommandHandler("properties", get_properties))
    logger.info("Обработчики зарегистрированы.")
    
    logger.info("Запуск long polling...")
    print("✅ Бот запущен. Отправь ему /start в Telegram.")
    print("Логи будут появляться в консоли.")
    
    try:
        application.run_polling()
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем (Ctrl+C).")
    except Exception as e:
        logger.exception(f"Критическая ошибка при запуске polling: {e}")

if __name__ == '__main__':
    main()