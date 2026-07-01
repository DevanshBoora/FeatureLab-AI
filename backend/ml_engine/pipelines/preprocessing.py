import pandas as pd
from typing import Dict, Any, List
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, OrdinalEncoder

class PreprocessingPipeline:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.numeric_imputer = None
        self.categorical_imputer = None
        self.scaler = None
        self.encoder = None
        self.numeric_cols = []
        self.categorical_cols = []
        
    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        self.numeric_cols = X.select_dtypes(include=['number']).columns.tolist()
        self.categorical_cols = X.select_dtypes(exclude=['number']).columns.tolist()
        
        # Imputation
        imputation_strategy = self.config.get("imputation", "median")
        if imputation_strategy == "median":
            self.numeric_imputer = SimpleImputer(strategy="median")
        elif imputation_strategy == "mean":
            self.numeric_imputer = SimpleImputer(strategy="mean")
            
        self.categorical_imputer = SimpleImputer(strategy="most_frequent")
        
        if self.numeric_cols and self.numeric_imputer:
            self.numeric_imputer.fit(X[self.numeric_cols])
        if self.categorical_cols and self.categorical_imputer:
            self.categorical_imputer.fit(X[self.categorical_cols])
            
        # Encoding
        encoding_strategy = self.config.get("encoding", "onehot")
        if encoding_strategy == "onehot":
            self.encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        elif encoding_strategy == "ordinal":
            self.encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
            
        if self.categorical_cols and self.encoder:
            # Fit encoder on imputed data
            cat_imputed = self.categorical_imputer.transform(X[self.categorical_cols])
            self.encoder.fit(cat_imputed)
            
        # Scaling
        scaling_strategy = self.config.get("scaling", "standard")
        if scaling_strategy == "standard":
            self.scaler = StandardScaler()
        elif scaling_strategy == "minmax":
            self.scaler = MinMaxScaler()
            
        if self.numeric_cols and self.scaler:
            num_imputed = self.numeric_imputer.transform(X[self.numeric_cols])
            self.scaler.fit(num_imputed)
            
        return self
        
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_out = X.copy()
        
        # Impute & Scale numeric
        if self.numeric_cols:
            num_imputed = self.numeric_imputer.transform(X_out[self.numeric_cols])
            if self.scaler:
                num_scaled = self.scaler.transform(num_imputed)
                df_num = pd.DataFrame(num_scaled, columns=self.numeric_cols, index=X_out.index)
            else:
                df_num = pd.DataFrame(num_imputed, columns=self.numeric_cols, index=X_out.index)
        else:
            df_num = pd.DataFrame(index=X_out.index)
            
        # Impute & Encode categorical
        if self.categorical_cols:
            cat_imputed = self.categorical_imputer.transform(X_out[self.categorical_cols])
            if self.encoder:
                cat_encoded = self.encoder.transform(cat_imputed)
                if isinstance(self.encoder, OneHotEncoder):
                    cat_cols = self.encoder.get_feature_names_out(self.categorical_cols)
                else:
                    cat_cols = self.categorical_cols
                df_cat = pd.DataFrame(cat_encoded, columns=cat_cols, index=X_out.index)
            else:
                df_cat = pd.DataFrame(cat_imputed, columns=self.categorical_cols, index=X_out.index)
        else:
            df_cat = pd.DataFrame(index=X_out.index)
            
        # Combine
        return pd.concat([df_num, df_cat], axis=1)
