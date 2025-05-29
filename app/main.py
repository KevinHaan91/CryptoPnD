import os
import asyncio
import logging
from fastapi import FastAPI, HTTPException
#from exchanges.binance import Binance
from exchanges.kucoin import KuCoin
from exchanges.coingecko import CoinGecko
from detector import detect_pump
from model import predict_pump_score

# Configure root logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crypto_pump_detector")

app = FastAPI()

@app.get("/pump-score")
async def get_pump_score(symbol: str = "BTCUSDT"):
    logger.info(f"Received request for symbol={symbol}")
    try:
        #binance = Binance()
        kucoin = KuCoin()
        gecko = CoinGecko()

        # Fire off all three fetches in parallel
        data = await asyncio.gather(
           # binance.get_price_volume(symbol),
            kucoin.get_price_volume(symbol),
            gecko.get_price_volume(symbol),
            return_exceptions=True
        )

        # Check for any fetch errors
        clean_data = []
        for idx, result in enumerate(data):
            if isinstance(result, Exception):
                logger.error(f"Error fetching from exchange #{idx}: {result}", exc_info=True)
            else:
                clean_data.append(result)

        if not clean_data:
            raise HTTPException(status_code=502, detail="No exchange data available")

        # Detection & scoring
        pump_flags = [detect_pump(d) for d in clean_data]
        score = predict_pump_score(clean_data)

        response = {"symbol": symbol, "data": clean_data, "flags": pump_flags, "score": score}
        logger.info(f"Responding: {response}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in /pump-score: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
