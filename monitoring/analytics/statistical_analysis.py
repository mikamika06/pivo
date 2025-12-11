
import pandas as pd
from typing import Dict, List, Any, Optional


class StatisticalAnalyzer:
    
    def calculate_basic_statistics(self, df: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Any]:
        if df.empty:
            return {}
        
        statistics = {}
        
        for column in numeric_columns:
            if column not in df.columns:
                continue
            
            df[column] = pd.to_numeric(df[column], errors='coerce')
            
            statistics[column] = {
                'mean': float(df[column].mean()),
                'median': float(df[column].median()),
                'min': float(df[column].min()),
                'max': float(df[column].max()),
                'std': float(df[column].std()),
                'quantile_25': float(df[column].quantile(0.25)),
                'quantile_50': float(df[column].quantile(0.50)),
                'quantile_75': float(df[column].quantile(0.75))
            }
        
        return statistics
    
    def perform_grouping_analysis(
        self, 
        df: pd.DataFrame, 
        group_by: str, 
        agg_column: str,
        agg_functions: Optional[List[str]] = None
    ) -> pd.DataFrame:
        if agg_functions is None:
            agg_functions = ['mean', 'sum', 'count']
        
        if df.empty or group_by not in df.columns or agg_column not in df.columns:
            return pd.DataFrame()
        
        grouped = df.groupby(group_by)[agg_column].agg(agg_functions)
        grouped = grouped.reset_index()
        
        return grouped
