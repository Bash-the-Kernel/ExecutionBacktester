"""Performance analysis with Sharpe ratio, drawdown, and turnover."""

import numpy as np
import pandas as pd
from typing import List, Dict


class PerformanceAnalyzer:
    """Analyze backtest performance metrics."""
    
    def __init__(self, portfolio_history: List[Dict], initial_capital: float):
        self.history = pd.DataFrame(portfolio_history)
        self.initial_capital = initial_capital
        
    def calculate_returns(self) -> pd.Series:
        """Calculate period returns."""
        if len(self.history) == 0:
            return pd.Series()
        return self.history["portfolio_value"].pct_change().fillna(0)
        
    def sharpe_ratio(self, risk_free_rate: float = 0.02, periods_per_year: int = 252) -> float:
        """Calculate annualized Sharpe ratio."""
        returns = self.calculate_returns()
        if len(returns) == 0 or returns.std() == 0:
            return 0.0
        
        excess_returns = returns - risk_free_rate / periods_per_year
        return np.sqrt(periods_per_year) * excess_returns.mean() / returns.std()
        
    def max_drawdown(self) -> float:
        """Calculate maximum drawdown."""
        if len(self.history) == 0:
            return 0.0
            
        portfolio_values = self.history["portfolio_value"]
        cummax = portfolio_values.cummax()
        drawdown = (portfolio_values - cummax) / cummax
        return drawdown.min()
        
    def total_return(self) -> float:
        """Calculate total return."""
        if len(self.history) == 0:
            return 0.0
        final_value = self.history["portfolio_value"].iloc[-1]
        return (final_value - self.initial_capital) / self.initial_capital
        
    def turnover(self) -> float:
        """Calculate portfolio turnover."""
        if len(self.history) == 0:
            return 0.0
        
        total_traded = (self.history["quantity"] * self.history["price"]).sum()
        avg_portfolio_value = self.history["portfolio_value"].mean()
        return total_traded / avg_portfolio_value if avg_portfolio_value > 0 else 0.0
        
    def win_rate(self) -> float:
        """Calculate win rate."""
        if len(self.history) == 0:
            return 0.0
        
        returns = self.calculate_returns()
        winning_trades = (returns > 0).sum()
        total_trades = len(returns)
        return winning_trades / total_trades if total_trades > 0 else 0.0
        
    def get_summary(self) -> Dict:
        """Get performance summary."""
        return {
            "total_return": self.total_return(),
            "sharpe_ratio": self.sharpe_ratio(),
            "max_drawdown": self.max_drawdown(),
            "turnover": self.turnover(),
            "win_rate": self.win_rate(),
            "total_trades": len(self.history),
        }
