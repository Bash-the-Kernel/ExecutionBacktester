# Quick Start Guide

Get up and running with ExecutionBacktester in 5 minutes.

## Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install Package

```bash
pip install -e .
```

### Step 3 (Optional): Build C++ Accelerator

```bash
pip install -e . --with-cpp
```

## Generate Sample Data

```bash
cd examples
python generate_sample_data.py
```

This creates:
- `data/sample_data.csv` - CSV format
- `data/sample_data.parquet` - Parquet format

Sample data includes:
- 3 symbols: AAPL, GOOGL, MSFT
- 1 year of hourly data
- Realistic price movements with random walk

## Run Your First Backtest

### Option 1: Using CLI

```bash
backtest configs/ma_strategy.json
```

### Option 2: Using Python Script

```bash
cd examples
python run_example.py
```

### Option 3: Using Jupyter Notebook

```bash
jupyter notebook notebooks/backtest_demo.ipynb
```

## Understanding the Output

```
=== Backtest Results ===
Total Return: 15.23%
Sharpe Ratio: 1.85
Max Drawdown: -8.45%
Turnover: 2.34
Win Rate: 54.32%
Total Trades: 127
```

**Metrics Explained:**

- **Total Return**: Overall profit/loss percentage
- **Sharpe Ratio**: Risk-adjusted return (higher is better)
- **Max Drawdown**: Largest peak-to-trough decline
- **Turnover**: Trading activity relative to portfolio size
- **Win Rate**: Percentage of profitable trades
- **Total Trades**: Number of executed trades

## Try Different Strategies

### Moving Average Crossover

```bash
backtest configs/ma_strategy.json
```

**Parameters:**
- Short window: 20 periods
- Long window: 50 periods

### Breakout Strategy

```bash
backtest configs/breakout_strategy.json
```

**Parameters:**
- Lookback: 20 periods

### ML Strategy

```bash
backtest configs/ml_strategy.json
```

**Parameters:**
- Lookback: 50 periods
- Model: XGBoost (auto-generated)

## Customize Configuration

Edit `configs/ma_strategy.json`:

```json
{
  "data_path": "data/sample_data.csv",
  "initial_capital": 100000,
  "slippage_bps": 5.0,
  "commission_bps": 1.0,
  "strategy": {
    "type": "moving_average",
    "short_window": 10,
    "long_window": 30
  }
}
```

**Adjustable Parameters:**

- `initial_capital`: Starting cash
- `slippage_bps`: Slippage in basis points (1 bps = 0.01%)
- `commission_bps`: Commission in basis points
- `short_window`: Fast moving average period
- `long_window`: Slow moving average period

## Create Your Own Strategy

### Step 1: Create Strategy File

Create `backtester/strategies/my_strategy.py`:

```python
from backtester.core.strategy import Strategy
from backtester.core.events import MarketEvent

class MyStrategy(Strategy):
    def __init__(self, strategy_id, engine):
        super().__init__(strategy_id, engine)
        self.threshold = 0.02  # 2% move
        
    def on_market_event(self, event: MarketEvent):
        # Your logic here
        if self.should_buy(event):
            self.generate_signal(
                event.symbol,
                "LONG",
                strength=1.0,
                timestamp=event.timestamp
            )
    
    def should_buy(self, event):
        # Implement your logic
        return True
```

### Step 2: Create Configuration

Create `configs/my_strategy.json`:

```json
{
  "data_path": "data/sample_data.csv",
  "initial_capital": 100000,
  "strategy": {
    "type": "my_strategy"
  }
}
```

### Step 3: Update CLI

Add to `backtester/cli.py`:

```python
from backtester.strategies.my_strategy import MyStrategy

# In run_backtest function:
elif strategy_type == "my_strategy":
    strategy = MyStrategy("my_strategy", engine)
```

### Step 4: Run It

```bash
backtest configs/my_strategy.json
```

## Use Your Own Data

### Data Format

CSV file with columns:

```csv
timestamp,symbol,price,volume,bid,ask
2023-01-01 09:30:00,AAPL,150.25,10000,150.20,150.30
2023-01-01 09:31:00,AAPL,150.50,12000,150.45,150.55
```

**Required Columns:**
- `timestamp`: Date and time (any pandas-parseable format)
- `symbol`: Ticker symbol
- `price`: Trade price

**Optional Columns:**
- `volume`: Trade volume
- `bid`: Bid price
- `ask`: Ask price

### Load Your Data

Update configuration:

```json
{
  "data_path": "path/to/your/data.csv",
  "data_format": "csv"
}
```

For Parquet files:

```json
{
  "data_path": "path/to/your/data.parquet",
  "data_format": "parquet"
}
```

## Run Tests

```bash
pytest tests/
```

Expected output:

```
tests/test_events.py ....
tests/test_engine.py ...
tests/test_portfolio.py ...
tests/test_performance.py ..

12 passed in 0.5s
```

## Next Steps

1. **Read the Architecture**: See `ARCHITECTURE.md` for detailed design
2. **Explore Strategies**: Check `backtester/strategies/` for examples
3. **Optimize Parameters**: Use the notebook to test different settings
4. **Add Features**: Extend the framework for your needs

## Common Issues

### Import Error

```
ModuleNotFoundError: No module named 'backtester'
```

**Solution**: Install package with `pip install -e .`

### No Data File

```
FileNotFoundError: data/sample_data.csv
```

**Solution**: Run `python examples/generate_sample_data.py`

### C++ Module Not Found

```
ImportError: execution_cpp
```

**Solution**: This is optional. Install with `pip install -e . --with-cpp` or ignore.

## Getting Help

- Check `README.md` for full documentation
- Review `ARCHITECTURE.md` for design details
- Open an issue on GitHub
- Review example code in `examples/` and `notebooks/`

## Performance Tips

1. **Use Parquet**: Faster loading than CSV
2. **Enable C++ Module**: 2-3x speedup for execution
3. **Reduce Data**: Test on smaller date ranges first
4. **Optimize Strategy**: Cache computed indicators
5. **Profile Code**: Use `cProfile` to find bottlenecks

Happy backtesting! 🚀
