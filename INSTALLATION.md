# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) C++ compiler for accelerator module

## Step-by-Step Installation

### 1. Clone or Download Repository

```bash
cd ExecutionBacktester
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- numpy (numerical computing)
- pandas (data manipulation)
- pyarrow (Parquet support)
- xgboost (machine learning)
- matplotlib (plotting)
- jupyter (notebooks)
- pytest (testing)
- pybind11 (C++ bindings)

### 3. Install Package

**Standard Installation:**
```bash
pip install -e .
```

**With C++ Accelerator (Optional):**
```bash
pip install -e . --with-cpp
```

Note: C++ accelerator requires a C++ compiler:
- Windows: Visual Studio Build Tools
- Linux: GCC
- macOS: Xcode Command Line Tools

### 4. Verify Installation

```bash
python -m pytest tests/ -v
```

Expected output: `17 passed`

### 5. Generate Sample Data

```bash
cd examples
python generate_sample_data.py
```

This creates:
- `data/sample_data.csv` (26,211 rows)
- `data/sample_data.parquet`

### 6. Run Example Backtest

```bash
python run_example.py
```

You should see backtest results with performance metrics.

## Quick Test

```bash
# Run a quick backtest
python -m backtester.cli configs/ma_strategy.json
```

## Troubleshooting

### ModuleNotFoundError: No module named 'backtester'

**Solution:** Install package with `pip install -e .`

### FileNotFoundError: data/sample_data.csv

**Solution:** Generate data with `python examples/generate_sample_data.py`

### C++ Module Build Fails

**Solution:** Skip C++ module (it's optional):
```bash
pip install -e .
```

The framework works perfectly without the C++ accelerator.

### Import Errors for Dependencies

**Solution:** Install all dependencies:
```bash
pip install -r requirements.txt
```

## Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Package installed (`pip install -e .`)
- [ ] Tests pass (`python -m pytest tests/`)
- [ ] Sample data generated
- [ ] Example script runs successfully

## Next Steps

Once installed:

1. **Read Documentation**: Start with `QUICKSTART.md`
2. **Run Examples**: Try different strategies in `configs/`
3. **Explore Notebook**: Open `notebooks/backtest_demo.ipynb`
4. **Create Strategy**: Build your own in `backtester/strategies/`

## Uninstallation

```bash
pip uninstall execution-backtester
```

## Getting Help

- Check `README.md` for full documentation
- Review `QUICKSTART.md` for usage guide
- Open an issue on GitHub
