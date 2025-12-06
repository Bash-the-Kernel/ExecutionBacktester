# Makefile for ExecutionBacktester

.PHONY: install test clean data run-example run-ma run-breakout run-ml notebook

install:
	pip install -e .

install-cpp:
	pip install -e . --with-cpp

test:
	pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache

data:
	cd examples && python generate_sample_data.py

run-example:
	cd examples && python run_example.py

run-ma:
	backtest configs/ma_strategy.json

run-breakout:
	backtest configs/breakout_strategy.json

run-ml:
	backtest configs/ml_strategy.json

notebook:
	jupyter notebook notebooks/backtest_demo.ipynb

format:
	black backtester/ tests/ examples/

lint:
	flake8 backtester/ tests/ examples/

help:
	@echo "ExecutionBacktester Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install       - Install package"
	@echo "  install-cpp   - Install with C++ accelerator"
	@echo "  test          - Run tests"
	@echo "  clean         - Clean build artifacts"
	@echo "  data          - Generate sample data"
	@echo "  run-example   - Run example script"
	@echo "  run-ma        - Run moving average backtest"
	@echo "  run-breakout  - Run breakout backtest"
	@echo "  run-ml        - Run ML backtest"
	@echo "  notebook      - Open Jupyter notebook"
	@echo "  format        - Format code with black"
	@echo "  lint          - Lint code with flake8"
