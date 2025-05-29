import pandas as pd
import random

def generate_mock_data(n=200):
    data = []
    for _ in range(n):
        price_change = random.uniform(-0.3, 0.5)
        volume_change = random.uniform(-1.0, 4.0)
        exchange = random.choice(['binance', 'kucoin', 'coingecko'])
        label = 1 if price_change > 0.2 and volume_change > 1.5 else 0
        data.append({
            'price_change': price_change,
            'volume_change': volume_change,
            'exchange': exchange,
            'label': label
        })
    return pd.DataFrame(data)

if __name__ == '__main__':
    df = generate_mock_data()
    df.to_csv("mock_dataset.csv", index=False)
