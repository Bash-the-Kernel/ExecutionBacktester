@echo off
REM Windows batch script to run backtests

echo ExecutionBacktester - Quick Run Script
echo ======================================
echo.

if "%1"=="" (
    echo Usage: run_backtest.bat [ma^|breakout^|ml^|example]
    echo.
    echo Options:
    echo   ma        - Run moving average strategy
    echo   breakout  - Run breakout strategy
    echo   ml        - Run ML strategy
    echo   example   - Run example script
    echo   data      - Generate sample data
    echo   test      - Run tests
    echo.
    exit /b 1
)

if "%1"=="ma" (
    echo Running Moving Average Strategy...
    python -m backtester.cli configs\ma_strategy.json
    exit /b 0
)

if "%1"=="breakout" (
    echo Running Breakout Strategy...
    python -m backtester.cli configs\breakout_strategy.json
    exit /b 0
)

if "%1"=="ml" (
    echo Running ML Strategy...
    python -m backtester.cli configs\ml_strategy.json
    exit /b 0
)

if "%1"=="example" (
    echo Running Example Script...
    cd examples
    python run_example.py
    cd ..
    exit /b 0
)

if "%1"=="data" (
    echo Generating Sample Data...
    cd examples
    python generate_sample_data.py
    cd ..
    exit /b 0
)

if "%1"=="test" (
    echo Running Tests...
    pytest tests\ -v
    exit /b 0
)

echo Unknown option: %1
exit /b 1
