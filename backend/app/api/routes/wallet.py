from fastapi import APIRouter
from app.services.wallet import get_wallet

router = APIRouter(prefix="/wallet", tags=["Wallet"])

@router.get("/{user_id}")
def wallet_details(user_id: int):
    return get_wallet(user_id)
