# ExecutionBacktester
Realistic, event-driven trading strategy backtesting and execution simulation framework.

## Overview

ExecutionBacktester is a Python-based framework for backtesting trading strategies with realistic execution simulation. It uses an event-driven architecture to model market data flow, signal generation, order placement, and execution with slippage and commissions.

## Architecture

### Event-Driven Design

The framework follows an event-driven architecture where components communicate through events:

```
Market Data → MarketEvent → Strategy → SignalEvent → Portfolio → OrderEvent → Execution → FillEvent → Portfolio
```

### Core Components

1. **EventEngine**: Central event queue and dispatcher
   - Manages event flow between components
   - Registers handlers for different event types
   - Processes events in order

2. **DataLoader**: Loads market data from CSV/Parquet files
   - Streams data as MarketEvents
   - Supports multiple symbols
   - Handles bid/ask spreads

3. **Strategy**: Base class for trading strategies
   - Receives MarketEvents
   - Generates SignalEvents based on logic
   - Pluggable architecture for custom strategies

4. **Portfolio**: Manages positions and capital
   - Converts signals to orders
   - Tracks positions and cash
   - Enforces risk limits (max 20% per position)
   - Records trade history

5. **ExecutionSimulator**: Simulates realistic execution
   - Models slippage (default 5 bps)
   - Applies commissions (default 1 bps)
   - Simulates partial fills (10% probability)
   - Generates FillEvents

6. **PerformanceAnalyzer**: Calculates performance metrics
   - Total return
   - Sharpe ratio
   - Maximum drawdown
   - Portfolio turnover
   - Win rate

### Architecture Diagram

```
┌─────────────┐
│ DataLoader  │
└──────┬──────┘
       │ MarketEvent
       ▼
┌─────────────┐     ┌──────────────┐
│ EventEngine │────▶│  Strategy    │
└──────┬──────┘     └──────┬───────┘
       │                   │ SignalEvent
       │                   ▼
       │            ┌──────────────┐
       │            │  Portfolio   │
       │            └──────┬───────┘
       │                   │ OrderEvent
       │                   ▼
       │            ┌──────────────┐
       │            │  Execution   │
       │            └──────┬───────┘
       │                   │ FillEvent
       │                   ▼
       └───────────▶ (back to Portfolio)
```

## Installation

### Basic Installation

```bash
pip install -e .
```

### With C++ Accelerator (Optional)

For faster execution simulation:

```bash
pip install -e . --with-cpp
```

Requirements:
- C++ compiler (MSVC on Windows, GCC/Clang on Linux/Mac)
- pybind11

## Quick Start

### 1. Generate Sample Data

```bash
cd examples
python generate_sample_data.py
```

This creates synthetic market data for AAPL, GOOGL, and MSFT.

### 2. Run a Backtest

```bash
backtest configs/ma_strategy.json
```

### 3. View Results

Results are saved to `results/ma_backtest_results.json`:

```json
{
  "total_return": 0.15,
  "sharpe_ratio": 1.8,
  "max_drawdown": -0.08,
  "turnover": 2.5,
  "win_rate": 0.55,
  "total_trades": 120
}
```

## Included Strategies

### 1. Moving Average Crossover

Classic trend-following strategy using short and long moving averages.

**Configuration:**
```json
{
  "strategy": {
    "type": "moving_average",
    "short_window": 20,
    "long_window": 50
  }
}
```

**Logic:**
- Buy when short MA crosses above long MA (golden cross)
- Sell when short MA crosses below long MA (death cross)

### 2. Breakout Strategy

Momentum strategy using Donchian channels.

**Configuration:**
```json
{
  "strategy": {
    "type": "breakout",
    "lookback": 20
  }
}
```

**Logic:**
- Buy when price breaks above 20-period high
- Sell when price breaks below 20-period low

### 3. ML Strategy (XGBoost)

Machine learning strategy using gradient boosting.

**Configuration:**
```json
{
  "strategy": {
    "type": "ml",
    "lookback": 50,
    "model_path": null
  }
}
```

**Features:**
- 5-period and 10-period returns (mean, std)
- Price momentum indicators
- Relative strength metrics

## Creating Custom Strategies

Extend the `Strategy` base class:

```python
from backtester.core.strategy import Strategy
from backtester.core.events import MarketEvent

class MyStrategy(Strategy):
    def __init__(self, strategy_id, engine, **params):
        super().__init__(strategy_id, engine)
        self.params = params
        
    def on_market_event(self, event: MarketEvent):
        # Your logic here
        if self.should_buy(event):
            self.generate_signal(
                event.symbol, 
                "LONG", 
                strength=1.0, 
                timestamp=event.timestamp
            )
```

## Configuration Files

Configuration files are JSON format with the following structure:

```json
{
  "data_path": "data/sample_data.csv",
  "data_format": "csv",
  "initial_capital": 100000,
  "slippage_bps": 5.0,
  "commission_bps": 1.0,
  "strategy": {
    "type": "moving_average",
    "short_window": 20,
    "long_window": 50
  },
  "output_path": "results/backtest_results.json"
}
```

## Data Format

Market data should be CSV or Parquet with columns:

| Column    | Type     | Required | Description           |
|-----------|----------|----------|-----------------------|
| timestamp | datetime | Yes      | Event timestamp       |
| symbol    | string   | Yes      | Ticker symbol         |
| price     | float    | Yes      | Trade price           |
| volume    | float    | No       | Trade volume          |
| bid       | float    | No       | Bid price             |
| ask       | float    | No       | Ask price             |

## Jupyter Notebook

Interactive demonstration in `notebooks/backtest_demo.ipynb`:

1. Load and visualize data
2. Run multiple strategies
3. Compare performance
4. Plot equity curves and returns

```bash
jupyter notebook notebooks/backtest_demo.ipynb
```

## Testing

Run the test suite:

```bash
pytest tests/
```

Tests cover:
- Event creation and dispatching
- Portfolio management
- Execution simulation
- Performance calculations

## C++ Accelerator Module

The optional C++ module provides faster execution for:
- Order execution simulation
- Portfolio value calculations
- Sharpe ratio computation

**Usage:**

```python
try:
    from execution_cpp import FastExecutionSimulator
    simulator = FastExecutionSimulator(slippage_bps=5.0, commission_bps=1.0)
    fill_price, slippage, commission = simulator.execute_order(150.0, 100, "BUY")
except ImportError:
    # Fall back to Python implementation
    pass
```

## Performance Metrics

### Sharpe Ratio
Risk-adjusted return metric:
```
Sharpe = sqrt(252) * (mean_return - risk_free_rate) / std_return
```

### Maximum Drawdown
Largest peak-to-trough decline:
```
Drawdown = (Portfolio_Value - Cumulative_Max) / Cumulative_Max
```

### Turnover
Trading activity relative to portfolio size:
```
Turnover = Total_Traded_Value / Average_Portfolio_Value
```

## Event-Driven Trading Systems

### Why Event-Driven?

1. **Realistic Simulation**: Models actual market data flow
2. **Modularity**: Components are loosely coupled
3. **Extensibility**: Easy to add new strategies or execution models
4. **Testability**: Each component can be tested independently
5. **Production-Ready**: Architecture translates to live trading

### Event Flow

1. **MarketEvent**: New market data arrives
2. **Strategy**: Analyzes data and generates signals
3. **SignalEvent**: Trading signal (LONG/SHORT/EXIT)
4. **Portfolio**: Converts signal to order based on risk limits
5. **OrderEvent**: Order to be executed
6. **Execution**: Simulates realistic fill with slippage
7. **FillEvent**: Confirms execution
8. **Portfolio**: Updates positions and cash

### Benefits Over Vectorized Backtesting

- No look-ahead bias
- Realistic order execution
- Event timing is explicit
- Easy to add market microstructure effects
- Supports multiple strategies simultaneously

## Project Structure

```
ExecutionBacktester/
├── backtester/
│   ├── core/
│   │   ├── events.py          # Event classes
│   │   ├── engine.py          # Event engine
│   │   ├── data_loader.py     # Data loading
│   │   ├── strategy.py        # Strategy base class
│   │   ├── portfolio.py       # Portfolio management
│   │   ├── execution.py       # Execution simulation
│   │   └── performance.py     # Performance metrics
│   ├── strategies/
│   │   ├── moving_average.py  # MA strategy
│   │   ├── breakout.py        # Breakout strategy
│   │   └── ml_strategy.py     # ML strategy
│   └── cli.py                 # Command-line interface
├── cpp/
│   └── execution_module.cpp   # C++ accelerator
├── tests/
│   ├── test_events.py
│   ├── test_engine.py
│   ├── test_portfolio.py
│   └── test_performance.py
├── examples/
│   └── generate_sample_data.py
├── configs/
│   ├── ma_strategy.json
│   ├── breakout_strategy.json
│   └── ml_strategy.json
├── notebooks/
│   └── backtest_demo.ipynb
├── data/                      # Generated data
├── results/                   # Backtest results
├── setup.py
└── README.md
```

## Requirements

- Python 3.8+
- numpy >= 1.20.0
- pandas >= 1.3.0
- pyarrow >= 5.0.0
- xgboost >= 1.5.0
- matplotlib >= 3.4.0
- jupyter >= 1.0.0
- pytest >= 6.2.0
- pybind11 >= 2.8.0 (for C++ module)

## License

MIT License

## Contributing

Contributions welcome! Areas for improvement:

- Additional strategies (mean reversion, pairs trading, etc.)
- More sophisticated execution models (VWAP, TWAP)
- Multi-asset portfolio optimization
- Risk management modules
- Live trading connectors
- Performance visualization dashboard

## Support

For issues and questions, please open a GitHub issue.

## Roadmap

- [ ] Add more execution algorithms (VWAP, TWAP, Iceberg)
- [ ] Implement portfolio optimization
- [ ] Add risk management (VaR, CVaR)
- [ ] Support for options and futures
- [ ] Real-time data connectors
- [ ] Web-based dashboard
- [ ] Distributed backtesting for parameter optimization
