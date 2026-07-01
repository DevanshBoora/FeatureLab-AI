from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any

class BasePlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> 'BasePlugin':
        pass

    @abstractmethod
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        pass

class PluginRegistry:
    def __init__(self):
        self._plugins: Dict[str, BasePlugin] = {}

    def register(self, plugin: BasePlugin):
        self._plugins[plugin.name] = plugin

    def get_plugin(self, name: str) -> BasePlugin:
        if name not in self._plugins:
            raise ValueError(f"Plugin {name} not found in registry.")
        return self._plugins[name]
        
    def get_all(self) -> Dict[str, BasePlugin]:
        return self._plugins

# Global registries for different stages
feature_engineering_registry = PluginRegistry()
feature_selection_registry = PluginRegistry()
