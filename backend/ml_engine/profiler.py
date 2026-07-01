import pandas as pd
import numpy as np
from typing import Dict, Any
import io

class DatasetProfiler:
    @staticmethod
    def profile(csv_bytes: bytes) -> Dict[str, Any]:
        """
        Profiles the dataset and returns a dictionary with metadata.
        Reads a maximum of 10,000 rows to prevent MemoryErrors on free tier servers.
        """
        df = pd.read_csv(io.BytesIO(csv_bytes), nrows=10000)
        
        row_count = len(df)
        column_count = len(df.columns)
        
        memory_usage = df.memory_usage(deep=True).sum()
        
        missing_stats = df.isnull().sum().to_dict()
        missing_percentage = {k: (v / row_count) * 100 for k, v in missing_stats.items()} if row_count > 0 else {}
        
        duplicate_count = int(df.duplicated().sum())
        duplicate_percentage = (duplicate_count / row_count) * 100 if row_count > 0 else 0
        
        columns_info = {}
        for col in df.columns:
            col_type = str(df[col].dtype)
            unique_count = int(df[col].nunique())
            
            info = {
                "type": col_type,
                "missing_percentage": float(missing_percentage[col]),
                "unique_count": unique_count
            }
            
            if pd.api.types.is_numeric_dtype(df[col]):
                info["mean"] = float(df[col].mean()) if not pd.isna(df[col].mean()) else None
                info["std"] = float(df[col].std()) if not pd.isna(df[col].std()) else None
                info["min"] = float(df[col].min()) if not pd.isna(df[col].min()) else None
                info["max"] = float(df[col].max()) if not pd.isna(df[col].max()) else None
                info["skew"] = float(df[col].skew()) if not pd.isna(df[col].skew()) else None
            
            columns_info[col] = info

        return {
            "row_count": row_count,
            "column_count": column_count,
            "memory_usage_bytes": int(memory_usage),
            "duplicate_percentage": float(duplicate_percentage),
            "columns": columns_info
        }
