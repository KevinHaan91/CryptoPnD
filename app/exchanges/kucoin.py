import httpx
from .base import ExchangeInterface
from utils import get_symbol

class KuCoin(ExchangeInterface):
    async def get_price_volume(self, symbol: str):
        mapped_symbol = get_symbol("kucoin", symbol)  # 🧠 Use the mapped version
        url = f"https://api.kucoin.com/api/v1/market/stats?symbol={mapped_symbol}"
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            j = r.json()["data"]
            return {
                "exchange": "kucoin",
                "price": float(j["last"]),
                "volume": float(j["volValue"])
            }
