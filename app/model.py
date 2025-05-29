import joblib
import os

model = joblib.load(os.path.join(os.path.dirname(__file__), 'model_training/model.pkl'))

def predict_pump_score(data):
    features = []
    for entry in data:
        price = entry['price']
        volume = entry['volume']
        exchange = entry['exchange']
        features.append({
            'price_change': price / 100,  # mock change
            'volume_change': volume / 1000000,  # normalize mock
            'exchange': exchange
        })
    import pandas as pd
    df = pd.DataFrame(features)
    preds = model.predict_proba(df)[:, 1]
    return round(float(preds.mean()), 2)
