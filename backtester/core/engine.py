"""Event engine for managing event queue and dispatching."""

from queue import Queue, Empty
from typing import Dict, List, Callable
from backtester.core.events import Event, MarketEvent, SignalEvent, OrderEvent, FillEvent


class EventEngine:
    """Central event queue and dispatcher."""
    
    def __init__(self):
        self.queue = Queue()
        self.handlers: Dict[type, List[Callable]] = {}
        self.running = False
        
    def register_handler(self, event_type: type, handler: Callable):
        """Register event handler."""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        
    def put(self, event: Event):
        """Add event to queue."""
        self.queue.put(event)
        
    def process_events(self):
        """Process all events in queue."""
        while not self.queue.empty():
            try:
                event = self.queue.get(block=False)
                self._dispatch(event)
            except Empty:
                break
                
    def _dispatch(self, event: Event):
        """Dispatch event to registered handlers."""
        event_type = type(event)
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                handler(event)
