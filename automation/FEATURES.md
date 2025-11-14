# Demo Website Builder - Features Overview

## What is this?

A **local desktop application** that automates the entire demo website creation process using Claude API with function calling. No web UI needed - it's a native PyQt6 app.

## Key Features

### 1. Multiple API Key Management ✨

**Why?** Switch between personal and work Anthropic accounts without editing config files.

**How it works:**
- Click "Manage Keys" → Add multiple API keys with names
- Dropdown selector to switch accounts instantly
- Keys stored in `config.json` (excluded from git for security)
- Auto-loads default key from `.env` on first run

**UI Elements:**
```
[API Key: ▼] [Manage Keys]  Active Key: Personal | Usage tracking coming soon
```

### 2. Usage Tracking Display

**Current:** Shows active key name
**Future:** Will display token usage when Anthropic adds usage API endpoint

**Note:** Anthropic doesn't currently provide a public usage API. The UI is ready for when they add it. Current display:
```
Active Key: [name] | Usage tracking coming soon
```

### 3. Automated Build Process

Claude API with function calling can:
- **read_file**: Read any local file
- **write_file**: Create new files
- **edit_file**: String replacement editing
- **run_command**: Execute bash commands
- **start_dev_server**: Launch npm dev server

**Workflow:**
1. Fetch original website
2. Extract company info
3. Create Astro project in `demos/`
4. Copy template components
5. Customize all content
6. Start dev server
7. Signal "ready for review"

### 4. Side-by-Side Preview

Before deploying, you see:
```
┌──────────────────┬──────────────────┐
│ Original Website │  Demo Website    │
│ (in iframe)      │  (localhost)     │
└──────────────────┴──────────────────┘
```

### 5. Interactive Review Loop

**Approve & Deploy:** Builds and deploys to Vercel
**Request Changes:** Natural language prompts like:
- "Make the colors more vibrant"
- "Add a contact form"
- "Use different images"
- "Fix mobile navigation"

Claude makes changes → Shows preview again → Repeat until approved

### 6. One-Click Deployment

After approval:
1. Runs `npm run build`
2. Deploys to Vercel with `vercel --prod --yes`
3. Extracts deployment URL from output
4. Shows success message

## Technical Architecture

```
┌─────────────────────────────────────────┐
│         PyQt6 Desktop App               │
│  (Multi-key selector + Usage display)   │
└────────────┬────────────────────────────┘
             │
             ▼
    ┌────────────────────┐
    │  Anthropic API     │
    │  (Claude Sonnet 4) │
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │  Function Calling  │
    │  (5 tool functions)│
    └────────┬───────────┘
             │
             ▼
    ┌────────────────────┐
    │  Local File System │
    │  + Shell Commands  │
    └────────────────────┘
```

## Security Features

1. **config.json** is gitignored (stores API keys locally only)
2. **API keys masked** in UI: `sk-ant-xxxxx...last4`
3. **Password field** when adding new keys
4. **.env support** for default key (optional)

## UI Components

### Top Bar
```
┌─────────────────────────────────────────────────────────────┐
│ API Key: [▼ Personal]  [Manage Keys]   Active: Personal... │
└─────────────────────────────────────────────────────────────┘
```

### Input Section
```
┌─────────────────────────────────────────────────────────────┐
│ Website URL: [https://www.example.com___] [Start]          │
└─────────────────────────────────────────────────────────────┘
```

### Build Log
```
┌─────────────────────────────────────────────────────────────┐
│ Build Log:                                                  │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Starting build for: https://www.example.com             │ │
│ │ Sending request to Claude...                            │ │
│ │ Iteration 1/50                                          │ │
│ │ Executing tool: read_file                               │ │
│ │ ...                                                     │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Side-by-Side Preview
```
┌───────────────────────────┬───────────────────────────────┐
│   Original Website        │     Demo Website              │
│  ┌─────────────────────┐  │   ┌─────────────────────┐     │
│  │  (WebEngine View)   │  │   │  (WebEngine View)   │     │
│  │  Original URL       │  │   │  localhost:4321     │     │
│  └─────────────────────┘  │   └─────────────────────┘     │
└───────────────────────────┴───────────────────────────────┘
```

### Review Controls
```
┌─────────────────────────────────────────────────────────────┐
│ [Approve & Deploy] [Enter changes...____] [Request Changes] │
└─────────────────────────────────────────────────────────────┘
```

## API Key Management Dialog

```
┌─────────────────────────────────────────────┐
│  Manage API Keys                      [×]   │
├─────────────────────────────────────────────┤
│  API Keys                                   │
│  ┌───────────────────────────────────────┐  │
│  │ Personal: sk-ant-xxxxx...abc4 [Remove]│  │
│  │ Work: sk-ant-xxxxx...xyz9     [Remove]│  │
│  └───────────────────────────────────────┘  │
│                                             │
│  Add New Key                                │
│  ┌───────────────────────────────────────┐  │
│  │ Name:    [________________]           │  │
│  │ API Key: [••••••••••••••••]           │  │
│  │          [Add Key]                    │  │
│  └───────────────────────────────────────┘  │
│                                             │
│                           [Close]           │
└─────────────────────────────────────────────┘
```

## Workflow Integration

The app reads `demos/template/WORKFLOW.md` and passes it to Claude as instructions. Claude follows it exactly:

1. ✅ Fetch website content
2. ✅ Extract company data
3. ✅ Create Astro project
4. ✅ Copy template
5. ✅ Customize Navigation
6. ✅ Update Hero sections
7. ✅ Configure AI Chatbot (with primaryColor!)
8. ✅ Add Footer with hours/contact
9. ✅ Use original images
10. ✅ Start dev server

## Future Enhancements

### Planned Features:
- [ ] **Real usage tracking** when Anthropic adds API endpoint
- [ ] **Cost estimation** per build
- [ ] **Build queue** for multiple concurrent projects
- [ ] **GitHub integration** (push to repo automatically)
- [ ] **Screenshot comparison** tool
- [ ] **Dark mode** UI
- [ ] **Export/import** project templates
- [ ] **Automatic Vercel alias** creation
- [ ] **Build history** with rollback

### Possible Anthropic API Features (when available):
```python
# Hypothetical future usage API
client = anthropic.Anthropic(api_key=api_key)
usage = client.usage.get()

# Display:
# "Tokens: 125,430 / 1,000,000 (12.5%)"
# "Cost this month: $4.25"
# "Remaining: $95.75"
```

## Why PyQt6 over Web UI?

1. **Native performance** - No browser overhead
2. **WebEngine built-in** - Chromium-based preview
3. **Desktop integration** - System notifications, file dialogs
4. **No server needed** - No port conflicts with dev servers
5. **Offline-capable** - Works without internet (except API calls)
6. **Better file access** - Direct filesystem operations

## Cost Estimation

Using Claude Sonnet 4:
- **New demo**: ~$0.50 - $2.00 (depending on complexity)
- **Change request**: ~$0.10 - $0.50 each
- **Average**: ~$1.00 per complete demo with 1-2 revisions

## Security Notes

⚠️ **Important:**
- `config.json` contains plaintext API keys
- Stored locally only (gitignored)
- Never commit `config.json` or `.env`
- Use file system permissions to protect config.json
- Consider encrypting config.json for production use

## Getting Started

```bash
cd automation
./start.sh
```

That's it! The app will:
1. Create virtual environment
2. Install dependencies
3. Load/create config.json
4. Open the GUI

Add your API key and start building! 🚀
