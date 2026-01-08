from fastapi import APIRouter
from app.services.trading import (
    place_intraday_trade,
    square_off_trade,
    get_open_trades,
)

router = APIRouter(prefix="/intraday", tags=["Intraday"])

@router.post("/trade")
def intraday_trade(
    option_type: str,
    strike_price: float,
    quantity: int,
):
    return place_intraday_trade(
        user_id=1,
        option_type=option_type,
        strike_price=strike_price,
        quantity=quantity,
    )

@router.post("/square-off/{trade_id}")
def square_off(trade_id: int):
    return square_off_trade(trade_id)

@router.get("/open-trades")
def open_trades():
    return get_open_trades(user_id=1)

from app.services.trading import get_mtm_positions

@router.get("/mtm")
def mtm():
    return get_mtm_positions(user_id=1)
