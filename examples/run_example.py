"""Example script to run a complete backtest."""

import sys
from pathlib import Path
sys.path.append('..')

from backtester.core.engine import EventEngine
from backtester.core.data_loader import DataLoader
from backtester.core.portfolio import Portfolio
from backtester.core.execution import ExecutionSimulator
from backtester.core.performance import PerformanceAnalyzer
from backtester.core.events import MarketEvent, SignalEvent, OrderEvent, FillEvent
from backtester.strategies import MovingAverageStrategy
import pandas as pd


def main():
    """Run example backtest."""
    print("ExecutionBacktester Example")
    print("=" * 50)
    
    # Initialize components
    print("\n1. Initializing components...")
    engine = EventEngine()
    data_path = Path(__file__).parent.parent / "data" / "sample_data.csv"
    data_loader = DataLoader(str(data_path), 'csv')
    portfolio = Portfolio(engine, initial_capital=100000)
    execution = ExecutionSimulator(engine, slippage_bps=5.0, commission_bps=1.0)
    
    # Create strategy
    print("2. Creating moving average strategy...")
    strategy = MovingAverageStrategy('ma_strategy', engine, short_window=20, long_window=50)
    
    # Register handlers
    print("3. Registering event handlers...")
    engine.register_handler(MarketEvent, strategy.on_market_event)
    engine.register_handler(SignalEvent, portfolio.on_signal_event)
    engine.register_handler(OrderEvent, execution.on_order_event)
    engine.register_handler(FillEvent, portfolio.on_fill_event)
    
    # Load data
    print("4. Loading market data...")
    data_loader.load()
    print(f"   Loaded {len(data_loader.data)} market events")
    
    # Run backtest
    print("5. Running backtest...")
    event_count = 0
    while data_loader.has_more_data():
        event = data_loader.get_next_event()
        if event:
            engine.put(event)
            engine.process_events()
            
            # Update prices
            prices = data_loader.get_latest_prices()
            portfolio.update_holdings(prices)
            execution.update_prices(prices)
            
            event_count += 1
            if event_count % 1000 == 0:
                print(f"   Processed {event_count} events...")
    
    print(f"   Completed! Processed {event_count} events")
    
    # Analyze performance
    print("\n6. Analyzing performance...")
    analyzer = PerformanceAnalyzer(portfolio.history, portfolio.initial_capital)
    summary = analyzer.get_summary()
    
    print("\n" + "=" * 50)
    print("BACKTEST RESULTS")
    print("=" * 50)
    print(f"Initial Capital:  ${portfolio.initial_capital:,.2f}")
    print(f"Final Value:      ${portfolio.get_portfolio_value():,.2f}")
    print(f"Total Return:     {summary['total_return']:.2%}")
    print(f"Sharpe Ratio:     {summary['sharpe_ratio']:.2f}")
    print(f"Max Drawdown:     {summary['max_drawdown']:.2%}")
    print(f"Turnover:         {summary['turnover']:.2f}")
    print(f"Win Rate:         {summary['win_rate']:.2%}")
    print(f"Total Trades:     {summary['total_trades']}")
    print("=" * 50)
    
    # Show sample trades
    if portfolio.history:
        print("\nSample Trades (first 5):")
        df = pd.DataFrame(portfolio.history[:5])
        print(df[['timestamp', 'symbol', 'direction', 'quantity', 'price', 'portfolio_value']].to_string(index=False))


if __name__ == "__main__":
    main()
