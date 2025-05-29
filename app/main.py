import os
import asyncio
import logging
from fastapi import FastAPI, HTTPException
from exchanges.binance import Binance
from exchanges.kucoin import KuCoin
from exchanges.coingecko import CoinGecko
from detector import detect_pump
from model import predict_pump_score
from fastapi.middleware.cors import CORSMiddleware

# Configure root logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crypto_pump_detector")

app = FastAPI()
 # Add CORS middleware here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify ["https://cryptopnd.vercel.app"] for stricter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Pydantic model for bulk input
class SymbolsRequest(BaseModel):
    symbols: list[str]


@app.get("/pump-score")
async def get_pump_score(symbol: str = "BTCUSDT"):
    logger.info(f"Received request for symbol={symbol}")
    try:
        binance = Binance()
        kucoin = KuCoin()
        gecko = CoinGecko()

        data = await asyncio.gather(
            binance.get_price_volume(symbol),
            kucoin.get_price_volume(symbol),
            gecko.get_price_volume(symbol),
            return_exceptions=True
        )

        clean_data = []
        for idx, result in enumerate(data):
            if isinstance(result, Exception):
                logger.error(f"Error fetching from exchange #{idx}: {result}", exc_info=True)
            else:
                clean_data.append(result)

        if not clean_data:
            raise HTTPException(status_code=502, detail="No exchange data available")

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


@app.post("/pump-scores")
async def get_bulk_scores(req: SymbolsRequest):
    logger.info(f"Bulk request for {len(req.symbols)} symbols")

    binance = Binance()
    kucoin = KuCoin()
    gecko = CoinGecko()

    results = []

    for symbol in req.symbols:
        try:
            data = await asyncio.gather(
                binance.get_price_volume(symbol),
                kucoin.get_price_volume(symbol),
                gecko.get_price_volume(symbol),
                return_exceptions=True
            )

            clean_data = [d for d in data if not isinstance(d, Exception)]
            if not clean_data:
                continue

            flags = [detect_pump(d) for d in clean_data]
            score = predict_pump_score(clean_data)

            results.append({
                "symbol": symbol,
                "data": clean_data,
                "flags": flags,
                "score": score
            })
        except Exception as e:
            logger.error(f"Error scoring symbol {symbol}: {e}", exc_info=True)

    return results


# Optional entry point for local dev
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)