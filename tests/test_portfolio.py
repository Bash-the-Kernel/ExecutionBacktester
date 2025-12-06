"""Tests for portfolio management."""

import pytest
from datetime import datetime
from backtester.core.engine import EventEngine
from backtester.core.portfolio import Portfolio
from backtester.core.events import SignalEvent, FillEvent


def test_portfolio_creation():
    """Test Portfolio initialization."""
    engine = EventEngine()
    portfolio = Portfolio(engine, initial_capital=100000)
    assert portfolio.cash == 100000
    assert portfolio.get_portfolio_value() == 100000


def test_portfolio_fill_event():
    """Test portfolio update on fill."""
    engine = EventEngine()
    portfolio = Portfolio(engine, initial_capital=100000)
    
    fill = FillEvent(
        timestamp=datetime.now(),
        symbol="AAPL",
        quantity=100,
        direction="BUY",
        fill_price=150.0,
        commission=1.5,
        slippage=0.5,
        order_id="123",
    )
    
    portfolio.on_fill_event(fill)
    
    assert portfolio.positions["AAPL"] == 100
    assert portfolio.cash < 100000
    assert len(portfolio.history) == 1


def test_portfolio_value_calculation():
    """Test portfolio value calculation."""
    engine = EventEngine()
    portfolio = Portfolio(engine, initial_capital=100000)
    
    portfolio.positions["AAPL"] = 100
    portfolio.holdings["AAPL"] = 150.0
    portfolio.cash = 85000
    
    value = portfolio.get_portfolio_value()
    assert value == 100000  # 85000 + 100*150
