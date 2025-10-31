# Setup Guide - Context Retrieval Script for Germany's 1. Bundesliga Coach RAG-Chatbot

This guide provides detailed setup instructions for both **venv** and **pipenv** workflows.

## Prerequisites

Before you begin, ensure you have:

- Python 3.8 or higher installed
- Git installed
- Internet connection (for API access)
- Command-line/terminal access

### Check Python Version

```bash
python --version
# or
python3 --version
```

Should output: `Python 3.8.x` or higher

## Setup Method 1: Using venv (Standard)

### Step-by-Step Instructions

1. **Clone the repository**
   ```bash
   git clone <https://github.com/apollosbangalu/bundesliga-coach-rag-chatbot>
   cd bundesliga-coach-rag-chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```
   
   This creates a `venv` directory containing the virtual environment.

3. **Activate virtual environment**
   
   **On Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```
   
   **On Windows (Command Prompt):**
   ```bash
   venv\Scripts\activate.bat
   ```
   
   **On Windows (PowerShell):**
   ```bash
   venv\Scripts\Activate.ps1
   ```
   
   Your prompt should now show `(venv)` prefix.

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Deactivate when done**
   ```bash
   deactivate
   ```

### Troubleshooting venv

**Issue**: `python: command not found`
- Try `python3` instead of `python`

**Issue**: Virtual environment activation fails on Windows PowerShell
- Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Then retry activation

**Issue**: `pip: command not found`
- Ensure pip is installed: `python -m ensurepip --upgrade`

## Setup Method 2: Using pipenv (Recommended)

### Why pipenv?

- Automatic virtual environment management
- Better dependency resolution
- Security vulnerability scanning
- Deterministic builds with lock file
- Easier collaboration

### Step-by-Step Instructions

1. **Install pipenv** (if not already installed)
   ```bash
   pip install pipenv
   # or
   pip3 install pipenv
   ```

2. **Clone the repository**
   ```bash
   git clone <https://github.com/apollosbangalu/bundesliga-coach-rag-chatbot>
   cd bundesliga-coach-rag-chatbot
   ```

3. **Install dependencies**
   ```bash
   pipenv install
   ```
   
   This command:
   - Creates a virtual environment automatically
   - Installs all dependencies from Pipfile
   - Generates Pipfile.lock for reproducible builds

4. **Run the application**
   
   **Option A: Direct execution (recommended for single commands)**
   ```bash
   pipenv run python main.py
   ```
   
   **Option B: Activate shell first**
   ```bash
   pipenv shell
   python main.py
   # When done:
   exit
   ```

### Additional pipenv Commands

**Check installed packages:**
```bash
pipenv graph
```

**Update dependencies:**
```bash
pipenv update
```

**Install new package:**
```bash
pipenv install package-name
```

**Check for security vulnerabilities:**
```bash
pipenv check
```

**Remove virtual environment:**
```bash
pipenv --rm
```

**Get virtual environment location:**
```bash
pipenv --venv
```

### Troubleshooting pipenv

**Issue**: `pipenv: command not found`
- Ensure pipenv is installed: `pip install --user pipenv`
- Add to PATH if needed

**Issue**: Pipenv creates environment in unexpected location
- Set environment variable: `export PIPENV_VENV_IN_PROJECT=1`
- This creates `.venv` in project directory

**Issue**: Installation is slow
- pipenv does dependency resolution which can take time
- Use `pipenv install --skip-lock` for faster installs (development only)

## Optional: Installing wikipedia-api Library

If you encounter Wikipedia API 403 errors:

**Using venv:**
```bash
# Activate venv first
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install wikipedia-api
```

**Using pipenv:**
```bash
pipenv install wikipedia-api
```

Then modify `main.py` line 13:
```python
from src.wikipedia_client_alternative import WikipediaClient
```

## Verification

After installation, verify the setup:

1. **Run the application:**
   ```bash
   # venv
   python main.py
   
   # pipenv
   pipenv run python main.py
   ```

2. **You should see:**
   ```
   ============================================================
   Bundesliga Coach Information System
   ============================================================
   
   Initializing system (retrieving Bundesliga clubs data)...
   System ready!
   ```

3. **Test with a query:**
   ```
   Your question: Who is coaching Berlin?
   ```

4. **Expected output:**
   - A complete LLM prompt with system instructions
   - Retrieved context about the club and coach
   - No error messages

## Environment Comparison

| Aspect | venv | pipenv |
|--------|------|--------|
| Installation | Built-in | Requires pip install |
| Setup Command | `python -m venv venv` | `pipenv install` |
| Activation | Manual (`source venv/bin/activate`) | Automatic or `pipenv shell` |
| Run Command | `python main.py` | `pipenv run python main.py` |
| Dependencies | requirements.txt | Pipfile + Pipfile.lock |
| Lock File | No | Yes (reproducible builds) |
| Dependency Updates | Manual | `pipenv update` |
| Security Checks | Manual | `pipenv check` |
| Team Collaboration | Requires documentation | Self-documenting |

## Best Practices

### For venv Users:

1. Always activate the virtual environment before running
2. Keep requirements.txt updated: `pip freeze > requirements.txt`
3. Use `.gitignore` to exclude venv directory
4. Document Python version requirements

### For pipenv Users:

1. Commit both `Pipfile` and `Pipfile.lock` to git
2. Use `pipenv install` for new team members
3. Run `pipenv check` regularly for security
4. Use `pipenv run` for one-off commands
5. Use `pipenv shell` for longer development sessions

## Next Steps

After successful setup:

1. Read the main [README.md](README.md) for usage instructions
2. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if you encounter issues
3. Review the example queries in the console output
4. Explore the code in the `src/` directory

## Getting Help

If you encounter issues:

1. Check logs in `logs/bundesliga_rag_YYYYMMDD.log`
2. Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. Ensure Python version is 3.8 or higher
4. Verify internet connection is active
5. Try the alternative Wikipedia client if API issues persist

## Common Issues

### Issue: Import errors

**Cause**: Dependencies not installed or wrong environment active

**Solution**:
- venv: Ensure activated and run `pip install -r requirements.txt`
- pipenv: Run `pipenv install` again

### Issue: Permission denied

**Cause**: Insufficient permissions to create virtual environment

**Solution**:
- Use `--user` flag: `pip install --user pipenv`
- Or run with appropriate permissions

### Issue: Network timeouts

**Cause**: Firewall or proxy blocking API access

**Solution**:
- Check firewall settings
- Configure proxy if needed
- Verify https://query.wikidata.org/ is accessible

## Development Setup

For contributing or development:

**Using venv:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pytest black flake8  # Development tools
```

**Using pipenv:**
```bash
pipenv install --dev
pipenv shell
```

Add development dependencies to Pipfile:
```toml
[dev-packages]
pytest = "*"
black = "*"
flake8 = "*"
```

---

**Ready to start?** Jump to [Quick Start](README.md#quick-start) in the main README!