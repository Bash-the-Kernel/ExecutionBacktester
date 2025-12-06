"""Base strategy interface."""

from abc import ABC, abstractmethod
from backtester.core.events import MarketEvent, SignalEvent
from backtester.core.engine import EventEngine


class Strategy(ABC):
    """Base strategy class."""
    
    def __init__(self, strategy_id: str, engine: EventEngine):
        self.strategy_id = strategy_id
        self.engine = engine
        self.positions = {}
        
    @abstractmethod
    def on_market_event(self, event: MarketEvent):
        """Handle market data event."""
        pass
        
    def generate_signal(self, symbol: str, signal_type: str, strength: float, timestamp):
        """Generate trading signal."""
        signal = SignalEvent(
            timestamp=timestamp,
            symbol=symbol,
            signal_type=signal_type,
            strength=strength,
            strategy_id=self.strategy_id,
        )
        self.engine.put(signal)
