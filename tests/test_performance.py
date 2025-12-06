"""Tests for performance analysis."""

import pytest
import pandas as pd
from backtester.core.performance import PerformanceAnalyzer


def test_performance_analyzer():
    """Test PerformanceAnalyzer metrics."""
    history = [
        {"timestamp": pd.Timestamp("2023-01-01"), "portfolio_value": 100000, 
         "quantity": 100, "price": 150, "direction": "BUY", "commission": 1.5},
        {"timestamp": pd.Timestamp("2023-01-02"), "portfolio_value": 101000,
         "quantity": 100, "price": 151, "direction": "SELL", "commission": 1.5},
        {"timestamp": pd.Timestamp("2023-01-03"), "portfolio_value": 102000,
         "quantity": 100, "price": 152, "direction": "BUY", "commission": 1.5},
    ]
    
    analyzer = PerformanceAnalyzer(history, 100000)
    
    total_return = analyzer.total_return()
    assert total_return > 0
    
    sharpe = analyzer.sharpe_ratio()
    assert isinstance(sharpe, float)
    
    drawdown = analyzer.max_drawdown()
    assert drawdown <= 0
    
    summary = analyzer.get_summary()
    assert "total_return" in summary
    assert "sharpe_ratio" in summary
