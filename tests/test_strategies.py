"""Tests for trading strategies."""

import pytest
from datetime import datetime
from backtester.core.engine import EventEngine
from backtester.core.events import MarketEvent
from backtester.strategies import MovingAverageStrategy, BreakoutStrategy


def test_moving_average_strategy():
    """Test MovingAverageStrategy."""
    engine = EventEngine()
    strategy = MovingAverageStrategy('test', engine, short_window=5, long_window=10)
    
    # Feed price data
    for i in range(15):
        event = MarketEvent(
            timestamp=datetime.now(),
            symbol='AAPL',
            price=100 + i,
            volume=1000
        )
        strategy.on_market_event(event)
    
    # Should have generated signals
    assert 'AAPL' in strategy.positions


def test_breakout_strategy():
    """Test BreakoutStrategy."""
    engine = EventEngine()
    strategy = BreakoutStrategy('test', engine, lookback=10)
    
    # Feed price data with breakout
    for i in range(15):
        event = MarketEvent(
            timestamp=datetime.now(),
            symbol='AAPL',
            price=100 + (i if i < 10 else 20),  # Breakout at i=10
            volume=1000
        )
        strategy.on_market_event(event)
    
    # Should have detected breakout
    assert 'AAPL' in strategy.positions


def test_strategy_signal_generation():
    """Test signal generation."""
    engine = EventEngine()
    signals = []
    
    def capture_signal(event):
        signals.append(event)
    
    from backtester.core.events import SignalEvent
    engine.register_handler(SignalEvent, capture_signal)
    
    strategy = MovingAverageStrategy('test', engine, short_window=2, long_window=3)
    
    # Feed data to trigger signal
    for i in range(5):
        event = MarketEvent(
            timestamp=datetime.now(),
            symbol='AAPL',
            price=100 + i * 5,
            volume=1000
        )
        strategy.on_market_event(event)
        engine.process_events()
    
    # Should have generated at least one signal
    assert len(signals) > 0
