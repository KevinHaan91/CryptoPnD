import os
import asyncio
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from exchanges.binance import Binance
from exchanges.kucoin import KuCoin
from exchanges.coingecko import CoinGecko
from detector import detect_pump
from model import predict_pump_score

# Configure root logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crypto_pump_detector")

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SymbolsRequest(BaseModel):
    symbols: list[str]

async def get_data_staggered(symbol: str):
    binance = Binance()
    kucoin = KuCoin()
    coingecko = CoinGecko()

    result = []

    try:
        result.append(await binance.get_price_volume(symbol))
        await asyncio.sleep(0.2)
    except Exception as e:
        logger.error(f"Binance error for {symbol}: {e}", exc_info=True)

    try:
        result.append(await kucoin.get_price_volume(symbol))
        await asyncio.sleep(0.2)
    except Exception as e:
        logger.error(f"KuCoin error for {symbol}: {e}", exc_info=True)

    try:
        result.append(await coingecko.get_price_volume(symbol))
        await asyncio.sleep(0.2)
    except Exception as e:
        logger.error(f"CoinGecko error for {symbol}: {e}", exc_info=True)

    return result

@app.get("/pump-score")
async def get_pump_score(symbol: str = "BTCUSDT"):
    logger.info(f"Received request for symbol={symbol}")
    try:
        data = await get_data_staggered(symbol)

        if not data:
            raise HTTPException(status_code=502, detail="No exchange data available")

        pump_flags = [detect_pump(d) for d in data]
        score = predict_pump_score(data)

        response = {"symbol": symbol, "data": data, "flags": pump_flags, "score": score}
        logger.info(f"Responding: {response}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in /pump-score: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pump-scores")
async def get_bulk_scores(req: SymbolsRequest):
    logger.info(f"Bulk request for {len(req.symbols)} symbols")
    results = []

    for symbol in req.symbols:
        try:
            data = await get_data_staggered(symbol)
            if not data:
                continue

            pump_flags = [detect_pump(d) for d in data]
            score = predict_pump_score(data)

            results.append({
                "symbol": symbol,
                "data": data,
                "flags": pump_flags,
                "score": score
            })

        except Exception as e:
            logger.error(f"Error processing {symbol}: {e}", exc_info=True)

    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)