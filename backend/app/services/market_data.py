import random
import time
import yfinance as yf

UPDATE_INTERVAL = 3  # seconds
LAST_UPDATED = 0

def fetch_delayed_nifty():
    try:
        nifty = yf.Ticker("^NSEI")
        data = nifty.history(period="1d")
        if not data.empty:
            return float(data["Close"].iloc[-1])
    except Exception:
        pass
    return None


# Initialize with delayed real NIFTY value
NIFTY_PRICE = fetch_delayed_nifty() or 26140.75


def get_nifty_price():
    global NIFTY_PRICE, LAST_UPDATED

    now = time.time()

    # Update simulated tick only on interval
    if now - LAST_UPDATED >= UPDATE_INTERVAL:
        movement = random.uniform(-5, 5)
        NIFTY_PRICE += movement
        LAST_UPDATED = now

    return round(NIFTY_PRICE, 2)
