"""Command-line interface for running backtests."""

import argparse
import json
from pathlib import Path
from backtester.core.engine import EventEngine
from backtester.core.data_loader import DataLoader
from backtester.core.portfolio import Portfolio
from backtester.core.execution import ExecutionSimulator
from backtester.core.performance import PerformanceAnalyzer
from backtester.core.events import MarketEvent, SignalEvent, OrderEvent, FillEvent
from backtester.strategies import MovingAverageStrategy, BreakoutStrategy, MLStrategy


def run_backtest(config_path: str):
    """Run backtest from configuration file."""
    from pathlib import Path
    
    with open(config_path) as f:
        config = json.load(f)
    
    # Resolve data path relative to config file
    config_dir = Path(config_path).parent
    data_path = config_dir / config["data_path"]
    if not data_path.exists():
        data_path = Path(config["data_path"])
    
    # Initialize components
    engine = EventEngine()
    data_loader = DataLoader(str(data_path), config.get("data_format", "csv"))
    portfolio = Portfolio(engine, config.get("initial_capital", 100000))
    execution = ExecutionSimulator(
        engine,
        config.get("slippage_bps", 5.0),
        config.get("commission_bps", 1.0),
    )
    
    # Initialize strategy
    strategy_type = config["strategy"]["type"]
    if strategy_type == "moving_average":
        strategy = MovingAverageStrategy(
            "ma_strategy",
            engine,
            config["strategy"].get("short_window", 20),
            config["strategy"].get("long_window", 50),
        )
    elif strategy_type == "breakout":
        strategy = BreakoutStrategy(
            "breakout_strategy",
            engine,
            config["strategy"].get("lookback", 20),
        )
    elif strategy_type == "ml":
        strategy = MLStrategy(
            "ml_strategy",
            engine,
            config["strategy"].get("model_path"),
            config["strategy"].get("lookback", 50),
        )
    else:
        raise ValueError(f"Unknown strategy type: {strategy_type}")
    
    # Register handlers
    engine.register_handler(MarketEvent, strategy.on_market_event)
    engine.register_handler(SignalEvent, portfolio.on_signal_event)
    engine.register_handler(OrderEvent, execution.on_order_event)
    engine.register_handler(FillEvent, portfolio.on_fill_event)
    
    # Load data
    data_loader.load()
    
    # Run backtest
    print("Running backtest...")
    while data_loader.has_more_data():
        event = data_loader.get_next_event()
        if event:
            engine.put(event)
            engine.process_events()
            
            # Update prices
            prices = data_loader.get_latest_prices()
            portfolio.update_holdings(prices)
            execution.update_prices(prices)
    
    # Analyze performance
    analyzer = PerformanceAnalyzer(portfolio.history, portfolio.initial_capital)
    summary = analyzer.get_summary()
    
    print("\n=== Backtest Results ===")
    print(f"Total Return: {summary['total_return']:.2%}")
    print(f"Sharpe Ratio: {summary['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {summary['max_drawdown']:.2%}")
    print(f"Turnover: {summary['turnover']:.2f}")
    print(f"Win Rate: {summary['win_rate']:.2%}")
    print(f"Total Trades: {summary['total_trades']}")
    
    # Save results
    output_path = config.get("output_path", "backtest_results.json")
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved to {output_path}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Run trading strategy backtest")
    parser.add_argument("config", help="Path to configuration file")
    args = parser.parse_args()
    
    run_backtest(args.config)


if __name__ == "__main__":
    main()
