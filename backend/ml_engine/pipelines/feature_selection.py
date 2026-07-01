import pandas as pd
from typing import Dict, Any, List
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif, f_regression

class FeatureSelectionPipeline:
    def __init__(self, config: Dict[str, Any], task_type: str):
        self.config = config
        self.task_type = task_type
        self.selector = None
        self.selected_features = []
        
    def fit(self, X: pd.DataFrame, y: pd.Series):
        strategy = self.config.get("feature_selection", "variance_threshold")
        
        if strategy == "variance_threshold":
            self.selector = VarianceThreshold(threshold=0.01)
        elif strategy == "kbest":
            score_func = f_classif if self.task_type == "classification" else f_regression
            k = min(10, X.shape[1])
            self.selector = SelectKBest(score_func=score_func, k=k)
            
        if self.selector:
            self.selector.fit(X, y)
            
            if hasattr(self.selector, 'get_feature_names_out'):
                self.selected_features = self.selector.get_feature_names_out(X.columns)
            else:
                self.selected_features = X.columns[self.selector.get_support()]
        else:
            self.selected_features = X.columns
            
        return self
        
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        if self.selector:
            return X[self.selected_features]
        return X
