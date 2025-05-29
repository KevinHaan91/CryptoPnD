import httpx
from .base import ExchangeInterface

class Binance(ExchangeInterface):
    async def get_price_volume(self, symbol: str):
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            j = r.json()
            return {
                "exchange": "binance",
                "price": float(j["lastPrice"]),
                "volume": float(j["quoteVolume"])
            }
