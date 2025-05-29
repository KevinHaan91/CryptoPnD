class ExchangeInterface:
    async def get_price_volume(self, symbol: str):
        raise NotImplementedError
