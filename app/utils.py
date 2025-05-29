SYMBOL_MAP = {
    "BTCUSDT": {
        "binance": "BTCUSDT",
        "kucoin": "BTC-USDT",
        "coingecko": "bitcoin"
    }
}

def get_symbol(exchange: str, symbol: str):
    return SYMBOL_MAP.get(symbol, {}).get(exchange, symbol)
