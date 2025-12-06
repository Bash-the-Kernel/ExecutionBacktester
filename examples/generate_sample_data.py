"""Generate sample market data for backtesting."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path


def generate_sample_data(
    symbols=["AAPL", "GOOGL", "MSFT"],
    start_date="2023-01-01",
    end_date="2023-12-31",
    output_path="../data/sample_data.csv"
):
    # Ensure data directory exists
    output_file = Path(__file__).parent.parent / "data" / "sample_data.csv"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_path = str(output_file)
    """Generate synthetic market data."""
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    
    # Generate timestamps (trading days only)
    timestamps = pd.bdate_range(start, end, freq="h")
    
    data = []
    for symbol in symbols:
        # Initial price
        price = np.random.uniform(100, 500)
        
        for ts in timestamps:
            # Random walk with drift
            drift = 0.0001
            volatility = 0.02
            price *= np.exp(drift + volatility * np.random.randn())
            
            # Generate bid-ask spread
            spread = price * 0.001
            bid = price - spread / 2
            ask = price + spread / 2
            
            volume = np.random.randint(1000, 100000)
            
            data.append({
                "timestamp": ts,
                "symbol": symbol,
                "price": round(price, 2),
                "volume": volume,
                "bid": round(bid, 2),
                "ask": round(ask, 2),
            })
    
    df = pd.DataFrame(data)
    df = df.sort_values("timestamp").reset_index(drop=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} rows of sample data")
    print(f"Saved to {output_path}")
    
    # Also save as parquet
    parquet_path = output_path.replace(".csv", ".parquet")
    df.to_parquet(parquet_path, index=False)
    print(f"Saved to {parquet_path}")


if __name__ == "__main__":
    generate_sample_data()
