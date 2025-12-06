"""Plotting utilities for backtest results."""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_portfolio_value(history, title="Portfolio Value Over Time"):
    """Plot portfolio value over time."""
    df = pd.DataFrame(history)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['portfolio_value'], linewidth=2)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt.gcf()


def plot_drawdown(history, initial_capital):
    """Plot drawdown over time."""
    df = pd.DataFrame(history)
    portfolio_values = df['portfolio_value']
    cummax = portfolio_values.cummax()
    drawdown = (portfolio_values - cummax) / cummax
    
    plt.figure(figsize=(12, 6))
    plt.fill_between(df['timestamp'], drawdown, 0, alpha=0.3, color='red')
    plt.plot(df['timestamp'], drawdown, color='red', linewidth=2)
    plt.title('Drawdown Over Time')
    plt.xlabel('Date')
    plt.ylabel('Drawdown')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt.gcf()


def plot_returns_distribution(returns, title="Returns Distribution"):
    """Plot returns distribution."""
    plt.figure(figsize=(12, 6))
    plt.hist(returns, bins=50, edgecolor='black', alpha=0.7)
    plt.axvline(returns.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {returns.mean():.4f}')
    plt.title(title)
    plt.xlabel('Return')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt.gcf()


def plot_strategy_comparison(summaries, strategy_names):
    """Compare multiple strategies."""
    metrics = ['total_return', 'sharpe_ratio', 'max_drawdown', 'win_rate']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, metric in enumerate(metrics):
        values = [summary[metric] for summary in summaries]
        axes[idx].bar(strategy_names, values)
        axes[idx].set_title(metric.replace('_', ' ').title())
        axes[idx].grid(True, alpha=0.3)
        
        if metric in ['total_return', 'max_drawdown', 'win_rate']:
            axes[idx].yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1%}'))
    
    plt.tight_layout()
    return fig
