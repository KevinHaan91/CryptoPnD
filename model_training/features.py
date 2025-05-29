from sklearn.preprocessing import OneHotEncoder
import pandas as pd

def preprocess(df):
    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
    encoded = encoder.fit_transform(df[['exchange']])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(['exchange']))
    return pd.concat([df[['price_change', 'volume_change']], encoded_df], axis=1), df['label']
