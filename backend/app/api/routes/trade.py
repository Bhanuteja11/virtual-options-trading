from fastapi import APIRouter
from app.services.trading import place_trade

router = APIRouter(prefix="/trade", tags=["Trade"])

@router.post("/")
def execute_trade():
    return place_trade(
        user_id=1,
        symbol="NIFTY",
        option_type="CE",
        strike_price=22000,
        quantity=50,
        premium=120
    )
