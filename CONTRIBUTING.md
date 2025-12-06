# Contributing to ExecutionBacktester

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/ExecutionBacktester.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests: `pytest tests/`
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
pytest tests/

# Format code
black backtester/

# Lint code
flake8 backtester/
```

## Code Style

- Follow PEP 8
- Use type hints where possible
- Write docstrings for all public functions
- Keep functions focused and small
- Use meaningful variable names

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage
- Test edge cases and error conditions

## Areas for Contribution

### High Priority

- Additional execution algorithms (VWAP, TWAP, Iceberg orders)
- More sophisticated slippage models
- Portfolio optimization modules
- Risk management features (VaR, CVaR)
- Performance visualization dashboard

### Medium Priority

- Additional strategy examples
- Data connectors for popular sources
- Multi-asset portfolio support
- Options and futures support
- Parameter optimization framework

### Low Priority

- Documentation improvements
- Example notebooks
- Performance optimizations
- Code refactoring

## Pull Request Guidelines

1. **Description**: Clearly describe what your PR does
2. **Tests**: Include tests for new functionality
3. **Documentation**: Update relevant documentation
4. **Commits**: Use clear, descriptive commit messages
5. **Code Quality**: Ensure code passes linting and formatting checks

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/stack traces

## Questions?

Open an issue with the "question" label or start a discussion.

Thank you for contributing!
