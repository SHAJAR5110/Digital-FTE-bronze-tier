# Bronze Tier: Digital FTE Foundation

**Status**: ✓ Complete and Ready to Use
**Estimated Time**: 8-12 hours (setup complete)
**Goal**: Build the foundation for autonomous AI agents managing personal affairs

## Overview

Bronze Tier establishes the core infrastructure for a Digital FTE. It consists of:

1. **Obsidian Vault**: Local markdown-based memory and dashboard
2. **FileSystem Watcher**: Python script monitoring ~/Downloads for files
3. **Claude Code Integration**: Terminal-based reasoning engine
4. **Basic Automation**: File detection → Claude processing → Planning

This tier demonstrates the "Perception → Reasoning → Action" architecture in its simplest form.

## What's Included

### ✓ Obsidian Vault Structure
```
AI_Employee_Vault/
├── Dashboard.md           # Real-time status dashboard
├── Company_Handbook.md    # Rules and guidelines for Claude
├── Inbox/                 # All incoming items
├── Needs_Action/          # Items awaiting Claude processing
├── Plans/                 # Claude's action plans with checkboxes
├── Done/                  # Completed items
└── References/            # Optional knowledge base
```

### ✓ FileSystem Watcher (Python)
- Monitors ~/Downloads folder every 30 seconds
- Creates markdown action files in /Needs_Action
- Includes file metadata (name, size, date, path)
- Implements BaseWatcher pattern for extensibility

### ✓ Claude Code Integration
- Claude reads /Needs_Action folder
- Claude creates /Plans with next steps
- Manual approval and execution workflow
- Human maintains control of all actions

### ✓ Documentation
- **CLAUDE.md**: Tier-specific architecture and guidelines
- **QUICKSTART.md**: 5-minute getting started guide
- **README.md**: This comprehensive guide
- **Inline code comments**: Self-documenting implementations

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Bronze Tier Architecture               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  PERCEPTION LAYER (Watchers)                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │ FileSystemWatcher                                │  │
│  │ - Monitors: ~/Downloads                          │  │
│  │ - Frequency: Every 30 seconds                    │  │
│  │ - Action: Creates .md in /Needs_Action           │  │
│  └──────────────────────────────────────────────────┘  │
│           ↓                                              │
│  REASONING LAYER (Claude Code)                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Claude Code (Manual Trigger)                     │  │
│  │ - Reads: /Needs_Action folder                    │  │
│  │ - Thinks: Analyzes task requirements             │  │
│  │ - Creates: /Plans with checkboxes                │  │
│  └──────────────────────────────────────────────────┘  │
│           ↓                                              │
│  ACTION LAYER (Human + Dashboard)                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Human Review & Execution                         │  │
│  │ - Reviews Plan.md                                │  │
│  │ - Executes actions manually                      │  │
│  │ - Moves completed items to /Done                 │  │
│  │ - Updates Dashboard.md                           │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Getting Started

### Prerequisites
- Python 3.13+
- Claude Code installed (`claude --version`)
- Obsidian installed (optional but recommended)
- ~500MB disk space

### Quick Setup (Already Done)

The Bronze Tier is fully set up. Verify with:
```bash
python3 test_setup.py
```

### First Time Using

See **QUICKSTART.md** for a 5-minute hands-on test.

## File Descriptions

### Core Vault Files

#### Dashboard.md
Real-time status hub. Update after each action cycle:
```markdown
# Dashboard

## Status Summary
- Pending Items: [count from /Needs_Action]
- Completed Today: [count from /Done]
- In Progress: [current task]

## Recent Activity
[Log of recent actions]
```

#### Company_Handbook.md
Rules that guide Claude's behavior:
- Communication guidelines
- Financial approval thresholds
- Business rules (e.g., "Flag payments > $500")
- Escalation procedures
- Success metrics

### Watcher Scripts

#### base_watcher.py
Abstract base class for all watchers:
```python
class BaseWatcher(ABC):
    @abstractmethod
    def check_for_updates(self) -> list
    @abstractmethod
    def create_action_file(self, item) -> Path
    def run(self)  # Main loop
```

#### filesystem_watcher.py
Concrete implementation monitoring file system:
- Monitors ~/Downloads (configurable)
- Creates markdown files with metadata
- Tracks processed files to avoid duplicates
- Includes error handling and logging

## Usage Workflows

### Workflow 1: File Drop → Claude Processing

```
1. Drop file in ~/Downloads
2. Watcher detects (within 30 seconds)
3. Watcher creates FILE_*.md in /Needs_Action
4. Run: claude code AI_Employee_Vault
5. Claude reads /Needs_Action
6. Claude creates Plan_*.md in /Plans
7. Human reviews Plan_*.md
8. Human executes action or move to /Done
9. Update Dashboard.md
```

### Workflow 2: Dashboard Updates

```
1. Open Dashboard.md in Obsidian
2. Review "Pending Items" section
3. Check /Needs_Action for count
4. Update status metrics
5. Claude can read and reference Dashboard
```

### Workflow 3: Company Handbook Updates

```
1. Open Company_Handbook.md
2. Add new rules as you learn
3. Clarify communication style
4. Set approval thresholds
5. Claude follows rules on next run
```

## Configuration

### Change Watch Folder

Edit `watchers/filesystem_watcher.py`:
```python
WATCH_FOLDER = "~/Downloads"  # Change this
```

### Change Check Interval

Edit `filesystem_watcher.py`:
```python
watcher = FileSystemWatcher(VAULT_PATH, WATCH_FOLDER, check_interval=30)
#                                                    ↑ in seconds
```

### Claude Code Commands

Always point Claude to the vault:
```bash
claude code /path/to/AI_Employee_Vault
```

Inside Claude Code:
```
Read /Needs_Action and summarize items
Create a Plan.md in /Plans with next steps
Update Dashboard.md with progress
```

## Common Tasks

### Add a New Rule to Company Handbook
1. Open `AI_Employee_Vault/Company_Handbook.md`
2. Add rule under appropriate section
3. Example: "Flag all vendor payments for approval"
4. Claude follows on next run

### Process Items Manually
```bash
# View pending items
cat AI_Employee_Vault/Needs_Action/*.md

# After reviewing, create a plan
claude code AI_Employee_Vault
# Type: "Create Plan.md for the items in /Needs_Action"

# Move to done
mv AI_Employee_Vault/Needs_Action/FILE_*.md AI_Employee_Vault/Done/
```

### Update Dashboard
1. Open in Obsidian or text editor
2. Update counts, recent activity, upcoming items
3. Claude can read and reference it

### Test Watcher
```bash
python3 watchers/filesystem_watcher.py
# Leave running, drop a file in ~/Downloads
# Check AI_Employee_Vault/Needs_Action for new .md file
```

## Troubleshooting

### Watcher Not Creating Files

**Check 1: Is watcher running?**
```bash
ps aux | grep filesystem_watcher
```

**Check 2: Is watch folder correct?**
```bash
ls ~/Downloads
# Should show your test file
```

**Check 3: Do vault folders exist?**
```bash
ls -la AI_Employee_Vault/
# Should show Needs_Action, Plans, Done, etc.
```

**Check 4: Check watcher logs**
```bash
python3 watchers/filesystem_watcher.py
# Watch for error messages
```

### Claude Can't Read Vault

**Check 1: Correct path?**
```bash
cd /c/Users/HP/Desktop/H/FTEs/Bronze\ Tier
# Must be absolute path, not relative
```

**Check 2: Folder readable?**
```bash
ls AI_Employee_Vault/Needs_Action/
```

**Check 3: Test Claude with simple prompt:**
```bash
claude code AI_Employee_Vault
# Type: "List all files in /Needs_Action"
```

### No Plans Being Created

**Solution 1**: Claude might need more explicit prompt
```bash
claude code AI_Employee_Vault
# Type: "Read /Needs_Action. Create a Plan.md file in /Plans with detailed next steps"
```

**Solution 2**: Check Company_Handbook.md for style guidance
- Add specific instructions to guide Claude's responses

## Testing Verification

Run the test suite anytime:
```bash
python3 test_setup.py
```

Expected output:
```
[PASS]: Vault Structure
[PASS]: Watcher Files
[PASS]: Python Imports
[PASS]: Watcher Instantiation
```

## Deliverables Checklist

- [x] Obsidian vault created with correct folder structure
- [x] Dashboard.md created with status template
- [x] Company_Handbook.md created with guidelines
- [x] FileSystem Watcher implemented and tested
- [x] Watcher successfully creates .md files in /Needs_Action
- [x] Claude Code can read /Needs_Action
- [x] Claude Code can write files to vault
- [x] End-to-end tested: File → Watcher → Claude → Plan
- [x] Documentation complete (CLAUDE.md, QUICKSTART.md, README.md)

## Key Files & Locations

| File | Purpose | Location |
|------|---------|----------|
| Dashboard.md | Status hub | `/AI_Employee_Vault/Dashboard.md` |
| Company_Handbook.md | Rules | `/AI_Employee_Vault/Company_Handbook.md` |
| CLAUDE.md | Bronze guidance | `/CLAUDE.md` |
| QUICKSTART.md | 5-min guide | `/QUICKSTART.md` |
| base_watcher.py | Abstract class | `/watchers/base_watcher.py` |
| filesystem_watcher.py | File monitor | `/watchers/filesystem_watcher.py` |
| test_setup.py | Verification | `/test_setup.py` |

## Next Steps: Silver Tier

When Bronze Tier is stable and you're ready to scale, move to **Silver Tier** which adds:

- **2+ Watchers**: Gmail watcher + WhatsApp watcher + LinkedIn monitoring
- **MCP Server**: Email sending capability (first "hand" for the agent)
- **Approval Workflow**: Files for requesting human approval
- **Scheduling**: Automated task execution via cron/Task Scheduler
- **LinkedIn Integration**: Auto-post business updates

Silver Tier estimated time: 20-30 hours
See `../Silver Tier/CLAUDE.md` (once created)

## Resources

### Documentation
- `CLAUDE.md`: Tier architecture and guidelines
- `QUICKSTART.md`: 5-minute hands-on guide
- `Personal AI Employee Hackathon 0_...md`: Complete project spec (parent dir)
- `../CLAUDE.md`: Root project guidance

### Tools
- Claude Code: https://claude.com/product/claude-code
- Obsidian: https://obsidian.md/
- Python docs: https://python.org/

### Community
- Wednesday Research Meetings (see hackathon guide for Zoom link)
- Community learning on implementation patterns

## FAQ

**Q: Can I change the watch folder?**
A: Yes, edit `watchers/filesystem_watcher.py` line with `WATCH_FOLDER`

**Q: Does Claude run 24/7?**
A: No, Bronze is manual trigger. You run `claude code vault` when ready. Silver+ adds scheduling.

**Q: Can I use Gmail instead of FileSystem?**
A: Yes, see hackathon guide for Gmail implementation. FileSystem is simpler for Bronze.

**Q: Is the vault secure?**
A: Vault is local markdown. Never commit secrets (.env, tokens) to it. Store locally only.

**Q: How do I move to Silver Tier?**
A: Create `../Silver Tier/CLAUDE.md`, build Watchers + MCP server, follow same pattern.

## Support

Issues or questions?
1. Check QUICKSTART.md for common issues
2. Review `../CLAUDE.md` for project-wide guidance
3. See `Personal AI Employee Hackathon 0_...md` for detailed specs
4. Reach out in Wednesday Research Meetings for community help

---

**Bronze Tier is complete and ready to use!** Start with QUICKSTART.md for a quick test.
