# Demo Website Builder - Automation Tool

Local desktop application that automates the creation of demo websites.

## 🎯 Versions Available

### 🤖 Fully Automated Version (RECOMMENDED) ⭐⭐⭐
- **100% automated** - Just enter URL and click Start!
- Uses AppleScript to open Terminal and run Claude automatically
- **FREE** - No API costs
- File: `demo_builder_auto.py`
- See: [AUTO_VERSION.md](AUTO_VERSION.md)
- **→ Run with: `./start.sh`**

### 📋 Simple Version (Manual Copy/Paste)
- Generates prompt, you paste it to Claude
- **FREE** - No API costs
- File: `demo_builder_simple.py`

### 💳 API Version (For Servers/CI/CD)
- Uses Anthropic API directly
- Costs ~$0.50-$2 per demo
- Works anywhere
- File: `demo_builder.py`

**For personal use: Use Automated Version!** 🤖

## Features

✅ **Automated Website Creation**: Enter a URL, Claude builds the entire demo site following the workflow
✅ **Multiple API Keys**: Add and switch between different Anthropic accounts
✅ **Usage Tracking**: Monitor API usage for active key (displayed in real-time)
✅ **Side-by-Side Preview**: Compare original vs demo site before deployment
✅ **Interactive Review**: Approve or request changes with natural language
✅ **File System Access**: Claude can read, write, edit files and run commands locally
✅ **Dev Server Integration**: Automatic preview with live reload
✅ **Vercel Deployment**: One-click deployment after approval

## Architecture

```
PyQt6 Desktop App
    ↓
Anthropic API (Claude Sonnet 4)
    ↓
Function Calling → Python Tools → Local File System
    ↓
Dev Server → Preview → Review → Deploy
```

## Setup

### 1. Install Dependencies

```bash
cd automation
pip install -r requirements.txt
```

### 2. Configure API Key

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

Get your API key from: https://console.anthropic.com/

### 3. Run the App

**macOS - Option 1: Double-Click (Easiest)**

Just double-click the file:
```
automation/Launch Demo Builder.command
```

(First time: Right-click → Open → "Open" to bypass security warning)

**macOS - Option 2: Terminal**
```bash
cd automation
chmod +x start.sh
./start.sh
```

**macOS - Option 3: Manual**
```bash
cd automation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python demo_builder.py
```

**macOS Notes:**
- The app requires Python 3.8+ (comes with macOS)
- Optional but recommended: `brew install qt@6` for better performance
- If you get permission errors, run: `xattr -cr .` in the automation folder
- First time launching .command file: Right-click → Open (to bypass Gatekeeper)

## Usage

### Managing API Keys

The app supports multiple API keys for switching between different Anthropic accounts.

**First Time Setup:**
1. Click **"Manage Keys"** button
2. Enter a name (e.g., "Personal", "Work Account")
3. Paste your API key
4. Click **"Add Key"**

**Switching Accounts:**
- Use the dropdown at the top to switch between configured API keys
- Current usage is displayed on the right: `Active Key: [name] | Usage tracking coming soon`

**Note:** API keys are stored in `automation/config.json` (excluded from git).

### Creating a New Demo

1. **Select API Key**: Choose from the dropdown (or add one if none exists)
2. **Enter URL**: Paste the original website URL (e.g., `https://www.example.com`)
3. **Click Start**: Claude will:
   - Fetch the original website
   - Create new Astro project
   - Copy template components
   - Customize everything (colors, content, images, chatbot)
   - Start dev server
3. **Review**: Side-by-side comparison opens
   - Left: Original website
   - Right: Demo website (http://localhost:4321)
4. **Approve or Request Changes**:
   - Click **Approve & Deploy** → Builds and deploys to Vercel
   - Enter change request → Claude makes changes → Review again

### Example Change Requests

- "Make the colors more vibrant"
- "Add a contact form to the homepage"
- "Use different images from the original site"
- "Fix the mobile navigation"
- "Update the chatbot welcome message"

## How It Works

### Function Calling Tools

Claude has access to these tools:

1. **read_file(path)** - Read any file
2. **write_file(path, content)** - Create new files
3. **edit_file(path, old_string, new_string)** - Edit existing files
4. **run_command(command, cwd)** - Execute shell commands
5. **start_dev_server(project_path)** - Start npm dev server

### Workflow

Claude follows the workflow from `demos/template/WORKFLOW.md`:

1. Fetch original website content
2. Extract company info (name, address, phone, email, hours, colors)
3. Create new Astro project in `demos/`
4. Copy template components
5. Customize:
   - Navigation
   - Hero sections
   - Services
   - Contact info
   - Footer (with opening hours)
   - AI Chatbot (with primaryColor, businessType, custom forms)
   - Images from original site
6. Start dev server
7. Report ready for review

### API Usage

The app uses:
- **Model**: `claude-sonnet-4-20250514`
- **Max tokens**: 8000 per request
- **Tools**: Function calling for file/command operations
- **Conversation loop**: Up to 50 iterations

## Troubleshooting

### API Key Error

```
ANTHROPIC_API_KEY not found in .env file
```

Solution: Create `.env` file with your API key

### Port Already in Use

If dev server fails to start (port 4321 in use):

```bash
# Kill process on port 4321
lsof -ti:4321 | xargs kill -9
```

### PyQt6 Installation Issues (macOS)

**If installation fails:**
```bash
# Install Qt6 via Homebrew first
brew install qt@6

# Then reinstall PyQt6
pip install --upgrade --force-reinstall PyQt6 PyQt6-WebEngine
```

**If app crashes on launch:**
```bash
# Remove quarantine attributes (macOS security)
cd automation
xattr -cr .
xattr -cr venv/

# Or reinstall in a clean venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**If WebEngine doesn't load:**
```bash
# Ensure you're using system Python or Homebrew Python
which python3
# Should show: /usr/bin/python3 or /opt/homebrew/bin/python3

# NOT Anaconda/Conda (can cause Qt issues)
# If using conda, deactivate it first:
conda deactivate
```

### Claude Creates Wrong Project Name

The app detects the newest folder in `demos/`. If detection fails:
- Check that project was created in `demos/`
- Check build log for errors

## File Structure

```
automation/
├── demo_builder.py              # Main application (PyQt6)
├── requirements.txt             # Python dependencies
├── start.sh                    # Quick start script (Terminal)
├── Launch Demo Builder.command  # Double-click launcher (macOS Finder)
├── .env                        # API key (optional, for default)
├── .env.example                # Template
├── config.json                 # API keys storage (auto-created, gitignored)
├── .gitignore                  # Excludes config.json and .env
├── README.md                   # This file
└── FEATURES.md                 # Detailed features documentation

demos/
├── template/           # Template components
│   ├── WORKFLOW.md     # Build instructions for Claude
│   └── src/
│       ├── components/ # Reusable components
│       ├── layouts/
│       └── pages/
└── [generated-demos]/  # Created by the tool
```

**config.json** stores multiple API keys:
```json
{
  "api_keys": [
    {"name": "Personal", "key": "sk-ant-..."},
    {"name": "Work", "key": "sk-ant-..."}
  ],
  "active_key_index": 0
}
```

## Limitations

- **Port 4321**: Dev server uses fixed port (Astro default)
- **One build at a time**: Can't run multiple builds simultaneously
- **Local only**: Files are created locally, not on GitHub
- **Manual deployment alias**: After deploy, you may need to create Vercel alias manually

## Future Enhancements

- [ ] GitHub integration (push to repo)
- [ ] Multiple dev servers (dynamic port allocation)
- [ ] Build queue (multiple projects)
- [ ] Dark mode UI
- [ ] Export/import project templates
- [ ] Automatic Vercel alias creation
- [ ] Screenshot comparison tool

## Cost Estimation

Using Claude Sonnet 4:
- ~$0.50 - $2.00 per demo website (depending on complexity and iterations)
- Change requests: ~$0.10 - $0.50 each

## License

MIT
