# Troubleshooting Guide

## Common Issues and Solutions

### Issue: FileNotFoundError for sample_data.csv

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/sample_data.csv'
```

**Solution:**
Generate the sample data first:
```bash
cd examples
python generate_sample_data.py
```

Or from project root:
```bash
python examples/generate_sample_data.py
```

### Issue: ModuleNotFoundError: No module named 'backtester'

**Error:**
```
ModuleNotFoundError: No module named 'backtester'
```

**Solution:**
Install the package:
```bash
pip install -e .
```

### Issue: Command 'backtest' not found

**Error:**
```
'backtest' is not recognized as an internal or external command
```

**Solution:**
Use the full Python module path:
```bash
python -m backtester.cli configs/ma_strategy.json
```

Or ensure Python Scripts directory is in PATH.

### Issue: pytest not found

**Error:**
```
Command 'pytest' not found
```

**Solution:**
Use Python module syntax:
```bash
python -m pytest tests/ -v
```

### Issue: C++ module build fails

**Error:**
```
ModuleNotFoundError: No module named 'pybind11'
```

**Solution:**
The C++ module is optional. Install without it:
```bash
pip install -e .
```

Skip the `--with-cpp` flag.

### Issue: Import errors for dependencies

**Error:**
```
ModuleNotFoundError: No module named 'numpy'
```

**Solution:**
Install all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Pandas FutureWarning about 'H' frequency

**Warning:**
```
FutureWarning: 'H' is deprecated and will be removed in a future version
```

**Solution:**
This is just a warning and doesn't affect functionality. The code has been updated to use 'h' instead of 'H'.

### Issue: Results directory doesn't exist

**Error:**
```
FileNotFoundError: results/backtest_results.json
```

**Solution:**
The results directory is created automatically. If you deleted it, recreate:
```bash
mkdir results
```

### Issue: Running from wrong directory

**Error:**
```
FileNotFoundError: configs/ma_strategy.json
```

**Solution:**
Run commands from the project root directory:
```bash
cd ExecutionBacktester
python -m backtester.cli configs/ma_strategy.json
```

## Verification Steps

### 1. Check Python Version
```bash
python --version
```
Should be 3.8 or higher.

### 2. Verify Installation
```bash
pip show execution-backtester
```
Should show package information.

### 3. Test Import
```bash
python -c "import backtester; print('OK')"
```
Should print "OK".

### 4. Run Tests
```bash
python -m pytest tests/ -v
```
Should show 17 tests passing.

### 5. Check Data
```bash
dir data
```
Should show sample_data.csv and sample_data.parquet.

## Getting Help

If issues persist:

1. Check Python version: `python --version`
2. Check installed packages: `pip list`
3. Verify project structure: `dir /s /b *.py`
4. Review error messages carefully
5. Check file paths are correct
6. Ensure you're in the correct directory

## Quick Reset

To start fresh:

```bash
# Uninstall
pip uninstall execution-backtester -y

# Clean
rmdir /s /q build dist *.egg-info __pycache__

# Reinstall
pip install -e .

# Regenerate data
python examples/generate_sample_data.py

# Test
python examples/run_example.py
```

## Platform-Specific Notes

### Windows
- Use backslashes in paths: `configs\ma_strategy.json`
- Or use forward slashes: `configs/ma_strategy.json` (also works)
- Use `python` command (not `python3`)

### Linux/Mac
- Use forward slashes: `configs/ma_strategy.json`
- May need `python3` instead of `python`
- May need `pip3` instead of `pip`

## Still Having Issues?

Open an issue on GitHub with:
- Python version
- Operating system
- Full error message
- Steps to reproduce
- What you've tried
