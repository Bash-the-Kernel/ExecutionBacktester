# Quick Reference Card

## Installation
```bash
pip install -e .
```

## Generate Sample Data
```bash
python examples/generate_sample_data.py
```

## Run Backtest

### CLI
```bash
python -m backtester.cli configs/ma_strategy.json
```

### Python Script
```bash
python examples/run_example.py
```

### Jupyter Notebook
```bash
jupyter notebook notebooks/backtest_demo.ipynb
```

## Run Tests
```bash
python -m pytest tests/ -v
```

## Project Structure
```
ExecutionBacktester/
├── backtester/          # Main package
│   ├── core/           # Core components
│   ├── strategies/     # Trading strategies
│   └── cli.py          # CLI tool
├── configs/            # Configuration files
├── data/               # Market data
├── examples/           # Example scripts
├── notebooks/          # Jupyter notebooks
├── tests/              # Test suite
└── results/            # Output results
```

## Configuration Format
```json
{
  "data_path": "data/sample_data.csv",
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

## Available Strategies
- `moving_average` - MA crossover (20/50)
- `breakout` - Donchian channels (20)
- `ml` - XGBoost predictions (50)

## Performance Metrics
- Total Return
- Sharpe Ratio
- Maximum Drawdown
- Portfolio Turnover
- Win Rate
- Total Trades

## Python API
```python
from backtester import EventEngine, DataLoader, Portfolio
from backtester.strategies import MovingAverageStrategy

# Initialize
engine = EventEngine()
data_loader = DataLoader('data/sample_data.csv')
portfolio = Portfolio(engine, 100000)
strategy = MovingAverageStrategy('ma', engine)

# Register handlers
engine.register_handler(MarketEvent, strategy.on_market_event)
engine.register_handler(SignalEvent, portfolio.on_signal_event)
engine.register_handler(OrderEvent, execution.on_order_event)
engine.register_handler(FillEvent, portfolio.on_fill_event)

# Run backtest
data_loader.load()
while data_loader.has_more_data():
    event = data_loader.get_next_event()
    engine.put(event)
    engine.process_events()
```

## Custom Strategy Template
```python
from backtester.core.strategy import Strategy
from backtester.core.events import MarketEvent

class MyStrategy(Strategy):
    def __init__(self, strategy_id, engine):
        super().__init__(strategy_id, engine)
        
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

## Common Commands

| Task | Command |
|------|---------|
| Install | `pip install -e .` |
| Generate data | `python examples/generate_sample_data.py` |
| Run example | `python examples/run_example.py` |
| Run MA backtest | `python -m backtester.cli configs/ma_strategy.json` |
| Run tests | `python -m pytest tests/ -v` |
| Open notebook | `jupyter notebook notebooks/backtest_demo.ipynb` |

## File Locations

| Item | Path |
|------|------|
| Sample data | `data/sample_data.csv` |
| Configs | `configs/*.json` |
| Results | `results/*.json` |
| Strategies | `backtester/strategies/*.py` |
| Tests | `tests/test_*.py` |
| Notebook | `notebooks/backtest_demo.ipynb` |

## Documentation

| Document | Description |
|----------|-------------|
| README.md | Main documentation |
| QUICKSTART.md | 5-minute guide |
| ARCHITECTURE.md | Design details |
| INSTALLATION.md | Setup instructions |
| TROUBLESHOOTING.md | Common issues |
| EVENT_DRIVEN_SYSTEMS.md | Architecture explanation |

## Support
- Check TROUBLESHOOTING.md for common issues
- Review documentation in docs/
- Open GitHub issue for bugs
