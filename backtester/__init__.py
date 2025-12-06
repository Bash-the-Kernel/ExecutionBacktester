"""ExecutionBacktester - Event-driven trading strategy backtesting framework."""

__version__ = "0.1.0"

from backtester.core.events import MarketEvent, SignalEvent, OrderEvent, FillEvent
from backtester.core.engine import EventEngine
from backtester.core.data_loader import DataLoader
from backtester.core.portfolio import Portfolio
from backtester.core.execution import ExecutionSimulator
from backtester.core.performance import PerformanceAnalyzer
from backtester.core.strategy import Strategy

__all__ = [
    "MarketEvent",
    "SignalEvent",
    "OrderEvent",
    "FillEvent",
    "EventEngine",
    "DataLoader",
    "Portfolio",
    "ExecutionSimulator",
    "PerformanceAnalyzer",
    "Strategy",
]
