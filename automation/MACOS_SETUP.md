# macOS Setup Guide - Demo Website Builder

Quick setup guide specifically for macOS users.

## Prerequisites

### 1. Check Python Installation

```bash
python3 --version
```

Should show Python 3.8 or higher. If not installed:

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11
```

### 2. (Optional) Install Qt6 for Better Performance

```bash
brew install qt@6
```

This is optional but recommended for smoother UI rendering.

## Installation

### Option 1: One-Click Setup (Recommended)

1. Open Finder
2. Navigate to `automation/` folder
3. **Double-click**: `Launch Demo Builder.command`
4. **First time only**: You'll see a security warning
   - Right-click the file
   - Click "Open"
   - Click "Open" again in the dialog
5. The app will auto-install and launch!

### Option 2: Terminal Setup

```bash
cd /Users/hug/Documents/Coding/Websiten/demo-websites/automation
chmod +x start.sh
./start.sh
```

## Troubleshooting

### "Cannot be opened because the developer cannot be verified"

This is macOS Gatekeeper security.

**Solution:**
1. Right-click `Launch Demo Builder.command`
2. Click "Open"
3. Click "Open" in the dialog

Or via terminal:
```bash
xattr -cr "/Users/hug/Documents/Coding/Websiten/demo-websites/automation/Launch Demo Builder.command"
```

### "zsh: permission denied: ./start.sh"

**Solution:**
```bash
chmod +x start.sh
chmod +x "Launch Demo Builder.command"
```

### PyQt6 Installation Fails

**Solution 1:** Install Qt6 first
```bash
brew install qt@6
pip install --upgrade --force-reinstall PyQt6 PyQt6-WebEngine
```

**Solution 2:** Use clean virtual environment
```bash
cd automation
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### App Crashes on Launch

**Solution:** Remove quarantine attributes
```bash
cd automation
xattr -cr .
xattr -cr venv/
```

### WebEngine Doesn't Display Websites

**Check if you're using the right Python:**
```bash
which python3
```

Should show:
- `/usr/bin/python3` (system Python) ✅
- `/opt/homebrew/bin/python3` (Homebrew Python) ✅
- `/Users/xxx/anaconda3/bin/python3` (Anaconda) ❌

If using Anaconda/Conda:
```bash
conda deactivate
```

Then reinstall in a fresh venv using system Python.

### Port 4321 Already in Use

Kill the process:
```bash
lsof -ti:4321 | xargs kill -9
```

## First Run

1. Launch the app (double-click .command file or run start.sh)
2. Click **"Manage Keys"** button
3. Add your Anthropic API key:
   - Name: "My Key" (or any name)
   - API Key: `sk-ant-...` (from https://console.anthropic.com/)
4. Click **"Add Key"**
5. Enter a website URL
6. Click **"Start"**!

## macOS-Specific Features

### Finder Integration

You can:
- Add `Launch Demo Builder.command` to your Dock
- Create an alias in Applications folder
- Add to Launchpad

### Keyboard Shortcuts

While app is running:
- `Cmd + Q`: Quit app
- `Cmd + W`: Close window (quits app)
- `Cmd + Tab`: Switch to/from app

### Dark Mode

The app follows your system dark mode preference automatically.

## Performance Tips

1. **Close other dev servers** on port 4321 before starting
2. **Install Qt6 via Homebrew** for better WebEngine performance:
   ```bash
   brew install qt@6
   ```
3. **Use wired connection** for faster website fetching
4. **Close heavy apps** (Docker, IDEs) during build for faster Claude API responses

## API Key Security on macOS

Your API keys are stored in:
```
automation/config.json
```

**Security recommendations:**
1. Don't share this file
2. Don't commit to git (already in .gitignore)
3. Use FileVault for disk encryption
4. Set proper file permissions:
   ```bash
   chmod 600 config.json
   ```

## Uninstalling

```bash
cd automation
rm -rf venv/
rm config.json
rm .env
```

Then delete the automation folder.

## Getting Help

- **README.md**: Full documentation
- **FEATURES.md**: Detailed feature list
- **Issues**: https://github.com/anthropics/claude-code/issues (for Claude Code issues)
- **Anthropic API**: https://console.anthropic.com/ (for API key issues)

## Quick Reference

**Start app:**
```bash
cd automation && ./start.sh
```

Or just double-click:
```
Launch Demo Builder.command
```

**Check logs:**
Build log is shown in the app UI.

**Update dependencies:**
```bash
cd automation
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

**Reset everything:**
```bash
cd automation
rm -rf venv config.json .env
./start.sh
```

Happy building! 🚀
