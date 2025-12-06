"""Tests for event classes."""

import pytest
from datetime import datetime
from backtester.core.events import MarketEvent, SignalEvent, OrderEvent, FillEvent


def test_market_event():
    """Test MarketEvent creation."""
    event = MarketEvent(
        timestamp=datetime.now(),
        symbol="AAPL",
        price=150.0,
        volume=1000,
        bid=149.5,
        ask=150.5,
    )
    assert event.symbol == "AAPL"
    assert event.price == 150.0


def test_signal_event():
    """Test SignalEvent creation."""
    event = SignalEvent(
        timestamp=datetime.now(),
        symbol="AAPL",
        signal_type="LONG",
        strength=0.8,
        strategy_id="test_strategy",
    )
    assert event.signal_type == "LONG"
    assert event.strength == 0.8


def test_order_event():
    """Test OrderEvent creation."""
    event = OrderEvent(
        timestamp=datetime.now(),
        symbol="AAPL",
        order_type="MARKET",
        quantity=100,
        direction="BUY",
    )
    assert event.direction == "BUY"
    assert event.quantity == 100


def test_fill_event():
    """Test FillEvent creation."""
    event = FillEvent(
        timestamp=datetime.now(),
        symbol="AAPL",
        quantity=100,
        direction="BUY",
        fill_price=150.5,
        commission=1.5,
        slippage=0.5,
        order_id="123",
    )
    assert event.fill_price == 150.5
    assert event.commission == 1.5
