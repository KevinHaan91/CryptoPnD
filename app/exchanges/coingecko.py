import httpx
from .base import ExchangeInterface

class CoinGecko(ExchangeInterface):
    async def get_price_volume(self, symbol: str):
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd&include_24hr_vol=true"
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            j = r.json()[symbol]
            return {
                "exchange": "coingecko",
                "price": float(j["usd"]),
                "volume": float(j["usd_24h_vol"])
            }
