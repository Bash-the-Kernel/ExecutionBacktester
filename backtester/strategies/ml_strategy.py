"""Machine learning strategy using XGBoost."""

import numpy as np
from collections import deque
from backtester.core.strategy import Strategy
from backtester.core.events import MarketEvent
import xgboost as xgb


class MLStrategy(Strategy):
    """ML-based strategy using XGBoost for predictions."""
    
    def __init__(self, strategy_id: str, engine, model_path: str = None, lookback: int = 50):
        super().__init__(strategy_id, engine)
        self.lookback = lookback
        self.price_history = {}
        self.model = None
        
        if model_path:
            self.model = xgb.Booster()
            self.model.load_model(model_path)
        else:
            # Simple default model
            self.model = self._create_default_model()
            
    def _create_default_model(self):
        """Create a simple default model."""
        # Train on synthetic data for demonstration
        X = np.random.randn(1000, 10)
        y = (X[:, 0] + X[:, 1] > 0).astype(int)
        dtrain = xgb.DMatrix(X, label=y)
        params = {"max_depth": 3, "eta": 0.1, "objective": "binary:logistic"}
        return xgb.train(params, dtrain, num_boost_round=10)
        
    def _extract_features(self, prices):
        """Extract features from price history."""
        if len(prices) < 10:
            return None
            
        returns = np.diff(prices) / prices[:-1]
        features = [
            np.mean(returns[-5:]),
            np.std(returns[-5:]),
            np.mean(returns[-10:]),
            np.std(returns[-10:]),
            (prices[-1] - prices[-5]) / prices[-5],
            (prices[-1] - prices[-10]) / prices[-10],
            np.max(prices[-10:]) / prices[-1] - 1,
            np.min(prices[-10:]) / prices[-1] - 1,
            np.mean(prices[-5:]) / np.mean(prices[-10:]) - 1,
            prices[-1] / prices[-20] - 1 if len(prices) >= 20 else 0,
        ]
        return np.array(features).reshape(1, -1)
        
    def on_market_event(self, event: MarketEvent):
        """Handle market event and generate signals."""
        symbol = event.symbol
        
        if symbol not in self.price_history:
            self.price_history[symbol] = deque(maxlen=self.lookback)
            
        self.price_history[symbol].append(event.price)
        
        if len(self.price_history[symbol]) < 20:
            return
            
        features = self._extract_features(list(self.price_history[symbol]))
        if features is None:
            return
            
        dmatrix = xgb.DMatrix(features)
        prediction = self.model.predict(dmatrix)[0]
        
        current_position = self.positions.get(symbol, 0)
        
        # Buy signal
        if prediction > 0.6 and current_position <= 0:
            self.generate_signal(symbol, "LONG", prediction, event.timestamp)
            self.positions[symbol] = 1
            
        # Sell signal
        elif prediction < 0.4 and current_position >= 0:
            self.generate_signal(symbol, "SHORT", 1 - prediction, event.timestamp)
            self.positions[symbol] = -1
