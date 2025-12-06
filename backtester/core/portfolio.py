"""Portfolio management with positions, PnL, and risk limits."""

from typing import Dict, List
from datetime import datetime
from backtester.core.events import SignalEvent, OrderEvent, FillEvent
from backtester.core.engine import EventEngine
import uuid


class Portfolio:
    """Manage positions, cash, and generate orders from signals."""
    
    def __init__(self, engine: EventEngine, initial_capital: float = 100000.0):
        self.engine = engine
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: Dict[str, float] = {}
        self.holdings: Dict[str, float] = {}
        self.history: List[Dict] = []
        self.max_position_size = 0.2  # 20% of portfolio per position
        
    def on_signal_event(self, event: SignalEvent):
        """Convert signal to order."""
        current_position = self.positions.get(event.symbol, 0)
        portfolio_value = self.get_portfolio_value()
        max_value = portfolio_value * self.max_position_size
        
        if event.signal_type == "LONG" and current_position <= 0:
            quantity = (max_value * event.strength) / self.holdings.get(event.symbol, 1)
            order = OrderEvent(
                timestamp=event.timestamp,
                symbol=event.symbol,
                order_type="MARKET",
                quantity=abs(quantity),
                direction="BUY",
                order_id=str(uuid.uuid4()),
            )
            self.engine.put(order)
            
        elif event.signal_type == "SHORT" and current_position >= 0:
            quantity = (max_value * event.strength) / self.holdings.get(event.symbol, 1)
            order = OrderEvent(
                timestamp=event.timestamp,
                symbol=event.symbol,
                order_type="MARKET",
                quantity=abs(quantity),
                direction="SELL",
                order_id=str(uuid.uuid4()),
            )
            self.engine.put(order)
            
        elif event.signal_type == "EXIT" and current_position != 0:
            order = OrderEvent(
                timestamp=event.timestamp,
                symbol=event.symbol,
                order_type="MARKET",
                quantity=abs(current_position),
                direction="SELL" if current_position > 0 else "BUY",
                order_id=str(uuid.uuid4()),
            )
            self.engine.put(order)
            
    def on_fill_event(self, event: FillEvent):
        """Update portfolio on fill."""
        direction_multiplier = 1 if event.direction == "BUY" else -1
        
        # Update positions
        self.positions[event.symbol] = self.positions.get(event.symbol, 0) + (
            event.quantity * direction_multiplier
        )
        
        # Update cash
        cost = event.quantity * event.fill_price
        self.cash -= cost * direction_multiplier + event.commission
        
        # Update holdings
        self.holdings[event.symbol] = event.fill_price
        
        # Record history
        self.history.append({
            "timestamp": event.timestamp,
            "symbol": event.symbol,
            "quantity": event.quantity,
            "direction": event.direction,
            "price": event.fill_price,
            "commission": event.commission,
            "slippage": event.slippage,
            "cash": self.cash,
            "portfolio_value": self.get_portfolio_value(),
        })
        
    def update_holdings(self, prices: Dict[str, float]):
        """Update current holdings prices."""
        self.holdings.update(prices)
        
    def get_portfolio_value(self) -> float:
        """Calculate total portfolio value."""
        holdings_value = sum(
            self.positions.get(symbol, 0) * price
            for symbol, price in self.holdings.items()
        )
        return self.cash + holdings_value
        
    def get_returns(self) -> float:
        """Calculate total returns."""
        return (self.get_portfolio_value() - self.initial_capital) / self.initial_capital
