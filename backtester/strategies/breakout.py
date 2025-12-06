"""Breakout strategy based on price channels."""

from collections import deque
from backtester.core.strategy import Strategy
from backtester.core.events import MarketEvent


class BreakoutStrategy(Strategy):
    """Price breakout strategy using Donchian channels."""
    
    def __init__(self, strategy_id: str, engine, lookback: int = 20):
        super().__init__(strategy_id, engine)
        self.lookback = lookback
        self.price_history = {}
        
    def on_market_event(self, event: MarketEvent):
        """Handle market event and generate signals."""
        symbol = event.symbol
        
        if symbol not in self.price_history:
            self.price_history[symbol] = deque(maxlen=self.lookback)
            
        self.price_history[symbol].append(event.price)
        
        if len(self.price_history[symbol]) < self.lookback:
            return
            
        prices = list(self.price_history[symbol])
        upper_band = max(prices[:-1])
        lower_band = min(prices[:-1])
        current_price = event.price
        
        current_position = self.positions.get(symbol, 0)
        
        # Breakout above upper band
        if current_price > upper_band and current_position <= 0:
            self.generate_signal(symbol, "LONG", 1.0, event.timestamp)
            self.positions[symbol] = 1
            
        # Breakdown below lower band
        elif current_price < lower_band and current_position >= 0:
            self.generate_signal(symbol, "SHORT", 1.0, event.timestamp)
            self.positions[symbol] = -1
