import pandas as pd
import numpy as np
import shap
from typing import Dict, Any

class ExplainabilityPipeline:
    def __init__(self, model: Any, task_type: str):
        self.model = model
        self.task_type = task_type
        
    def explain(self, X: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculates SHAP values for the model on the given dataset X.
        Returns a dictionary with feature importances.
        """
        # SHAP calculation can be slow, so we might sample
        X_sample = X.sample(n=min(100, len(X)), random_state=42)
        
        try:
            # Tree explainer works for Random Forest
            if hasattr(self.model, "estimators_"): 
                explainer = shap.TreeExplainer(self.model)
                shap_values = explainer.shap_values(X_sample)
            else:
                # KernelExplainer for linear models and others
                explainer = shap.KernelExplainer(self.model.predict, shap.sample(X, 10))
                shap_values = explainer.shap_values(X_sample)
                
            # Formatting SHAP output is complex as it depends on task (classification returns a list of arrays)
            if isinstance(shap_values, list): # Multi-class or binary classification TreeExplainer
                # Take the SHAP values for the positive class (class 1)
                shap_values_mean = np.abs(shap_values[1]).mean(axis=0)
            else:
                shap_values_mean = np.abs(shap_values).mean(axis=0)
                
            feature_names = X.columns.tolist()
            importance = {feature_names[i]: float(shap_values_mean[i]) for i in range(len(feature_names))}
            
            # Sort by importance
            importance = dict(sorted(importance.items(), key=lambda item: item[1], reverse=True))
            
            return {
                "method": "shap",
                "feature_importance": importance
            }
        except Exception as e:
            return {
                "method": "shap",
                "error": str(e),
                "feature_importance": {}
            }
