"""Tests for event engine."""

import pytest
from datetime import datetime
from backtester.core.engine import EventEngine
from backtester.core.events import MarketEvent


def test_event_engine_creation():
    """Test EventEngine initialization."""
    engine = EventEngine()
    assert engine.queue.empty()


def test_event_registration():
    """Test handler registration."""
    engine = EventEngine()
    called = []
    
    def handler(event):
        called.append(event)
    
    engine.register_handler(MarketEvent, handler)
    assert MarketEvent in engine.handlers


def test_event_dispatch():
    """Test event dispatching."""
    engine = EventEngine()
    called = []
    
    def handler(event):
        called.append(event)
    
    engine.register_handler(MarketEvent, handler)
    
    event = MarketEvent(
        timestamp=datetime.now(),
        symbol="AAPL",
        price=150.0,
        volume=1000,
    )
    
    engine.put(event)
    engine.process_events()
    
    assert len(called) == 1
    assert called[0].symbol == "AAPL"
