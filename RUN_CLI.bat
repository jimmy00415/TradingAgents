@echo off
REM TradingAgents CLI Runner - Ensures fresh Python cache
echo ============================================================
echo TradingAgents CLI - HKBU GenAI Edition
echo ============================================================
echo.
echo [INFO] Clearing Python cache for fresh execution...
REM Kill any running Python processes for this project
taskkill /F /FI "WINDOWTITLE eq *TradingAgents*" /IM python.exe 2>nul
if exist cli\__pycache__ rmdir /s /q cli\__pycache__ 2>nul
if exist tradingagents\__pycache__ rmdir /s /q tradingagents\__pycache__ 2>nul
if exist tradingagents\graph\__pycache__ rmdir /s /q tradingagents\graph\__pycache__ 2>nul
if exist tradingagents\agents\__pycache__ rmdir /s /q tradingagents\agents\__pycache__ 2>nul
if exist tradingagents\dataflows\__pycache__ rmdir /s /q tradingagents\dataflows\__pycache__ 2>nul
REM Clear any .pyc files
del /s /q *.pyc 2>nul
echo [OK] Cache cleared.
echo.
echo [INFO] Verifying Python environment...
python --version
echo.
echo [INFO] Starting TradingAgents CLI...
echo.
echo ============================================================
echo                     IMPORTANT TIPS
echo ============================================================
echo  1. For ticker: Just press ENTER to use SPY (recommended)
echo  2. Don't paste paths or filenames - type ticker only
echo  3. Valid tickers: SPY, AAPL, MSFT, TSLA, BRK.B, etc.
echo  4. See TICKER_INPUT_GUIDE.txt for more help
echo ============================================================
echo.
python -m cli.main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================================
    echo [ERROR] CLI exited with error code %ERRORLEVEL%
    echo ============================================================
)

pause
