"""
Traffic Accident Analysis System — ML Prediction Module
Simple RandomForest classifier to predict accident severity.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score


class AccidentPredictor:
    """Predicts accident severity based on contextual features."""

    FEATURE_COLS = ["Hour", "Weather", "Location", "Vehicle_Type", "Cause"]

    def __init__(self):
        self.model = None
        self.encoders = {}
        self.feature_importance = {}
        self.accuracy = None
        self.classes = []

    def train(self, df):
        """Train the model on the given dataframe.
        Returns True if training succeeded, False otherwise.
        """
        if "Severity" not in df.columns:
            return False

        # Determine which feature columns are available
        available = [c for c in self.FEATURE_COLS if c in df.columns]
        if len(available) < 2:
            return False

        # Prepare features
        X = df[available].copy()
        y = df["Severity"].copy()

        # Drop rows with any NaN in features or target
        mask = X.notna().all(axis=1) & y.notna()
        X = X[mask]
        y = y[mask]

        if len(X) < 10:
            return False

        # Encode categorical features
        self.encoders = {}
        for col in available:
            if X[col].dtype == "object":
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                self.encoders[col] = le

        # Encode target
        self.target_encoder = LabelEncoder()
        y_encoded = self.target_encoder.fit_transform(y)
        self.classes = list(self.target_encoder.classes_)

        # Train
        self.model = RandomForestClassifier(
            n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
        )
        self.model.fit(X, y_encoded)

        # Cross-validation accuracy
        try:
            scores = cross_val_score(self.model, X, y_encoded, cv=min(5, len(X) // 2), scoring="accuracy")
            self.accuracy = round(float(scores.mean()), 3)
        except Exception:
            self.accuracy = None

        # Feature importance
        importances = self.model.feature_importances_
        self.feature_importance = {
            col: round(float(imp), 4) for col, imp in zip(available, importances)
        }

        return True

    def predict(self, features_dict):
        """Predict severity for given feature values.
        features_dict: e.g. {"Hour": 14, "Weather": "Rainy", "Location": "Highway A1", ...}
        Returns dict with prediction and probabilities.
        """
        if self.model is None:
            return {"error": "Model not trained. Upload data first."}

        available = [c for c in self.FEATURE_COLS if c in self.encoders or c in features_dict]

        row = {}
        for col in available:
            val = features_dict.get(col)
            if val is None:
                return {"error": f"Missing feature: {col}"}
            if col in self.encoders:
                le = self.encoders[col]
                if str(val) not in le.classes_:
                    return {"error": f"Unknown value '{val}' for {col}. Known values: {list(le.classes_)}"}
                row[col] = le.transform([str(val)])[0]
            else:
                row[col] = val

        X_pred = pd.DataFrame([row])
        proba = self.model.predict_proba(X_pred)[0]
        pred_idx = int(np.argmax(proba))
        predicted_severity = self.classes[pred_idx]

        probabilities = {
            self.classes[i]: round(float(p), 3) for i, p in enumerate(proba)
        }

        return {
            "prediction": predicted_severity,
            "confidence": round(float(proba[pred_idx]), 3),
            "probabilities": probabilities,
            "features_used": list(features_dict.keys()),
        }

    def get_feature_importance(self):
        """Return feature importance rankings."""
        if not self.feature_importance:
            return {"error": "Model not trained."}
        sorted_features = sorted(
            self.feature_importance.items(), key=lambda x: x[1], reverse=True
        )
        return {
            "features": [{"name": n, "importance": v} for n, v in sorted_features],
            "accuracy": self.accuracy,
        }
