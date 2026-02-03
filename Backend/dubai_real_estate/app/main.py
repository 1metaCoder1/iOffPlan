from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database.connection import engine, Base

# Импортируем все роуты
from app.api.v1 import (
    lkp_areas,
    lkp_market_types,
    lkp_transaction_groups,
    lkp_transaction_procedures,
    valuation,
    units,
    buildings,
    projects,
    transactions,
)

# Создаем приложение
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем таблицы при старте
@app.on_event("startup")
async def startup_event():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

# Подключаем роуты
app.include_router(
    lkp_areas.router,
    prefix="/api/v1/lkp-areas",
    tags=["LKP Areas"]
)

app.include_router(
    lkp_market_types.router,
    prefix="/api/v1/lkp-market-types",
    tags=["LKP Market Types"]
)

app.include_router(
    lkp_transaction_groups.router,
    prefix="/api/v1/lkp-transaction-groups",
    tags=["LKP Transaction Groups"]
)

app.include_router(
    lkp_transaction_procedures.router,
    prefix="/api/v1/lkp-transaction-procedures",
    tags=["LKP Transaction Procedures"]
)

app.include_router(
    valuation.router,
    prefix="/api/v1/valuation",
    tags=["Valuation"]
)

app.include_router(
    units.router,
    prefix="/api/v1/units",
    tags=["Units"]
)

app.include_router(
    buildings.router,
    prefix="/api/v1/buildings",
    tags=["Buildings"]
)

app.include_router(
    projects.router,
    prefix="/api/v1/projects",
    tags=["Projects"]
)

app.include_router(
    transactions.router,
    prefix="/api/v1/transactions",
    tags=["Transactions"]
)

@app.get("/")
def root():
    return {
        "message": "Dubai Real Estate API",
        "docs": "/docs",
        "version": settings.VERSION
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
