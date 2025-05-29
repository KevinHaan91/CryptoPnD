from fastapi import FastAPI
from exchanges.binance import Binance
from exchanges.kucoin import KuCoin
from exchanges.coingecko import CoinGecko
from detector import detect_pump
from model import predict_pump_score
import asyncio

app = FastAPI()

@app.get("/pump-score")
async def get_pump_score(symbol: str = "BTCUSDT"):
    binance = Binance()
    kucoin = KuCoin()
    gecko = CoinGecko()

    data = await asyncio.gather(
        binance.get_price_volume(symbol),
        kucoin.get_price_volume(symbol),
        gecko.get_price_volume(symbol)
    )

    pump_flags = [detect_pump(d) for d in data]
    score = predict_pump_score(data)

    return {"symbol": symbol, "data": data, "flags": pump_flags, "score": score}
