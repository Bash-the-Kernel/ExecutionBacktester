"""Event classes for event-driven architecture."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Event:
    """Base event class."""
    timestamp: datetime


@dataclass
class MarketEvent(Event):
    """Market data update event."""
    symbol: str
    price: float
    volume: float
    bid: Optional[float] = None
    ask: Optional[float] = None


@dataclass
class SignalEvent(Event):
    """Trading signal event."""
    symbol: str
    signal_type: str  # 'LONG', 'SHORT', 'EXIT'
    strength: float  # 0.0 to 1.0
    strategy_id: str


@dataclass
class OrderEvent(Event):
    """Order placement event."""
    symbol: str
    order_type: str  # 'MARKET', 'LIMIT'
    quantity: float
    direction: str  # 'BUY', 'SELL'
    price: Optional[float] = None
    order_id: Optional[str] = None


@dataclass
class FillEvent(Event):
    """Order fill event."""
    symbol: str
    quantity: float
    direction: str
    fill_price: float
    commission: float
    slippage: float
    order_id: str
