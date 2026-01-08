from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router

from app.api.routes.wallet import router as wallet_router
from app.api.routes.market import router as market_router
from app.api.routes.meta import router as meta_router
from app.core.config import settings
from app.api.routes.intraday import router as intraday_router


# ✅ 1. Create app FIRST
app = FastAPI(
    title=settings.app_name,
    version="0.1.0"
)

# ✅ 2. THEN add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 3. THEN include routers
app.include_router(health_router)
app.include_router(wallet_router)
app.include_router(market_router)
app.include_router(meta_router)
app.include_router(intraday_router)
