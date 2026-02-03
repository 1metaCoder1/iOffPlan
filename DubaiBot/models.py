from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PropertyListing(Base):
    __tablename__ = 'property_listings'
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Основные поля недвижимости
    property_type = Column(String(50), nullable=False)  # apartment, villa, townhouse
    location = Column(String(100), nullable=False)     # район/локация
    area_sqm = Column(Float, nullable=False)           # площадь в кв.м
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)              # цена в AED
    
    # Дополнительные характеристики
    amenities = Column(Text)                           # удобства через запятую
    description = Column(Text)                         # описание
    
    # Контактные данные продавца
    seller_name = Column(String(100), nullable=False)
    seller_phone = Column(String(20), nullable=False)
    seller_email = Column(String(100))
    is_verified = Column(Boolean, default=False)      # подтверждено ли объявление
    
    def __repr__(self):
        return f"<PropertyListing {self.id}: {self.property_type} in {self.location}>"