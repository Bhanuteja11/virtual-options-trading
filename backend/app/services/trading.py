from datetime import datetime
from fastapi import HTTPException

from app.models.trade import OptionTrade
from app.services.wallet import debit_wallet, credit_wallet
from app.services.pricing import calculate_option_premium
from app.services.market_data import get_nifty_price

TRADES = []


def place_intraday_trade(
    user_id: int,
    option_type: str,
    strike_price: float,
    quantity: int
):
    spot = get_nifty_price()
    premium = calculate_option_premium(spot, strike_price, option_type)
    cost = premium * quantity

    debit_wallet(user_id, cost)

    trade = OptionTrade(
        trade_id=len(TRADES) + 1,
        user_id=user_id,
        symbol="NIFTY",
        option_type=option_type,
        strike_price=strike_price,
        quantity=quantity,
        entry_premium=premium,
        entry_time=datetime.utcnow(),
        status="OPEN"
    )
    TRADES.append(trade)
    return trade


def square_off_trade(trade_id: int):
    trade = next(
        (t for t in TRADES if t.trade_id == trade_id and t.status == "OPEN"),
        None
    )

    if not trade:
        raise HTTPException(
            status_code=404,
            detail="Open trade not found"
        )

    spot = get_nifty_price()
    exit_premium = calculate_option_premium(
        spot, trade.strike_price, trade.option_type
    )

    pnl = (exit_premium - trade.entry_premium) * trade.quantity

    trade.exit_premium = exit_premium
    trade.exit_time = datetime.utcnow()
    trade.status = "CLOSED"

    credit_wallet(trade.user_id, exit_premium * trade.quantity)

    return {
        "trade_id": trade.trade_id,
        "pnl": round(pnl, 2),
        "exit_premium": exit_premium
    }


def get_open_trades(user_id: int):
    return [t for t in TRADES if t.user_id == user_id and t.status == "OPEN"]


def get_mtm_positions(user_id: int):
    spot = get_nifty_price()
    positions = []

    for trade in TRADES:
        if trade.user_id == user_id and trade.status == "OPEN":
            current_premium = calculate_option_premium(
                spot,
                trade.strike_price,
                trade.option_type
            )
            pnl = (current_premium - trade.entry_premium) * trade.quantity

            positions.append({
                "trade_id": trade.trade_id,
                "option_type": trade.option_type,
                "strike_price": trade.strike_price,
                "quantity": trade.quantity,
                "entry_premium": trade.entry_premium,
                "current_premium": current_premium,
                "pnl": round(pnl, 2),
            })

    return {
        "spot": spot,
        "positions": positions,
        "total_mtm": round(sum(p["pnl"] for p in positions), 2),
    }
