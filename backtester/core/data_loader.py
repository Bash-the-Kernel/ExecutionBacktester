"""Data loading from CSV and Parquet files."""

import pandas as pd
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from backtester.core.events import MarketEvent


class DataLoader:
    """Load and stream market data."""
    
    def __init__(self, data_path: str, file_format: str = "csv"):
        self.data_path = Path(data_path)
        self.file_format = file_format
        self.data: Optional[pd.DataFrame] = None
        self.current_index = 0
        
    def load(self):
        """Load data from file."""
        if self.file_format == "csv":
            self.data = pd.read_csv(self.data_path, parse_dates=["timestamp"])
        elif self.file_format == "parquet":
            self.data = pd.read_parquet(self.data_path)
        else:
            raise ValueError(f"Unsupported format: {self.file_format}")
        
        self.data = self.data.sort_values("timestamp").reset_index(drop=True)
        self.current_index = 0
        
    def get_next_event(self) -> Optional[MarketEvent]:
        """Get next market event."""
        if self.data is None or self.current_index >= len(self.data):
            return None
            
        row = self.data.iloc[self.current_index]
        self.current_index += 1
        
        return MarketEvent(
            timestamp=row["timestamp"],
            symbol=row["symbol"],
            price=row["price"],
            volume=row.get("volume", 0),
            bid=row.get("bid"),
            ask=row.get("ask"),
        )
        
    def has_more_data(self) -> bool:
        """Check if more data available."""
        return self.data is not None and self.current_index < len(self.data)
        
    def get_latest_prices(self) -> Dict[str, float]:
        """Get latest prices for all symbols."""
        if self.data is None or self.current_index == 0:
            return {}
        
        recent_data = self.data.iloc[:self.current_index]
        return recent_data.groupby("symbol")["price"].last().to_dict()
