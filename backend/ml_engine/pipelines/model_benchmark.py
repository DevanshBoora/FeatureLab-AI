import pandas as pd
from typing import Dict, Any, List, Tuple
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, mean_squared_error, r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression

class ModelBenchmarkPipeline:
    def __init__(self, config: Dict[str, Any], task_type: str):
        self.config = config
        self.task_type = task_type
        self.models_to_run = self.config.get("models", [])
        self.trained_models = {}
        self.results = {}
        
    def get_model_instance(self, model_name: str):
        if model_name == "RandomForestClassifier":
            return RandomForestClassifier(n_estimators=50, random_state=42)
        elif model_name == "LogisticRegression":
            return LogisticRegression(random_state=42, max_iter=500)
        elif model_name == "RandomForestRegressor":
            return RandomForestRegressor(n_estimators=50, random_state=42)
        elif model_name == "LinearRegression":
            return LinearRegression()
        else:
            raise ValueError(f"Model {model_name} is not supported.")
            
    def _evaluate_classification(self, y_true, y_pred) -> Dict[str, float]:
        return {
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "f1_score": float(f1_score(y_true, y_pred, average='weighted')),
            "precision": float(precision_score(y_true, y_pred, average='weighted')),
            "recall": float(recall_score(y_true, y_pred, average='weighted'))
        }
        
    def _evaluate_regression(self, y_true, y_pred) -> Dict[str, float]:
        return {
            "rmse": float(mean_squared_error(y_true, y_pred, squared=False)),
            "mae": float(mean_absolute_error(y_true, y_pred)),
            "r2_score": float(r2_score(y_true, y_pred))
        }

    def fit_and_evaluate(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        for model_name in self.models_to_run:
            model = self.get_model_instance(model_name)
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            
            if self.task_type == "classification":
                metrics = self._evaluate_classification(y_test, y_pred)
            else:
                metrics = self._evaluate_regression(y_test, y_pred)
                
            self.trained_models[model_name] = model
            self.results[model_name] = metrics
            
        return self.results
