from fastapi import APIRouter
from app.services.market_data import get_nifty_price

router = APIRouter(prefix="/market", tags=["Market"])

@router.get("/nifty")
def nifty_price():
    return {"nifty": get_nifty_price()}
