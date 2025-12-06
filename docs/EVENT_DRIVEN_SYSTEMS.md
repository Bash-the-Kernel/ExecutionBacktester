# Understanding Event-Driven Trading Systems

## What is Event-Driven Architecture?

Event-driven architecture (EDA) is a design pattern where the flow of the program is determined by events. In trading systems, events represent market data updates, trading signals, orders, and executions.

## Why Event-Driven for Trading?

### 1. Realistic Simulation

Traditional vectorized backtesting processes entire datasets at once, which creates look-ahead bias and unrealistic execution assumptions.

Event-driven approach processes data sequentially, mimicking real market conditions with proper timing, slippage, and commissions.

### 2. Modularity

Components are loosely coupled through events. Each component has a single responsibility and can be tested independently.

### 3. Production-Ready

The same architecture works for backtesting, paper trading, and live trading. Only the data source and execution handler change.

## Event Types in ExecutionBacktester

- **MarketEvent**: New market data (price, volume, bid/ask)
- **SignalEvent**: Trading signal from strategy (LONG/SHORT/EXIT)
- **OrderEvent**: Order to be executed (MARKET/LIMIT)
- **FillEvent**: Executed order with actual fill price and costs

## Event Flow

```
Market Data → Strategy → Signal → Portfolio → Order → Execution → Fill → Portfolio
```

Each step processes events sequentially, ensuring no look-ahead bias and realistic timing.

## Advantages Over Vectorized Backtesting

1. **No Look-Ahead Bias**: Only past data is accessible
2. **Realistic Execution**: Models slippage, commissions, partial fills
3. **Multiple Strategies**: Easy to run multiple strategies simultaneously
4. **Market Microstructure**: Can model order books, queue positions, etc.

## Transitioning to Live Trading

Change only the data source and execution handler:

- **Backtesting**: CSV data + Execution simulator
- **Paper Trading**: Live data feed + Execution simulator
- **Live Trading**: Live data feed + Broker API

The strategy and portfolio logic remain unchanged!
