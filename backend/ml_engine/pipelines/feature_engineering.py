import pandas as pd
from typing import Dict, Any, List
from ml_engine.plugins.base import feature_engineering_registry

class FeatureEngineeringPipeline:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.plugins = []
        
        # Load plugins based on config
        plugin_names = self.config.get("feature_engineering_plugins", [])
        for name in plugin_names:
            try:
                plugin_instance = feature_engineering_registry.get_plugin(name)
                self.plugins.append(plugin_instance)
            except ValueError:
                pass # Ignore missing plugins or log warning
                
    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        X_curr = X.copy()
        for plugin in self.plugins:
            plugin.fit(X_curr, y)
            X_curr = plugin.transform(X_curr)
        return self
        
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_curr = X.copy()
        for plugin in self.plugins:
            X_curr = plugin.transform(X_curr)
        return X_curr
