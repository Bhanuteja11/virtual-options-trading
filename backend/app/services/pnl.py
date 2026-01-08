from app.services.market_data import get_nifty_price

def calculate_pnl(trade):
    current_price = get_nifty_price()
    current_premium = trade.premium
    pnl = (current_premium - trade.premium) * trade.quantity
    return {
        "current_nifty": current_price,
        "pnl": round(pnl, 2)
    }

