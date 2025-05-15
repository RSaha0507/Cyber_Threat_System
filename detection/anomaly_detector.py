import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

# PyOD models
from pyod.models.iforest import IForest # Isolation Forest
from pyod.models.knn import KNN # k-Nearest Neighbors
from pyod.models.lof import LOF # Local Outlier Factor
from pyod.models.copod import COPOD # Copula-based Outlier Detection
from pyod.models.hbos import HBOS # Histogram-based Outlier Score

def preprocess(df):
    df = df.copy()
    df['threat_level'] = df['threat_level'].str.lower()
    df['threat_level_code'] = df['threat_level'].map({
        'low': 1, 'medium': 2, 'high': 3, 'critical': 4
    })

    features = df[['category', 'threat_level_code']]

    preprocessor = ColumnTransformer(transformers=[
        ('cat', OneHotEncoder(), ['category']),
        ('num', StandardScaler(), ['threat_level_code']),
    ])

    X = preprocessor.fit_transform(features)
    return X, df


def detect_best_anomaly_model(df, model_choice="IForest"):
    if df.empty:
        return pd.DataFrame(), "None"

    # Preprocess data
    X, df_processed = preprocess(df)

    # Train-test split
    X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

    # Select model
    model_map = {
        "IForest": IForest(contamination=0.15, random_state=42),
        "KNN": KNN(),
        "LOF": LOF(),
        "COPOD": COPOD(),
        "HBOS": HBOS()
    }

    model_used = model_choice if model_choice in model_map else "IForest"
    model = model_map[model_used]

    model.fit(X_train)
    y_pred = model.predict(X)

    df_processed['is_anomaly'] = y_pred
    return df_processed[df_processed['is_anomaly'] == 1], model_used
