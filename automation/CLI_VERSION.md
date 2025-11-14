# Demo Builder - CLI Version 💰

## Why CLI Version?

**NO API COSTS!** 🎉

Instead of paying for Anthropic API calls ($0.50-$2 per demo), this version uses the **Claude Code CLI** that you already have installed. It's basically free!

## How It Works

```
PyQt6 Desktop App
    ↓
Spawns: `claude` command
    ↓
Sends prompt with workflow
    ↓
Claude Code does everything:
  - Reads/writes files
  - Runs commands
  - Creates demo site
  - Starts dev server
    ↓
App shows preview
```

## Comparison

### API Version (`demo_builder.py`)
- ❌ Costs $0.50-$2.00 per demo
- ❌ Requires API key management
- ❌ Need to track usage/costs
- ✅ Works anywhere with internet

### CLI Version (`demo_builder_cli.py`) ⭐
- ✅ **FREE** (uses your Claude Code subscription)
- ✅ No API keys needed
- ✅ No usage tracking needed
- ✅ Works exactly like chatting with me
- ✅ Same quality results
- ❌ Requires Claude Code installed

## Setup

### 1. Install Claude Code

If you don't have it:
```bash
# Check if installed
which claude

# If not found, install Claude Code
# Visit: https://docs.anthropic.com/claude/docs/claude-code
```

### 2. Run the App

```bash
cd automation
./start.sh
```

The script will:
1. Check for `claude` CLI ✅
2. Install dependencies (just PyQt6) ✅
3. Launch the app ✅

## Usage

Exactly the same as the API version:

1. **Enter URL**: Paste website URL
2. **Click Start**: Claude Code builds the demo
3. **Review**: Side-by-side preview
4. **Approve or Request Changes**
5. **Deploy** when ready

## What Claude Code Does

When you click "Start", the app runs:

```bash
cd demos
claude
```

And sends this prompt:

```
Create a new demo website following the workflow below.

Original website URL: https://www.example.com

WORKFLOW:
[Full workflow from demos/template/WORKFLOW.md]

Instructions:
1. Change directory to: demos/
2. Fetch the original website content
3. Create a new Astro project
4. Copy components from template
5. Customize everything
6. Start dev server
7. Tell me when it's ready for review
```

Claude Code then:
- ✅ Reads WORKFLOW.md
- ✅ Fetches the website
- ✅ Creates Astro project
- ✅ Copies template files
- ✅ Customizes all content
- ✅ Starts `npm run dev`
- ✅ Reports "ready for review"

## Advantages

### 1. **Cost**
- API: $0.50-$2 per demo = **$50-$200** for 100 demos
- CLI: **$0** (included in Claude Code subscription)

### 2. **No Setup**
- API: Need API key, manage keys, track usage
- CLI: Just need `claude` command

### 3. **Same Quality**
- Both use Claude Sonnet 4
- Same workflow
- Same results

### 4. **Easier Debugging**
- Can see Claude's full output
- Can interact if needed
- Same as your normal Claude Code workflow

## Technical Details

The app uses `subprocess.Popen` to run:

```python
process = subprocess.Popen(
    ["claude"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
    cwd=demos_dir
)

# Send prompt
process.stdin.write(prompt + "\n")
process.stdin.flush()

# Read output
for line in process.stdout:
    print(line)  # Show in app UI
```

When it detects `localhost:4321` in output, it knows the dev server started and shows the preview.

## Limitations

### API Version
- ✅ Works anywhere
- ❌ Costs money
- ❌ Need API key

### CLI Version
- ✅ Free
- ✅ No API key
- ❌ Requires Claude Code installed
- ❌ Only works locally (not on servers)

## Which Should You Use?

**For personal use**: CLI Version (free!)

**For production/deployment**: API Version (works anywhere)

**For this demo automation**: CLI Version all the way! 🚀

## Cost Savings Example

Building 50 demo sites:

- **API Version**: 50 × $1 = **$50**
- **CLI Version**: 50 × $0 = **$0**

**Savings: $50** 💰

## Requirements

```txt
# requirements.txt (CLI version)
PyQt6>=6.6.0
PyQt6-WebEngine>=6.6.0

# That's it! No anthropic, requests, or python-dotenv needed
```

Installation is **10x faster** (no large anthropic SDK).

## Running

```bash
# Quick start
./start.sh

# Or manually
python3 demo_builder_cli.py
```

## Troubleshooting

### "Claude CLI not found"

Install Claude Code:
```bash
# macOS/Linux
# Visit: https://docs.anthropic.com/claude/docs/claude-code
```

### "Process ended but no dev server"

Check the logs in the app. Claude might have hit an error. You can:
1. Look at the full log output
2. Manually run `claude` in the demos folder
3. Debug what went wrong

### Dev server not detected

The app looks for these strings in Claude's output:
- `localhost:4321`
- `local:`

If Claude uses different wording, we might miss it. But you can manually check `http://localhost:4321`.

## Summary

🎯 **Use CLI Version** for:
- Personal demo creation
- Cost savings
- Easier debugging
- Local development

💻 **Use API Version** for:
- Server deployment
- CI/CD pipelines
- When Claude Code not available

For your use case (creating demos locally), **CLI Version is perfect!** 💪
