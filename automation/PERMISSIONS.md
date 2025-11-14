# macOS Permissions Guide

## Why Permissions Are Needed

The automated version uses **AppleScript** to:
1. Open Terminal
2. Simulate keyboard input (Cmd+T for new tab)
3. Send commands

macOS requires **Accessibility** permissions for keyboard simulation.

## Error Messages

### German (Deutsch)
```
„System Events" hat einen Fehler erhalten: osascript ist nicht berechtigt,
Tastatureingaben zu senden. (1002)
```

### English
```
System Events got an error: osascript is not allowed to send keystrokes. (1002)
```

## Solution: Grant Accessibility Permission

### Step-by-Step (macOS Ventura/Sonoma)

1. **Open System Settings** (⚙️ in Dock)

2. Click **Privacy & Security** in sidebar

3. Click **Accessibility** (Bedienungshilfen)

4. Click the **🔒 lock icon** (bottom left)
   - Enter your password

5. Click the **+ button**

6. Navigate to **one of these**:
   - `/Applications/Utilities/Terminal.app` ✅ **RECOMMENDED**
   - OR: `/Library/Frameworks/Python.framework/.../Python.app`

7. Click **Open**

8. **Enable the checkbox** next to Terminal

9. Click **🔒 lock** to prevent changes

### Visual Guide

```
System Settings
  └─ Privacy & Security
      └─ Accessibility
          └─ [🔒 Click to unlock]
              └─ [+ Add Application]
                  └─ Terminal.app ✅
```

## Testing Permissions

After granting permissions:

```bash
# Test AppleScript can control Terminal
osascript -e 'tell application "Terminal" to activate'

# If it works, Terminal will come to front
# If still fails, restart Terminal and try again
```

## Alternative: No-Permission Version

If you don't want to grant permissions, use the **Simple Version**:

```bash
cd automation
python demo_builder_simple.py
```

This version:
- ✅ No permissions needed
- ✅ Still FREE
- ⚠️ You manually copy/paste prompt to Claude

## Troubleshooting

### "Terminal not in the list"

It might already be there! Look for:
- `Terminal` or `Terminal.app`
- `Python` or `Python.app`

### "Permission granted but still error"

1. **Restart Terminal completely** (Cmd+Q)
2. **Restart the Python app**
3. Try again

### "Can't find Python.app"

Use Terminal instead! It's easier:
- Just add `/Applications/Utilities/Terminal.app`
- This gives Terminal permission to control itself

## Which Apps Need Permission?

Only **ONE** of these needs permission:

| App | Path | Notes |
|-----|------|-------|
| **Terminal** ✅ | `/Applications/Utilities/Terminal.app` | RECOMMENDED - Easiest to find |
| Python | `/Library/Frameworks/Python.framework/...` | Hard to locate |
| iTerm2 | `/Applications/iTerm.app` | If you use iTerm instead |

## Security Note

Granting Accessibility permission allows the app to:
- ✅ Send keystrokes to Terminal
- ✅ Automate Terminal commands

It does NOT allow:
- ❌ Access to other apps
- ❌ Access to your files
- ❌ System-level changes

**It's safe!** This is standard for macOS automation apps.

## Quick Fix Checklist

- [ ] Open System Settings
- [ ] Privacy & Security → Accessibility
- [ ] Unlock with 🔒 password
- [ ] Add Terminal.app with + button
- [ ] Enable checkbox
- [ ] Lock with 🔒
- [ ] Restart Terminal (Cmd+Q, then reopen)
- [ ] Run `./start.sh` again

## Still Not Working?

### Option 1: Use Simple Version (No Permissions)
```bash
python demo_builder_simple.py
```
You copy/paste manually, but no permissions needed.

### Option 2: Use API Version (Different Approach)
```bash
python demo_builder.py
```
Costs money but bypasses all permission issues.

### Option 3: Manual Workflow
1. Run app to generate prompt
2. Copy prompt
3. Open Terminal yourself
4. Run `claude`
5. Paste prompt

## Summary

**Recommended Setup:**
1. Grant Terminal → Accessibility permission (one-time)
2. Use automated version forever (free!)

**If permissions are annoying:**
1. Use simple version (still free)
2. Just copy/paste once per build

Both are free and work great! 🚀
