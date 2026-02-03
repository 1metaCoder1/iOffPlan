import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import (
    Application, CommandHandler, ContextTypes, 
    MessageHandler, filters, ConversationHandler
)
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# ⚠️ ЗАМЕНИ НА СВОЙ ТОКЕН!
BOT_TOKEN = "7547158925:AAHp05LwF4h7ZSghSCK1g7G0kSWpsswH6gI"

# Настройки базы данных
DB_URL = "postgresql://user:password@localhost:5432/real_estate"

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
(
    SELECTING_PROPERTY_TYPE, ENTERING_LOCATION, ENTERING_AREA, 
    ENTERING_BEDROOMS, ENTERING_BATHROOMS, ENTERING_PRICE,
    ENTERING_AMENITIES, ENTERING_DESCRIPTION, 
    ENTERING_NAME, ENTERING_PHONE, ENTERING_EMAIL,
    CONFIRMING
) = range(12)

# Инициализация базы данных
Base = declarative_base()

class PropertyListing(Base):
    __tablename__ = 'property_listings'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    property_type = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)
    area_sqm = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
    amenities = Column(Text)
    description = Column(Text)
    
    seller_name = Column(String(100), nullable=False)
    seller_phone = Column(String(20), nullable=False)
    seller_email = Column(String(100))
    is_verified = Column(Boolean, default=False)

# Создание таблиц
engine = create_engine(DB_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Главное меню
MAIN_MENU_KEYBOARD = [
    ["📝 Заполнить форму продавца"],
    ["📊 Посмотреть последние объявления"]
]
MAIN_MENU_MARKUP = ReplyKeyboardMarkup(MAIN_MENU_KEYBOARD, resize_keyboard=True, one_time_keyboard=True)

# Типы недвижимости
PROPERTY_TYPES = [
    "🏙️ Апартаменты",
    "🏡 Вилла",
    "🏘️ Таунхаус",
    "🏢 Офис",
    "🏪 Магазин",
    "🏭 Промышленное помещение"
]
PROPERTY_TYPE_MARKUP = ReplyKeyboardMarkup(
    [PROPERTY_TYPES[i:i+2] for i in range(0, len(PROPERTY_TYPES), 2)],
    resize_keyboard=True,
    one_time_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начальное сообщение с главным меню"""
    await update.message.reply_text(
        "👋 Добро пожаловать в бота по продаже недвижимости в Дубае!\n\n"
        "Выберите действие:",
        reply_markup=MAIN_MENU_MARKUP
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена текущей операции"""
    await update.message.reply_text(
        "❌ Операция отменена.\n\nВыберите действие:",
        reply_markup=MAIN_MENU_MARKUP
    )
    return ConversationHandler.END

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать главное меню"""
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=MAIN_MENU_MARKUP
    )
    return ConversationHandler.END

async def start_seller_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало формы для продавца"""
    await update.message.reply_text(
        "🏠 Давайте заполним форму для вашего объявления о продаже недвижимости.\n\n"
        "Шаг 1: Выберите тип недвижимости:",
        reply_markup=PROPERTY_TYPE_MARKUP
    )
    return SELECTING_PROPERTY_TYPE

async def select_property_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выбор типа недвижимости"""
    property_type = update.message.text.replace('🏙️ ', '').replace('🏡 ', '').replace('🏘️ ', '').replace('🏢 ', '').replace('🏪 ', '').replace('🏭 ', '')
    context.user_data['property_type'] = property_type
    
    await update.message.reply_text(
        f"✅ Тип недвижимости: {property_type}\n\n"
        "Шаг 2: Укажите локацию (район/локация в Дубае):",
        reply_markup=ReplyKeyboardRemove()
    )
    return ENTERING_LOCATION

async def enter_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ввод локации"""
    location = update.message.text.strip()
    if len(location) < 3:
        await update.message.reply_text("❌ Локация должна быть минимум 3 символа. Попробуйте еще раз:")
        return ENTERING_LOCATION
        
    context.user_data['location'] = location
    
    await update.message.reply_text(
        f"✅ Локация: {location}\n\n"
        "Шаг 3: Укажите площадь в кв.м (например, 120.5):"
    )
    return ENTERING_AREA

async def enter_area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ввод площади"""
    try:
        area = float(update.message.text.strip())
        if area <= 0:
            raise ValueError
        context.user_data['area_sqm'] = area
        
        await update.message.reply_text(
            f"✅ Площадь: {area} кв.м\n\n"
            "Шаг 4: Укажите количество спален (целое число):"
        )
        return ENTERING_BEDROOMS
    except ValueError:
        await update.message.reply_text("❌ Пожалуйста, введите корректное число для площади (например, 120.5):")
        return ENTERING_AREA

async def enter_bedrooms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ввод количества спален"""
    try:
        bedrooms = int(update.message.text.strip())
        if bedrooms < 0:
            raise ValueError
        context.user_data['bedrooms'] = bedrooms
        
        await update.message.reply_text(
            f"✅ Спален: {bedrooms}\n\n"
            "Шаг 5: Укажите количество ванных комнат (целое число):"
        )
        return ENTERING_BATHROOMS
    except ValueError:
        await update.message.reply_text("❌ Пожалуйста, введите целое число для количества спален:")
        return ENTERING_BEDROOMS

async def enter_bathrooms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ввод количества ванных комнат"""
    try:
        bathrooms = int(update.message.text.strip())
        if bathrooms < 0:
            raise ValueError
        context.user_data['bathrooms'] = bathrooms
        
        await update.message.reply_text(
            f"✅ Ванных комнат: {bathrooms}\n\n"
            "Шаг 6: Укажите цену в AED (например, 1500000):"
        )
        return ENTERING_PRICE
    except ValueError:
        await update.message.reply_text("❌ Пожалуйста, введите целое число для количества ванных комнат:")
        return ENTERING_BATHROOMS

async def enter_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ввод цены"""
    try:
        price = float(update.message.text.strip().replace(',', ''))
        if price <= 0:
            raise ValueError
        context.user_data['price'] = price
        
        await update.message.reply_text(
            f"✅ Цена: {price:,.0f} AED\n\n"
            "Шаг 7: Укажите удобства через запятую (например: бассейн, парковка, кондиционер):"
        )
        return ENTERING_AMENITIES
    except ValueError:
        await update.message.reply_text("❌ Пожалуйста, введите корректную цену (например, 1500000):")
        return ENTERING_PRICE

async def enter_amenities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ввод удобств"""
    amenities = update.message.text.strip()
    context.user_data['amenities'] = amenities
    
    await update.message.reply_text(
        f"✅ Удобства: {amenities}\n\n"
        "Шаг 8: Напишите описание недвижимости (минимум 10 слов):"
    )
    return ENTERING_DESCRIPTION

async def enter_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ввод описания"""
    description = update.message.text.strip()
    if len(description.split()) < 10:
        await update.message.reply_text("❌ Описание должно быть минимум 10 слов. Попробуйте еще раз:")
        return ENTERING_DESCRIPTION
        
    context.user_data['description'] = description
    
    await update.message.reply_text(
        f"✅ Описание сохранено!\n\n"
        "Шаг 9: Введите ваше имя (как продавца):"
    )
    return ENTERING_NAME

async def enter_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ввод имени продавца"""
    name = update.message.text.strip()
    if len(name) < 2:
        await update.message.reply_text("❌ Имя должно быть минимум 2 символа. Попробуйте еще раз:")
        return ENTERING_NAME
        
    context.user_data['seller_name'] = name
    
    await update.message.reply_text(
        f"✅ Имя: {name}\n\n"
        "Шаг 10: Введите ваш телефон для связи (например, +971 50 123 4567):"
    )
    return ENTERING_PHONE

async def enter_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ввод телефона"""
    phone = update.message.text.strip()
    if len(phone) < 8:
        await update.message.reply_text("❌ Телефон должен быть минимум 8 символов. Попробуйте еще раз:")
        return ENTERING_PHONE
        
    context.user_data['seller_phone'] = phone
    
    await update.message.reply_text(
        f"✅ Телефон: {phone}\n\n"
        "Шаг 11 (опционально): Введите ваш email для связи:"
    )
    return ENTERING_EMAIL

async def enter_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ввод email"""
    email = update.message.text.strip()
    if '@' not in email and email != 'пропустить':
        await update.message.reply_text(
            "❌ Некорректный email. Введите корректный email или напишите 'пропустить':"
        )
        return ENTERING_EMAIL
    
    context.user_data['seller_email'] = email if email != 'пропустить' else None
    
    # Подготовка данных для подтверждения
    data = context.user_data
    
    confirmation_text = (
        "📋 Пожалуйста, проверьте введенные данные:\n\n"
        f"🏠 Тип недвижимости: {data['property_type']}\n"
        f"📍 Локация: {data['location']}\n"
        f"📏 Площадь: {data['area_sqm']} кв.м\n"
        f"🛏️ Спален: {data['bedrooms']}\n"
        f"🚿 Ванных комнат: {data['bathrooms']}\n"
        f"💰 Цена: {data['price']:,.0f} AED\n"
        f"⭐ Удобства: {data['amenities']}\n"
        f"📝 Описание: {data['description'][:100]}...\n\n"
        f"👤 Имя продавца: {data['seller_name']}\n"
        f"📱 Телефон: {data['seller_phone']}\n"
        f"📧 Email: {data.get('seller_email', 'не указан')}\n\n"
        "✅ Все верно? Отправьте 'да' для подтверждения или 'нет' для отмены."
    )
    
    await update.message.reply_text(confirmation_text)
    return CONFIRMING

async def confirm_listing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подтверждение и сохранение объявления"""
    if update.message.text.lower() not in ['да', 'yes']:
        await update.message.reply_text(
            "❌ Объявление не сохранено.\n\nВыберите действие:",
            reply_markup=MAIN_MENU_MARKUP
        )
        context.user_data.clear()
        return ConversationHandler.END
    
    # Сохранение в базу данных
    try:
        session = Session()
        listing = PropertyListing(
            property_type=context.user_data['property_type'],
            location=context.user_data['location'],
            area_sqm=context.user_data['area_sqm'],
            bedrooms=context.user_data['bedrooms'],
            bathrooms=context.user_data['bathrooms'],
            price=context.user_data['price'],
            amenities=context.user_data['amenities'],
            description=context.user_data['description'],
            seller_name=context.user_data['seller_name'],
            seller_phone=context.user_data['seller_phone'],
            seller_email=context.user_data.get('seller_email')
        )
        session.add(listing)
        session.commit()
        
        listing_id = listing.id
        session.close()
        
        await update.message.reply_text(
            f"🎉 Отлично! Ваше объявление успешно сохранено!\n\n"
            f"🆔 ID вашего объявления: {listing_id}\n\n"
            "Наши менеджеры свяжутся с вами для подтверждения деталей.\n\n"
            "Выберите следующее действие:",
            reply_markup=MAIN_MENU_MARKUP
        )
        
        # Очистка данных пользователя
        context.user_data.clear()
        return ConversationHandler.END
        
    except Exception as e:
        logger.error(f"Ошибка при сохранении в БД: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при сохранении объявления. Попробуйте еще раз позже.",
            reply_markup=MAIN_MENU_MARKUP
        )
        context.user_data.clear()
        return ConversationHandler.END

async def show_latest_listings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ последних объявлений"""
    try:
        session = Session()
        listings = session.query(PropertyListing).order_by(PropertyListing.created_at.desc()).limit(5).all()
        session.close()
        
        if not listings:
            await update.message.reply_text(
                "📭 Пока нет объявлений. Будьте первым, кто разместит объявление!",
                reply_markup=MAIN_MENU_MARKUP
            )
            return
            
        response = "📊 Последние объявления о продаже недвижимости:\n\n"
        
        for i, listing in enumerate(listings, 1):
            response += (
                f"{i}. 🏠 {listing.property_type} в {listing.location}\n"
                f"   📏 {listing.area_sqm} кв.м | 🛏️ {listing.bedrooms} сп. | 🚿 {listing.bathrooms} ван.\n"
                f"   💰 {listing.price:,.0f} AED\n"
                f"   📞 {listing.seller_phone}\n"
                f"   ──────────────────────\n"
            )
        
        response += "\nВыберите действие:"
        await update.message.reply_text(response, reply_markup=MAIN_MENU_MARKUP)
        
    except Exception as e:
        logger.error(f"Ошибка при получении объявлений: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при получении объявлений. Попробуйте позже.",
            reply_markup=MAIN_MENU_MARKUP
        )

def main():
    """Основная функция запуска бота"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # ConversationHandler для формы продавца
    seller_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^📝 Заполнить форму продавца$"), start_seller_form)],
        states={
            SELECTING_PROPERTY_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, select_property_type)],
            ENTERING_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_location)],
            ENTERING_AREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_area)],
            ENTERING_BEDROOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_bedrooms)],
            ENTERING_BATHROOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_bathrooms)],
            ENTERING_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_price)],
            ENTERING_AMENITIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_amenities)],
            ENTERING_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_description)],
            ENTERING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_name)],
            ENTERING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_phone)],
            ENTERING_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_email)],
            CONFIRMING: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_listing)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", show_menu))
    application.add_handler(CommandHandler("cancel", cancel))
    
    # Обработчики меню
    application.add_handler(seller_conv_handler)
    application.add_handler(MessageHandler(filters.Regex("^📊 Посмотреть последние объявления$"), show_latest_listings))
    application.add_handler(MessageHandler(filters.Regex("^📝 Заполнить форму продавца$"), start_seller_form))
    
    logger.info("✅ Бот запущен!")
    print("✅ Бот запущен. Отправьте /start для начала работы.")
    
    application.run_polling()

if __name__ == '__main__':
    main()