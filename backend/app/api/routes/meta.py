from fastapi import APIRouter

router = APIRouter(prefix="/meta", tags=["Meta"])

@router.get("/info")
def system_info():
    return {
        "market_data": "Delayed index data / simulated feed",
        "trading": "Paper trading only",
        "capital": "Virtual money"
    }
