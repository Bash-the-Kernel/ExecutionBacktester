"""Execution simulator with slippage, queue position, and partial fills."""

import random
from backtester.core.events import OrderEvent, FillEvent
from backtester.core.engine import EventEngine


class ExecutionSimulator:
    """Simulate realistic order execution."""
    
    def __init__(self, engine: EventEngine, slippage_bps: float = 5.0, 
                 commission_bps: float = 1.0, partial_fill_prob: float = 0.1):
        self.engine = engine
        self.slippage_bps = slippage_bps / 10000.0
        self.commission_bps = commission_bps / 10000.0
        self.partial_fill_prob = partial_fill_prob
        self.current_prices = {}
        
    def update_prices(self, prices: dict):
        """Update current market prices."""
        self.current_prices.update(prices)
        
    def on_order_event(self, event: OrderEvent):
        """Execute order with realistic simulation."""
        if event.symbol not in self.current_prices:
            return
            
        base_price = self.current_prices[event.symbol]
        
        # Calculate slippage
        slippage_factor = random.uniform(0.5, 1.5) * self.slippage_bps
        if event.direction == "BUY":
            slippage = base_price * slippage_factor
        else:
            slippage = -base_price * slippage_factor
            
        fill_price = base_price + slippage
        
        # Simulate partial fills
        fill_quantity = event.quantity
        if random.random() < self.partial_fill_prob:
            fill_quantity *= random.uniform(0.5, 0.95)
            
        # Calculate commission
        commission = fill_quantity * fill_price * self.commission_bps
        
        # Generate fill event
        fill = FillEvent(
            timestamp=event.timestamp,
            symbol=event.symbol,
            quantity=fill_quantity,
            direction=event.direction,
            fill_price=fill_price,
            commission=commission,
            slippage=abs(slippage),
            order_id=event.order_id or "",
        )
        self.engine.put(fill)
