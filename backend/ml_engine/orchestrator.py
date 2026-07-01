from typing import Dict, Any
import pandas as pd

class TaskDetector:
    @staticmethod
    def detect_task(profile_data: Dict[str, Any], target_column: str) -> str:
        """
        Determines if the task is classification or regression based on the target column's profile.
        """
        columns = profile_data.get("columns", {})
        if target_column not in columns:
            raise ValueError(f"Target column '{target_column}' not found in dataset profile.")
            
        target_info = columns[target_column]
        dtype = target_info.get("type", "")
        unique_count = target_info.get("unique_count", 0)
        
        # Simple heuristic: If it's an object/category, or has few unique integer values -> Classification
        if "object" in dtype or "category" in dtype or "bool" in dtype:
            return "classification"
        
        if "int" in dtype and unique_count <= 20:
            return "classification"
            
        return "regression"

class PipelineBuilder:
    @staticmethod
    def build_config(task_type: str, user_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Builds the final ML pipeline configuration by merging defaults with user_config.
        """
        default_config = {
            "imputation": "median",
            "encoding": "onehot",
            "scaling": "standard",
            "feature_selection": "variance_threshold",
            "models": []
        }
        
        if task_type == "classification":
            default_config["models"] = ["RandomForestClassifier", "LogisticRegression"]
        else:
            default_config["models"] = ["RandomForestRegressor", "LinearRegression"]
            
        if user_config:
            default_config.update(user_config)
            
        return default_config
