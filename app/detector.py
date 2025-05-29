PUMP_PRICE_DELTA = 0.1
PUMP_VOLUME_DELTA = 2.0

def detect_pump(data):
    price = data["price"]
    volume = data["volume"]
    return price > 0 and volume > 0
