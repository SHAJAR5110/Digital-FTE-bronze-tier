# How to Use Bronze Tier - Simple Guide

## What is Bronze Tier?

Bronze Tier watches your Downloads folder and automatically analyzes files using Claude Code.

**It does this:**
1. Monitor Downloads folder for new files
2. Create action items in Obsidian vault
3. Claude Code analyzes the content
4. Store results in organized folders

---

## 3 Simple Steps to Get Started

### Step 1: Start the Watcher

Open terminal and run:
```bash
cd "/c/Users/HP/Desktop/H/FTEs/Bronze Tier"
bash scripts/start-watchers.sh
```

This command starts monitoring your Downloads folder. Keep this terminal window open.

---

### Step 2: Open Obsidian Vault

1. Open Obsidian app
2. Click "Open vault folder"
3. Select: `C:\Users\HP\Desktop\H\FTEs\Bronze Tier\AI_Employee_Vault`
4. You will see folders:
   - **Dashboard.md** - Current status
   - **Needs_Action** - New files here
   - **Plans** - Claude's analysis
   - **Done** - Completed items

---

### Step 3: Run Claude Analysis

Open a NEW terminal window and run:
```bash
cd "/c/Users/HP/Desktop/H\FTEs/Bronze Tier"
bash scripts/run-claude.sh
```

Claude will:
1. Read files from Needs_Action
2. Analyze the content
3. Write results to Plans folder
4. Move items to Done folder

---

## How It Works - Example

**You download a PDF file to Downloads:**

```
YOUR ACTION: Download invoice.pdf to Downloads
        ↓
WATCHER DETECTS: "New file found!"
        ↓
CREATES: AI_Employee_Vault/Needs_Action/FILE_invoice.md
        ↓
YOU RUN: bash scripts/run-claude.sh
        ↓
CLAUDE READS: The Needs_Action file
        ↓
CLAUDE ANALYZES: Opens PDF, reads content
        ↓
CLAUDE CREATES: AI_Employee_Vault/Plans/Invoice_Analysis.md
        ↓
CLAUDE COMPLETES: Moves to Done folder
        ↓
YOU SEE: Results in Obsidian vault
```

---

## Folder Structure

```
Bronze Tier/
├── AI_Employee_Vault/          ← Main vault (open in Obsidian)
│   ├── Dashboard.md            ← Check status here
│   ├── Needs_Action/           ← New files detected here
│   ├── Plans/                  ← Claude's analysis
│   ├── Done/                   ← Completed tasks
│   ├── Inbox/                  ← Backup storage
│   └── References/             ← Notes and references
│
├── watchers/                   ← Monitoring scripts
│   └── filesystem_watcher.py   ← Watches Downloads
│
├── scripts/                    ← Commands to run
│   ├── start-watchers.sh       ← Start monitoring
│   └── run-claude.sh           ← Run analysis
│
└── .claude/skills/             ← AI capabilities
    └── browsing-with-playwright/ ← Can open websites
```

---

## What AI is Being Used?

### Claude Code (by Anthropic)

Claude Code is the AI system that:
- Reads files from the vault
- Analyzes content
- Makes decisions about what to do
- Writes results back to vault
- Uses web browsing when needed

### How Claude Works in Bronze

1. **Reads** - Opens .md files from Needs_Action
2. **Thinks** - Analyzes the content
3. **Uses Skills** - Playwright skill to open websites
4. **Writes** - Creates analysis in Plans folder
5. **Organizes** - Moves items to Done folder

---

## Daily Usage

### Every Day Do This:

1. **Download/Save files** - Put files in Downloads normally
2. **Watcher works** - Automatically detects new files
3. **Run Claude** - Execute `bash scripts/run-claude.sh`
4. **Check Obsidian** - View results in vault

### Monitor Progress:

**In Obsidian:**
- Open AI_Employee_Vault
- Click on Needs_Action to see pending items
- Click on Plans to see analyses
- Click on Done to see completed items

**In Terminal:**
```bash
# See what needs action
ls AI_Employee_Vault/Needs_Action/

# See completed plans
ls AI_Employee_Vault/Plans/

# See finished items
ls AI_Employee_Vault/Done/
```

---

## Commands You Will Use

### Start Monitoring (do this first)
```bash
bash scripts/start-watchers.sh
```
Leaves this terminal open and running.

### Run Analysis (in a new terminal)
```bash
bash scripts/run-claude.sh
```
Claude analyzes files and creates results.

### Check Status
```bash
cat AI_Employee_Vault/Dashboard.md
```
See current status and what's pending.

### View Results
```bash
ls AI_Employee_Vault/Plans/
cat AI_Employee_Vault/Plans/your-file.md
```
Read Claude's analysis of your files.

### Stop Monitoring
```bash
# Close the watcher terminal (Ctrl+C)
# Or in a new terminal:
pkill -f filesystem_watcher
```

---

## Test It Works

Try this simple test:

```bash
# Create a test file
cat > AI_Employee_Vault/Needs_Action/TEST_001.md << 'EOF'
---
type: test
created: now
---

# Test File

Please analyze this test file and confirm Bronze Tier is working.
EOF

# Run Claude
bash scripts/run-claude.sh

# Check if Claude created a response
ls AI_Employee_Vault/Plans/
```

You should see a new file in Plans folder with Claude's response.

---

## Customize Behavior

### Change How Claude Acts

Edit this file:
```bash
nano AI_Employee_Vault/Company_Handbook.md
```

Add rules like:
- "Always be professional in responses"
- "Flag urgent items immediately"
- "Create summaries for all files"

Claude will follow these rules.

### Change What Files to Monitor

Edit this file:
```bash
nano watchers/filesystem_watcher.py
```

Look for:
```python
monitor_path = os.path.expanduser("~/Downloads")
```

Change to monitor different folder.

---

## Troubleshooting

### Problem: Watcher not detecting files

**Solution:**
```bash
# Check if running
ps aux | grep filesystem_watcher

# Restart watcher
bash scripts/start-watchers.sh
```

### Problem: Claude not analyzing files

**Solution:**
```bash
# Check Needs_Action has files
ls AI_Employee_Vault/Needs_Action/

# Run Claude again
bash scripts/run-claude.sh

# Check for results
ls AI_Employee_Vault/Plans/
```

### Problem: Obsidian not showing vault

**Solution:**
1. Close Obsidian completely
2. Reopen Obsidian
3. Click "Open vault folder"
4. Select correct path: `Bronze Tier\AI_Employee_Vault`
5. Reload (Ctrl+R)

### Problem: Commands not found

**Solution:**
```bash
# Make sure you are in correct directory
cd "/c/Users/HP/Desktop/H/FTEs/Bronze Tier"

# Then run commands
bash scripts/start-watchers.sh
bash scripts/run-claude.sh
```

---

## What Happens Step by Step

### When You Download a File

```
Step 1: File downloaded to Downloads
        ↓
Step 2: Watcher detects new file (every 60 seconds)
        ↓
Step 3: Watcher creates .md file in Needs_Action
        ↓
Step 4: You run "bash scripts/run-claude.sh"
        ↓
Step 5: Claude reads the .md file
        ↓
Step 6: Claude opens the actual file (using Playwright skill)
        ↓
Step 7: Claude analyzes content
        ↓
Step 8: Claude writes analysis to Plans folder
        ↓
Step 9: Item moved to Done folder
        ↓
Step 10: You see results in Obsidian
```

---

## Key Features

- **Automatic Detection** - Watcher runs 24/7
- **Claude Analysis** - AI analyzes every file
- **Web Browsing** - Can check links and websites
- **Organized Storage** - Everything in Obsidian vault
- **Human Readable** - All files are markdown
- **No Data Loss** - Everything stays on your computer
- **Customizable** - Change rules in Company_Handbook.md

---

## Summary

1. Run `bash scripts/start-watchers.sh` (keep running)
2. Run `bash scripts/run-claude.sh` (when you want analysis)
3. Open Obsidian to see results
4. Files go from Needs_Action → Plans → Done

**That's it! Bronze Tier handles the rest.**

---

## Next Steps

1. Follow the 3 steps above
2. Download a file to test
3. Check Obsidian vault for results
4. Customize behavior in Company_Handbook.md
5. Move to Silver Tier when ready for more features

---

**Questions? Check README.md or QUICKSTART.md for more details.**
