from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OptionTrade(BaseModel):
    trade_id: int
    user_id: int
    symbol: str
    option_type: str      # CE / PE
    strike_price: float
    quantity: int
    entry_premium: float
    entry_time: datetime
    exit_premium: Optional[float] = None
    exit_time: Optional[datetime] = None
    status: str           # OPEN / CLOSED
