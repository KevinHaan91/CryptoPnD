import logging
import httpx
from .base import ExchangeInterface

logger = logging.getLogger("crypto_pump_detector.binance")

class Binance(ExchangeInterface):
    async def get_price_volume(self, symbol: str):
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            j = resp.json()

            if "lastPrice" not in j or "quoteVolume" not in j:
                logger.error(f"Binance API unexpected response for {symbol}: {j}")
                raise ValueError(f"Binance API response missing expected fields: {j}")

            price = float(j["lastPrice"])
            volume = float(j["quoteVolume"])

            logger.debug(f"Binance[{symbol}] price={price}, volume={volume}")
            return {"exchange": "binance", "price": price, "volume": volume}
