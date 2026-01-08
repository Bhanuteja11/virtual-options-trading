from pydantic import BaseModel

class Wallet(BaseModel):
    user_id: int
    balance: float = 1_000_000.0
    realized_pnl: float = 0.0
