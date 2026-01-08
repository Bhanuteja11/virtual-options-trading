from app.models.wallet import Wallet

WALLETS = {
    1: Wallet(user_id=1)
}

def get_wallet(user_id: int) -> Wallet:
    return WALLETS[user_id]

def debit_wallet(user_id: int, amount: float):
    wallet = get_wallet(user_id)
    if wallet.balance < amount:
        raise ValueError("Insufficient balance")
    wallet.balance -= amount

def credit_wallet(user_id: int, amount: float):
    wallet = get_wallet(user_id)
    wallet.balance += amount
