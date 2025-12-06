"""Tests for data loader."""

import pytest
import pandas as pd
from pathlib import Path
from backtester.core.data_loader import DataLoader
from datetime import datetime


def test_data_loader_csv(tmp_path):
    """Test CSV data loading."""
    # Create test CSV
    csv_file = tmp_path / "test_data.csv"
    df = pd.DataFrame({
        'timestamp': [datetime(2023, 1, 1, 9, 30), datetime(2023, 1, 1, 10, 30)],
        'symbol': ['AAPL', 'AAPL'],
        'price': [150.0, 151.0],
        'volume': [1000, 1100],
    })
    df.to_csv(csv_file, index=False)
    
    # Load data
    loader = DataLoader(str(csv_file), 'csv')
    loader.load()
    
    assert len(loader.data) == 2
    assert loader.has_more_data()


def test_data_loader_events(tmp_path):
    """Test event generation."""
    csv_file = tmp_path / "test_data.csv"
    df = pd.DataFrame({
        'timestamp': [datetime(2023, 1, 1, 9, 30)],
        'symbol': ['AAPL'],
        'price': [150.0],
        'volume': [1000],
    })
    df.to_csv(csv_file, index=False)
    
    loader = DataLoader(str(csv_file), 'csv')
    loader.load()
    
    event = loader.get_next_event()
    assert event is not None
    assert event.symbol == 'AAPL'
    assert event.price == 150.0
    
    assert not loader.has_more_data()


def test_data_loader_latest_prices(tmp_path):
    """Test latest prices retrieval."""
    csv_file = tmp_path / "test_data.csv"
    df = pd.DataFrame({
        'timestamp': [datetime(2023, 1, 1, 9, 30), datetime(2023, 1, 1, 10, 30)],
        'symbol': ['AAPL', 'GOOGL'],
        'price': [150.0, 2800.0],
        'volume': [1000, 500],
    })
    df.to_csv(csv_file, index=False)
    
    loader = DataLoader(str(csv_file), 'csv')
    loader.load()
    
    loader.get_next_event()
    loader.get_next_event()
    
    prices = loader.get_latest_prices()
    assert 'AAPL' in prices
    assert 'GOOGL' in prices
    assert prices['AAPL'] == 150.0
