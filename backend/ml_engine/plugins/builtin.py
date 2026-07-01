import pandas as pd
import numpy as np
from typing import Dict, Any
from sklearn.preprocessing import PolynomialFeatures
from .base import BasePlugin, feature_engineering_registry

class PolynomialFeaturesPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "polynomial_features"
        
    def __init__(self, degree=2):
        self.degree = degree
        self.poly = PolynomialFeatures(degree=self.degree, include_bias=False)
        self.numeric_cols = []
        
    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> 'BasePlugin':
        self.numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        if self.numeric_cols:
            self.poly.fit(X[self.numeric_cols])
        return self
        
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if not self.numeric_cols:
            return X
            
        poly_features = self.poly.transform(X[self.numeric_cols])
        poly_feature_names = self.poly.get_feature_names_out(self.numeric_cols)
        
        df_poly = pd.DataFrame(poly_features, columns=poly_feature_names, index=X.index)
        
        # Drop original numeric cols and concat the new polynomial ones
        X_out = X.drop(columns=self.numeric_cols)
        X_out = pd.concat([X_out, df_poly], axis=1)
        
        return X_out

class DatetimeExtractionPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "datetime_extraction"
        
    def __init__(self):
        self.datetime_cols = []
        
    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> 'BasePlugin':
        # Simple heuristic to detect datetime columns
        for col in X.columns:
            if pd.api.types.is_datetime64_any_dtype(X[col]):
                self.datetime_cols.append(col)
            elif X[col].dtype == 'object':
                try:
                    pd.to_datetime(X[col].dropna().head(10))
                    self.datetime_cols.append(col)
                except:
                    pass
        return self
        
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if not self.datetime_cols:
            return X
            
        X_out = X.copy()
        for col in self.datetime_cols:
            dt_series = pd.to_datetime(X_out[col])
            X_out[f"{col}_year"] = dt_series.dt.year
            X_out[f"{col}_month"] = dt_series.dt.month
            X_out[f"{col}_day"] = dt_series.dt.day
            X_out[f"{col}_dayofweek"] = dt_series.dt.dayofweek
            X_out = X_out.drop(columns=[col])
            
        return X_out

# Register built-in plugins
feature_engineering_registry.register(PolynomialFeaturesPlugin())
feature_engineering_registry.register(DatetimeExtractionPlugin())
