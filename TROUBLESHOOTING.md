# TROUBLESHOOTING GUIDE - HKBU GenAI Integration

## ✅ Quick Fixes

### Problem: Invalid Ticker Error
```
'ticker': '"D:/Pycharm project/TradingAgents/.venv/Scripts/activate.bat"'
OSError: [WinError 123] 文件名、目录名或卷标语法不正确
```

**Cause**: Accidentally pasting a file path instead of ticker symbol

**Solution**: 
1. When prompted for ticker, just type the symbol (e.g., `SPY`, `AAPL`)
2. Or simply press Enter to use the default (`SPY`)
3. Don't paste paths or filenames

**Validation Added**: The CLI now validates ticker input and rejects:
- File paths (`C:\...`, `/usr/...`)
- File extensions (`.bat`, `.exe`, `.ps1`)
- Special characters except `.` and `-`

---

### Problem: Python Cache Issues
```
ValueError: Unsupported LLM provider
NameError: name 're' is not defined
```

**Cause**: Python is using old cached bytecode

**Solution**: Always use `RUN_CLI.bat` which clears cache automatically

**Manual Fix**:
```powershell
Get-ChildItem -Path . -Include __pycache__,*.pyc -Recurse -Force | Remove-Item -Recurse -Force
python -m cli.main
```

---

### Problem: Import Errors
```
ModuleNotFoundError: No module named 'xxx'
```

**Solution**: Install missing dependencies
```powershell
pip install -r requirements.txt
```

Or use uv:
```powershell
uv pip install -r requirements.txt
```

---

### Problem: Unicode/Encoding Errors
```
UnicodeEncodeError: 'gbk' codec can't encode character
```

**Cause**: Windows console doesn't support emoji characters

**Solution**: Use the Windows-compatible test:
```powershell
python test_hkbu_win.py
```

Instead of:
```powershell
python test_hkbu_integration.py
```

---

### Problem: API Authentication Errors
```
401 Unauthorized
403 Forbidden
```

**Solution**: Verify API key in `.env`:
```properties
AZURE_OPENAI_API_KEY=30b041fb-3d53-46f9-8558-628c648d14d8
AZURE_OPENAI_ENDPOINT=https://genai.hkbu.edu.hk/api/v0/rest
AZURE_API_VERSION=2024-12-01-preview
```

---

### Problem: Model Not Found
```
Error code: 400 - Configuration for model 'gpt-4o-mini' is not available
```

**Cause**: Using OpenAI model names instead of HKBU deployment names

**Solution**: Use HKBU models:
- ✅ `gpt-4.1-mini`, `gpt-4o`, `o1`, `gpt-5`
- ❌ `gpt-4o-mini`, `gpt-3.5-turbo`

**Full HKBU Model List**:

Quick-Thinking:
- `gpt-4.1-nano`
- `gpt-4.1-mini` ⭐ Recommended
- `gpt-4o`

Deep-Thinking:
- `gpt-5`
- `gpt-4.1`
- `o1` ⭐ Recommended
- `o3-mini`
- `qwen3-max`
- `deepseek-v3`
- `deepseek-r1`

---

## 🔍 Diagnostic Commands

### Check Python Environment
```powershell
python --version
python -c "import sys; print(sys.executable)"
```

### Verify CLI Loads
```powershell
python -c "from cli.main import get_user_selections; print('OK')"
```

### Test Provider Normalization
```powershell
python test_hkbu_win.py
```

### Test Ticker Validation
```powershell
python test_ticker_validation.py
```

### Check Environment Variables
```powershell
python -c "import os; print('Endpoint:', os.getenv('AZURE_OPENAI_ENDPOINT')); print('Key:', 'SET' if os.getenv('AZURE_OPENAI_API_KEY') else 'NOT SET')"
```

---

## 📋 Pre-Flight Checklist

Before running the CLI, verify:

- [ ] Python 3.13+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file exists with HKBU credentials
- [ ] Using `RUN_CLI.bat` (clears cache)
- [ ] Know which ticker to analyze (e.g., SPY)
- [ ] Understand model options (gpt-4.1-mini + o1)

---

## 🎯 Common User Errors

### Error: Pasting Full Command Instead of Ticker

**Wrong**:
```
[SPY]: python -m cli.main
```

**Right**:
```
[SPY]: SPY
```
Or just press Enter for default.

---

### Error: Using Wrong Provider

**Wrong**: Selecting "OpenAI" when you want HKBU

**Right**: Select "HKBU GenAI (Azure Compatible)"

---

### Error: Not Clearing Cache

**Wrong**: Running `python -m cli.main` directly after code changes

**Right**: Running `RUN_CLI.bat` which clears cache first

---

## 🛠️ Advanced Troubleshooting

### Check What Python Module is Loaded
```powershell
python -c "import cli.main; print(cli.main.__file__)"
```

### Force Reimport
```powershell
python -c "import sys; sys.path.insert(0, '.'); import importlib; import cli.main; importlib.reload(cli.main); print('Reloaded')"
```

### Check Imports in File
```powershell
python -c "with open('cli/main.py', 'r', encoding='utf-8') as f: lines = f.readlines(); print([l.rstrip() for l in lines[:10]])"
```

### Verify Ticker Validation Code
```powershell
python -c "import inspect; from cli.main import get_ticker; print(inspect.getsource(get_ticker))"
```

---

## 📞 Getting Help

If issues persist:

1. **Run full diagnostic**:
   ```powershell
   python test_hkbu_win.py
   python test_ticker_validation.py
   ```

2. **Check documentation**:
   - `HKBU_INTEGRATION_GUIDE.md` - Full setup
   - `QUICK_START.txt` - Quick reference

3. **Verify setup**:
   - API key correct in `.env`
   - Python version 3.13+
   - All dependencies installed

4. **Clean reinstall**:
   ```powershell
   pip uninstall -y -r requirements.txt
   pip install -r requirements.txt
   ```

---

## ✅ Success Indicators

You'll know it's working when:

- ✅ CLI starts without errors
- ✅ Provider shows "HKBU GenAI (Azure Compatible)"
- ✅ Debug output shows `Mapped to: 'azure'`
- ✅ Ticker validation accepts `SPY` but rejects paths
- ✅ Models list shows HKBU deployments
- ✅ Analysis runs without authentication errors

---

## 🎓 Tips for Students

1. **Always use default ticker (SPY)** for testing - just press Enter
2. **Don't paste** - type tickers manually or use default
3. **Use RUN_CLI.bat** - it handles cache automatically
4. **Pick recommended models**: gpt-4.1-mini + o1
5. **Check QUICK_START.txt** for quick reference

---

**Last Updated**: October 14, 2025  
**Version**: TROUBLESHOOTING_V1.0
