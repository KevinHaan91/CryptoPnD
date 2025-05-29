import httpx
from .base import ExchangeInterface
from utils import get_symbol

class CoinGecko(ExchangeInterface):
    async def get_price_volume(self, symbol: str):
        mapped_symbol = get_symbol("coingecko", symbol)  # 👈 Fix is here
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={mapped_symbol}&vs_currencies=usd&include_24hr_vol=true"
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            j = r.json()
            return {
                "exchange": "coingecko",
                "price": float(j[mapped_symbol]["usd"]),
                "volume": float(j[mapped_symbol]["usd_24h_vol"])
            }