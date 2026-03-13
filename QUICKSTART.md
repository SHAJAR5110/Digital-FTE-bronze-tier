# Bronze Tier - Quick Start Guide

**Status**: Ready to use
**Setup Time**: ~5 minutes

## What You Have

- ✓ Obsidian vault with Dashboard and Company Handbook
- ✓ FileSystem Watcher script (monitors ~/Downloads)
- ✓ Claude Code integration ready
- ✓ Basic automation patterns established

## Quick Test (5 minutes)

### Step 1: Run the Watcher
```bash
cd /c/Users/HP/Desktop/H/FTEs/Bronze\ Tier
python3 watchers/filesystem_watcher.py
```

Expected output:
```
2026-03-12 19:23:05,645 - FileSystemWatcher - INFO - Monitoring folder: C:\Users\HP\Downloads
```

### Step 2: Drop a Test File
1. Create a test file in your Downloads folder (e.g., `test.txt`)
2. Save it to `~/Downloads`

### Step 3: Check Needs_Action
```bash
ls AI_Employee_Vault/Needs_Action/
```

You should see a new file like: `FILE_test.md`

### Step 4: Run Claude to Process
In a new terminal:
```bash
cd /c/Users/HP/Desktop/H/FTEs/Bronze\ Tier
claude code AI_Employee_Vault
```

In Claude, type:
```
Read the /Needs_Action folder and summarize what you find.
Create a Plan.md file in /Plans with next steps.
```

### Step 5: Verify
```bash
ls AI_Employee_Vault/Plans/
```

You should see a new `Plan_*.md` file with Claude's analysis.

## File Structure

```
Bronze Tier/
├── CLAUDE.md                    # Tier-specific guidance
├── QUICKSTART.md               # This file
├── README.md                   # Full documentation
├── test_setup.py               # Verification script
├── AI_Employee_Vault/          # Obsidian vault
│   ├── Dashboard.md            # Status dashboard
│   ├── Company_Handbook.md     # Rules of engagement
│   ├── Inbox/                  # Incoming items
│   ├── Needs_Action/           # Items for Claude
│   ├── Plans/                  # Claude's plans
│   ├── Done/                   # Completed items
│   └── References/             # Knowledge base
└── watchers/                   # Python watcher scripts
    ├── base_watcher.py         # Base class for all watchers
    └── filesystem_watcher.py   # Watches ~/Downloads
```

## Common Commands

### Test the setup
```bash
python3 test_setup.py
```

### Start the FileSystem Watcher
```bash
python3 watchers/filesystem_watcher.py
```

### Run Claude on the vault
```bash
claude code AI_Employee_Vault
```

### View pending items
```bash
cat AI_Employee_Vault/Needs_Action/*
```

### View Claude's plans
```bash
cat AI_Employee_Vault/Plans/*
```

## Next Steps

1. **Customize Company_Handbook.md**: Update rules to match your preferences
2. **Test multiple cycles**: Drop files, let Claude process, review results
3. **Adjust Watcher**: Change watch folder from `~/Downloads` to something else if desired
4. **Review Plans**: See what Claude creates and adjust prompts
5. **When ready**: Move to Silver Tier for multiple Watchers + MCP servers

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Watcher not detecting files | Check file was saved to correct folder |
| Claude can't read vault | Verify vault path is correct in commands |
| Files not appearing in Plans | Claude might need different prompt, check Needs_Action first |
| Permission errors | Ensure write permissions on vault folders |

## Configuration

### Change Watch Folder
Edit `watchers/filesystem_watcher.py`:
```python
WATCH_FOLDER = "~/Downloads"  # Change this path
```

### Change Check Interval
```python
watcher = FileSystemWatcher(VAULT_PATH, WATCH_FOLDER, check_interval=30)
#                                                    ^^ Change from 30 seconds
```

## Key Concepts

**Watcher**: Continuously monitors a folder for new files, creates action items
**Vault**: Obsidian markdown folders (Needs_Action, Plans, Done, etc.)
**Claude Code**: Processes items from Needs_Action, creates Plans
**Dashboard**: Your status hub (update manually or via Claude)
**Company Handbook**: Rules that guide Claude's behavior

## Success Criteria

Bronze Tier is complete when:
1. Watcher reliably creates files in /Needs_Action
2. Claude successfully reads vault and creates Plan files
3. You can manually move items from Plans → Done
4. Dashboard can be updated (manually or by Claude)
5. End-to-end cycle works: File drop → Watcher → Claude → Plan

---

Ready to go! Start with the 5-minute test above.
