# CLAUDE.md - Bronze Tier

This file provides guidance to Claude Code when working on the Bronze Tier of the Digital FTE project.

## Bronze Tier Overview

**Estimated Time**: 8-12 hours
**Status**: IN PROGRESS
**Goal**: Build the foundation for a Digital FTE with manual Watcher, Obsidian vault, and Claude Code integration.

## Bronze Tier Deliverables

- [ ] Obsidian vault with `Dashboard.md` (real-time summary) and `Company_Handbook.md` (rules of engagement)
- [ ] One working Watcher script (Gmail OR file system monitoring)
- [ ] Claude Code successfully reading from and writing to vault
- [ ] Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`
- [ ] All AI functionality implemented as Agent Skills in `.claude/skills/`

## Architecture for Bronze Tier

```
Bronze Tier = Manual Perception → Claude Reasoning → Manual Action

Watcher Script (Python)
    ↓
    ├── Monitors: Gmail OR FileSystem
    ├── Creates: .md files in /Needs_Action
    └── Triggers: Human runs "claude code /vault/path"

Claude Code (Terminal)
    ├── Reads: /Needs_Action folder
    ├── Thinks: Plans next steps
    ├── Creates: /Plans/Task_*.md files with checkboxes
    └── Writes: Updates to vault

Manual Actions
    └── User approves and executes plans manually
```

## Obsidian Vault Structure (Bronze Minimal)

```
AI_Employee_Vault/
├── Dashboard.md (status summary: pending tasks, completed tasks)
├── Company_Handbook.md (rules: how Claude should behave)
├── Inbox/ (all incoming items)
├── Needs_Action/ (items for Claude to process)
├── Plans/ (Plan.md files created by Claude)
├── Done/ (completed items)
└── References/ (optional: knowledge base)
```

## Bronze Tier: Step-by-Step Build Path

### Phase 1: Create Obsidian Vault Structure
1. Create `AI_Employee_Vault` folder
2. Create subfolders: `/Inbox`, `/Needs_Action`, `/Done`, `/Plans`
3. Create `Dashboard.md` with template:
   ```markdown
   # Dashboard

   ## Status Summary
   - Pending Items: 0
   - Completed Today: 0
   - Active Projects: None

   ## Today's Goals
   - [ ] Set up vault
   - [ ] Create Company Handbook
   - [ ] Build Watcher script
   ```
4. Create `Company_Handbook.md` with rules template:
   ```markdown
   # Company Handbook: Rules of Engagement

   ## Claude's Guidelines
   - Always be helpful and clear
   - Ask questions before assuming
   - Flag anything unclear or missing information
   - Suggest next steps for incomplete tasks

   ## Personal Rules
   - [Add your business rules here]
   - [e.g., "Flag payments over $500 for approval"]
   - [e.g., "Always confirm before sending emails"]
   ```

### Phase 2: Build One Watcher Script

Choose **either** Gmail OR FileSystem monitoring. FileSystem is simpler for Bronze.

#### Option A: FileSystem Watcher (RECOMMENDED FOR BRONZE)

Create `watchers/filesystem_watcher.py`:

```python
from pathlib import Path
from datetime import datetime
import time
import logging

class FileSystemWatcher:
    def __init__(self, vault_path: str, watch_folder: str = "~/Downloads"):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.watch_folder = Path(watch_folder).expanduser()
        self.processed_files = set()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def check_for_new_files(self):
        """Check for new files in watch folder"""
        if not self.watch_folder.exists():
            return []

        new_files = []
        for file in self.watch_folder.iterdir():
            if file.is_file() and str(file) not in self.processed_files:
                new_files.append(file)
                self.processed_files.add(str(file))

        return new_files

    def create_action_file(self, source_file: Path):
        """Create markdown file in Needs_Action"""
        filename = f"FILE_{source_file.name}"
        action_file = self.needs_action / filename.replace(source_file.suffix, '.md')

        content = f"""---
type: file_drop
original_name: {source_file.name}
created: {datetime.now().isoformat()}
size: {source_file.stat().st_size} bytes
status: pending
---

# New File: {source_file.name}

A new file has been detected in your watch folder.

## File Details
- **Path**: {source_file}
- **Size**: {source_file.stat().st_size} bytes
- **Created**: {datetime.now().isoformat()}

## Next Steps
- [ ] Review file
- [ ] Determine action needed
- [ ] Move to Done when processed
"""
        action_file.write_text(content)
        self.logger.info(f"Created action file: {action_file}")
        return action_file

    def run(self):
        """Main loop: check for files every 30 seconds"""
        self.logger.info(f"FileSystem Watcher started. Watching {self.watch_folder}")

        while True:
            try:
                new_files = self.check_for_new_files()
                for file in new_files:
                    self.create_action_file(file)
            except Exception as e:
                self.logger.error(f"Error: {e}")

            time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    # Update these paths to match your setup
    VAULT_PATH = "/path/to/AI_Employee_Vault"
    WATCH_FOLDER = "~/Downloads"

    watcher = FileSystemWatcher(VAULT_PATH, WATCH_FOLDER)
    watcher.run()
```

#### Option B: Gmail Watcher (More Complex)

See the hackathon guide's Gmail implementation. Requires:
- Google OAuth2 credentials setup
- Google Workspace account

### Phase 3: Verify Claude Code Integration

Test that Claude Code can:
1. Read files from `/Needs_Action`
2. Write files to `/Plans` and `/Done`

**Test Command**:
```bash
claude code /path/to/AI_Employee_Vault
```

**What to do in Claude Code**:
```
Read the /Needs_Action folder and list all pending items.
Create a Plan.md file in /Plans with suggested next steps.
```

### Phase 4: Create Initial Agent Skills

All AI functionality should be in `.claude/skills/`. Already set up:
- `.claude/skills/browsing-with-playwright/` (for web automation if needed)

For Bronze, you may want to add:
- Vault reading/writing utility skill
- Task analysis skill

## Bronze Tier Tools & Skills

### Current Skills
- `browsing-with-playwright`: Browser automation (available if needed)

### Skill Structure
```
.claude/skills/<skill-name>/
├── SKILL.md (instructions)
├── scripts/ (Python/shell executables)
├── references/ (docs)
└── skills-lock.json
```

## Bronze Tier: Testing & Verification

### Test 1: Watcher Creates Files
```bash
# Run the watcher
python3 watchers/filesystem_watcher.py

# Drop a file in the watched folder (e.g., ~/Downloads)
# Check: Does /Needs_Action have a new .md file?
```

### Test 2: Claude Reads Vault
```bash
claude code /path/to/AI_Employee_Vault

# Inside Claude Code:
# "Read /Needs_Action and summarize pending items"
```

### Test 3: Claude Writes to Vault
```bash
# In Claude Code:
# "Create a Plan.md file in /Plans with next steps for setting up this Digital FTE"

# Check: Does /Plans/Plan_*.md exist?
```

### Test 4: Obsidian Opens Vault
- Open Obsidian
- Select "Open vault from folder"
- Point to `AI_Employee_Vault`
- Verify you can see `/Needs_Action`, `/Plans`, `/Done` folders
- Verify you can read and edit `Dashboard.md` and `Company_Handbook.md`

## Bronze Tier: Common Commands

### Start Watcher (FileSystem)
```bash
cd /c/Users/HP/Desktop/H/FTEs/Bronze\ Tier
python3 watchers/filesystem_watcher.py
```

### Trigger Claude to Process Vault
```bash
claude code /c/Users/HP/Desktop/H/FTEs/Bronze\ Tier/AI_Employee_Vault
```

### Check Vault Structure
```bash
ls -la /c/Users/HP/Desktop/H/FTEs/Bronze\ Tier/AI_Employee_Vault/
```

## Bronze Tier: Troubleshooting

| Issue | Solution |
|-------|----------|
| Watcher not creating files | Check watch folder path, file permissions, logs |
| Claude can't read vault | Verify vault path is absolute, folders exist |
| Obsidian can't open vault | Ensure vault is a valid folder with subfolders |
| Files not appearing in `/Needs_Action` | Check watcher script is running, monitor logs |
| Claude writes missing | File permissions, vault path issues |

## Bronze Tier: Completion Checklist

- [ ] Obsidian vault created with correct folder structure
- [ ] `Dashboard.md` created with status template
- [ ] `Company_Handbook.md` created with guidelines
- [ ] Watcher script (FileSystem or Gmail) implemented and tested
- [ ] Watcher successfully creates `.md` files in `/Needs_Action`
- [ ] Claude Code can read `/Needs_Action` and `/Plans` folders
- [ ] Claude Code can write files to vault
- [ ] All AI functionality in `.claude/skills/`
- [ ] Tested end-to-end: File dropped → Watcher creates task → Claude processes → Files in `/Plans`

## Bronze Tier Completion

Once Bronze is complete, all foundation components are ready:
- ✓ Obsidian vault with structure
- ✓ FileSystem Watcher running
- ✓ Claude Code integration working
- ✓ Basic automation patterns established

Bronze Tier is standalone and fully functional for local file-based task processing.

## Key Bronze Patterns

### File Naming Convention
- Watcher files: `FILE_<original-name>.md`, `EMAIL_<id>.md`, `WHATSAPP_<id>.md`
- Claude plans: `Plan_<task-name>.md`
- Approval files: `APPROVAL_REQUIRED_<action>.md`

### Folder States
- `/Needs_Action`: Items awaiting Claude processing
- `/Plans`: Claude's plans with checkboxes
- `/Done`: Completed items (move here manually)

### Obsidian as Dashboard
- `Dashboard.md` is the single source of truth for status
- `Company_Handbook.md` guides Claude's behavior
- Update Dashboard manually or via Claude after each action

## Resources

- **Hackathon Guide**: `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md` (in parent directory)
- **Root CLAUDE.md**: `../CLAUDE.md` for project-wide context
- **Obsidian Docs**: https://help.obsidian.md/
- **Claude Code**: https://claude.com/product/claude-code
