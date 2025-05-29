import httpx
from .base import ExchangeInterface

class KuCoin(ExchangeInterface):
    async def get_price_volume(self, symbol: str):
        url = f"https://api.kucoin.com/api/v1/market/stats?symbol={symbol}"
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            j = r.json()["data"]
            return {
                "exchange": "kucoin",
                "price": float(j["last"]),
                "volume": float(j["volValue"])
            }
