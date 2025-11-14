# Fully Automated Demo Builder 🤖

## What Changed?

Instead of copying/pasting, the app now **fully automates** everything using AppleScript!

## How It Works

### What You Do:
1. Enter website URL
2. Click "🚀 Start Building"
3. Wait and watch!

### What Happens Automatically:
1. ✅ App generates the prompt
2. ✅ Opens Terminal (or new tab)
3. ✅ Changes to `demos/` directory
4. ✅ Runs `claude` command
5. ✅ Sends the prompt automatically
6. ✅ Monitors for completion
7. ✅ Shows preview when ready

**You literally just enter URL and click Start!** 🎉

## Technical Details

The app uses **AppleScript** to control Terminal:

```applescript
tell application "Terminal"
    activate

    -- Create new tab
    tell application "System Events" to keystroke "t" using command down

    -- Change directory
    do script "cd /path/to/demos"

    -- Run claude
    do script "claude"

    -- Send prompt
    do script "$(cat /tmp/claude_demo_prompt.txt)"
end tell
```

This:
- Opens Terminal app
- Creates new tab (or window if none exist)
- Runs `cd demos/`
- Runs `claude`
- Sends the full prompt

Then the app monitors the `demos/` folder for:
- New projects created
- Dev server starting on port 4321

When detected → Shows preview automatically!

## Running

```bash
cd automation
./start.sh
```

The app opens with:
- Big green "Start Building" button
- Instructions panel
- Build status log
- Side-by-side preview (appears when ready)
- Deploy button (appears when ready)

## Workflow

### Step 1: Enter URL
```
Website URL: [https://www.example.com___________] [🚀 Start Building]
```

### Step 2: Click Start Building

App does:
```
🚀 Starting automated build...
📍 URL: https://www.example.com
💾 Prompt generated and saved
🖥️  Opening Terminal with Claude Code...
✅ Terminal opened successfully!
✅ Claude Code started automatically!
✅ Prompt sent to Claude!
📺 Watch the Terminal window to see Claude working...
⏳ Monitoring for project completion...
```

### Step 3: Watch Terminal

A Terminal window/tab opens showing:
```
claude

I'll help you create this demo website...
[Claude Code output]
```

### Step 4: Automatic Preview

When Claude finishes and starts the dev server:
```
🎉 BUILD COMPLETE!
📦 Project: example-com
🚀 Dev server: http://localhost:4321
```

Preview appears automatically showing original vs demo!

### Step 5: Deploy

Click "✅ Approve & Deploy to Vercel" → Done!

## Advantages

### Before (Manual):
1. Enter URL
2. Click Generate
3. Click Copy
4. Open Terminal manually
5. Type `claude` manually
6. Paste prompt
7. Wait
8. App monitors

**~8 steps**

### Now (Automated):
1. Enter URL
2. Click Start

**2 steps!** 🎉

## Requirements

- ✅ macOS (AppleScript)
- ✅ Terminal app
- ✅ `claude` command installed
- ✅ PyQt6 (auto-installed)

No API keys needed! ✅

## Cost

**$0** - Uses your Claude Code subscription

## File Structure

```
automation/
├── demo_builder_auto.py  ⭐ FULLY AUTOMATED VERSION
├── demo_builder_simple.py  (manual copy/paste)
├── demo_builder_cli.py     (attempted automation - didn't work well)
├── demo_builder.py         (API version - costs money)
├── start.sh               (launches auto version)
└── ...
```

## What Makes It Reliable?

### AppleScript Advantages:
1. **Native macOS integration** - Terminal control
2. **Keystroke simulation** - Cmd+T for new tab
3. **Command execution** - `do script`
4. **Timing control** - `delay` commands

### Monitoring Strategy:
1. Watches `demos/` folder every 2 seconds
2. Detects new directories
3. Checks port 4321 for dev server
4. Finds newest project by modification time
5. Triggers preview when server detected

## Debugging

If Terminal doesn't open:
- Grant Terminal permission in System Preferences
- Check AppleScript execution permissions

If prompt doesn't send:
- Check `/tmp/claude_demo_prompt.txt` exists
- Manually run: `cat /tmp/claude_demo_prompt.txt`

If monitoring doesn't work:
- Check `demos/` directory exists
- Ensure dev server uses port 4321
- Look for process on port: `lsof -ti:4321`

## Comparison: All Versions

| Version | Automation | Cost | Reliability |
|---------|-----------|------|-------------|
| `demo_builder.py` | Full | $$$$ | High |
| `demo_builder_cli.py` | Attempted | Free | Low |
| `demo_builder_simple.py` | Partial | Free | Medium |
| `demo_builder_auto.py` ⭐ | **Full** | **Free** | **High** |

## Example Session

```
🤖 Welcome to Demo Builder!

[Enter URL: https://www.piel-schuett-gmbh.de/]
[Click: 🚀 Start Building]

🚀 Starting automated build...
📍 URL: https://www.piel-schuett-gmbh.de/
💾 Prompt generated and saved
🖥️  Opening Terminal with Claude Code...
✅ Terminal opened successfully!
✅ Claude Code started automatically!
✅ Prompt sent to Claude!

[Terminal window appears showing Claude working]

👀 Monitoring demos folder for new projects...
📦 New project detected: piel-schuett-gmbh-de
🚀 Dev server detected on port 4321!

🎉 BUILD COMPLETE!
📦 Project: piel-schuett-gmbh-de
🚀 Dev server: http://localhost:4321

[Preview appears automatically]

[Review the site]
[Click: ✅ Approve & Deploy to Vercel]

🚀 Deploying to Vercel...
📦 Building project...
✅ Build successful!
☁️  Deploying to Vercel...
✅ Deployed: https://piel-schuett-gmbh-de.vercel.app

🎉 Deployment complete!
```

**Total time**: 3-5 minutes (depending on site complexity)
**Total cost**: $0
**Total effort**: 2 clicks

## Summary

This is the **perfect balance**:
- ✅ **Free** (no API costs)
- ✅ **Fully automated** (2 clicks)
- ✅ **Reliable** (AppleScript + monitoring)
- ✅ **Visible** (see Claude working in Terminal)
- ✅ **Interactive** (can interrupt if needed)

**This is the version you should use!** 🚀
