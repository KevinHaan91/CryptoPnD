import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv('mock_dataset.csv')

X = df[['price_change', 'volume_change', 'exchange']]
y = df['label']

preprocessor = ColumnTransformer(
    transformers=[
        ('exchange', OneHotEncoder(handle_unknown='ignore'), ['exchange'])
    ],
    remainder='passthrough'
)

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model.fit(X_train, y_train)

joblib.dump(model, 'model.pkl')
