import httpx
from .base import ExchangeInterface
from utils import get_symbol

class Binance(ExchangeInterface):
    async def get_price_volume(self, symbol: str):
        mapped_symbol = get_symbol("binance", symbol)  # 🔧 use mapped format: "BTCUSDT"
        url = f"https://api.binance.us/api/v3/ticker/24hr?symbol={mapped_symbol}"
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            j = r.json()

            # Safety check: Binance sometimes returns errors in JSON
            if "lastPrice" not in j or "quoteVolume" not in j:
                raise ValueError(f"Unexpected Binance response: {j}")

            return {
                "exchange": "binance",
                "price": float(j["lastPrice"]),
                "volume": float(j["quoteVolume"])
            }
