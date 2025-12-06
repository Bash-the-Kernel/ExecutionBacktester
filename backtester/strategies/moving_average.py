"""Moving average crossover strategy."""

from collections import deque
from backtester.core.strategy import Strategy
from backtester.core.events import MarketEvent


class MovingAverageStrategy(Strategy):
    """Simple moving average crossover strategy."""
    
    def __init__(self, strategy_id: str, engine, short_window: int = 20, long_window: int = 50):
        super().__init__(strategy_id, engine)
        self.short_window = short_window
        self.long_window = long_window
        self.price_history = {}
        
    def on_market_event(self, event: MarketEvent):
        """Handle market event and generate signals."""
        symbol = event.symbol
        
        if symbol not in self.price_history:
            self.price_history[symbol] = deque(maxlen=self.long_window)
            
        self.price_history[symbol].append(event.price)
        
        if len(self.price_history[symbol]) < self.long_window:
            return
            
        prices = list(self.price_history[symbol])
        short_ma = sum(prices[-self.short_window:]) / self.short_window
        long_ma = sum(prices) / self.long_window
        
        current_position = self.positions.get(symbol, 0)
        
        # Golden cross - buy signal
        if short_ma > long_ma and current_position <= 0:
            self.generate_signal(symbol, "LONG", 1.0, event.timestamp)
            self.positions[symbol] = 1
            
        # Death cross - sell signal
        elif short_ma < long_ma and current_position >= 0:
            self.generate_signal(symbol, "SHORT", 1.0, event.timestamp)
            self.positions[symbol] = -1
