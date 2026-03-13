# USE.md - Bronze Tier Usage Guide

**Purpose**: Understand which directories you can work with and how to use them
**Level**: Practical, hands-on guide for daily use

## Directory Overview & Workability

### Overview of All Directories

```
AI_Employee_Vault/
├── Dashboard.md              ✓ Workable (You write, Claude reads)
├── Company_Handbook.md       ✓ Workable (You write, Claude follows)
├── Inbox/                    ⚠ Optional (future use - not used in Bronze)
├── Needs_Action/             ✓ READ-ONLY (Watcher writes, you read, Claude reads)
├── Plans/                    ✓ READ-ONLY (Claude writes, you read and execute)
├── Done/                     ✓ Workable (You move files here after completion)
└── References/               ✓ Workable (You add knowledge base docs)
```

---

## Detailed Directory Guide

### 1. Dashboard.md - YOUR STATUS HUB

**Purpose**: Real-time status of everything happening in your vault
**Workability**: ✅ You control this (READ & WRITE)
**Who interacts**: You (human) + Claude (reads)

#### What Goes Here
```markdown
# Dashboard

## Status Summary
- Pending Items: [count]
- Completed Today: [count]
- In Progress: [current task name]

## Today's Goals
- [ ] Task 1
- [ ] Task 2

## Recent Activity
- [Time] Completed: Email response to Client A
- [Time] Created: Payment approval request

## Key Metrics
- Processing Rate: [tasks/day]
- Approval Rate: [%]
```

#### How to Use It

**When to Update**:
1. Start of day - set goals
2. After Claude creates a plan - log it
3. After you complete an action - mark it done
4. End of day - summarize progress

**Example Updates**:
```bash
# Open in text editor or Obsidian
nano AI_Employee_Vault/Dashboard.md

# Update status section
- Pending Items: 3
- Completed Today: 2
- In Progress: Email response for Project X

# Claude reads this for context
```

**Why It Matters**:
- Claude references Dashboard for context
- You track your own productivity
- Provides quick status check anytime
- Foundation for future automated audits

#### Commands
```bash
# View current dashboard
cat AI_Employee_Vault/Dashboard.md

# Edit dashboard
nano AI_Employee_Vault/Dashboard.md  # or any editor

# Check how many items pending
wc -l AI_Employee_Vault/Needs_Action/*
# Use this to update "Pending Items" count
```

---

### 2. Company_Handbook.md - YOUR RULES GUIDE

**Purpose**: Document rules that guide Claude's behavior
**Workability**: ✅ You control this (READ & WRITE)
**Who interacts**: You (human) + Claude (reads and follows)

#### What Goes Here
```markdown
# Company Handbook

## Claude's Guidelines
- Always confirm before sending emails
- Be professional in all communications
- Ask if something is unclear

## My Business Rules
- Flag payments over $500
- Respond to emails within 4 hours
- Always be polite on WhatsApp

## Approval Thresholds
- Small tasks: Auto-approve (< $50)
- Medium tasks: Ask for approval ($50-$500)
- Large tasks: Manual review (> $500)

## Communication Style
- Formal for business, casual for friends
- Always sign-off professionally
```

#### How to Use It

**When to Update**:
1. First time - add your baseline rules
2. When Claude makes a mistake - clarify the rule
3. When you want to change behavior - update it
4. Regularly - review and refine

**Real Example**:
```markdown
## My Business Rules (Version 1)

### Email Rules
- Never send without explicit instruction
- Flag urgent emails (URGENT, ASAP, ASAP)
- Summarize long emails

### Financial Rules
- Flag all payments for approval
- Verify recipients before sending money
- Keep transaction log updated

### Social Media Rules
- Draft posts, never auto-publish
- Flag controversial topics for review
- Keep business and personal separate
```

**How Claude Uses This**:
When you run Claude and it processes a task, it reads Company_Handbook.md and follows the rules. Example:

```
Claude sees: "Client wants to discuss payment"
Claude reads Company_Handbook: "Flag all payments for approval"
Claude creates: APPROVAL_REQUIRED_Payment_Discussion.md
Claude does NOT send payment without your approval
```

#### Commands
```bash
# View current handbook
cat AI_Employee_Vault/Company_Handbook.md

# Edit handbook (add your rules)
nano AI_Employee_Vault/Company_Handbook.md

# Reference during setup
# Update this file BEFORE running Claude for best results
```

**Pro Tips**:
- Start simple, add rules as needed
- Be specific ("Flag payments > $500" not "Flag big payments")
- Update after Claude makes mistakes
- Review weekly for clarity

---

### 3. Needs_Action/ - YOUR TASK INBOX

**Purpose**: Items waiting to be processed by Claude
**Workability**: 🔴 READ-ONLY (You read, don't write)
**Who creates files**: Watcher script (automatic)
**Who reads files**: You + Claude

#### What Goes Here (Auto-Created by Watcher)

```markdown
---
type: file_drop
original_name: invoice.pdf
file_size_kb: 145.2
source_path: C:\Users\HP\Downloads\invoice.pdf
detected_at: 2026-03-12T10:30:00
status: pending
---

# New File: invoice.pdf

A new file has been detected in your watch folder.

## File Details
- Name: invoice.pdf
- Size: 145.2 KB
- Type: PDF
- Location: C:\Users\HP\Downloads
- Detected: 2026-03-12 10:30 AM

## Status
- [ ] Review file
- [ ] Determine action needed
- [ ] Move to Done when processed

## Notes
Add any analysis or next steps below.
```

#### How to Use It

**Workflow**:
1. Watcher creates FILE_*.md in Needs_Action/
2. You review the file (optional)
3. You run Claude: `claude code AI_Employee_Vault`
4. Claude reads all files in Needs_Action/
5. Claude creates Plans (see Plans/ directory)
6. You execute the plan or approve actions

**Example Task**:
```bash
# 1. Watcher creates this file
AI_Employee_Vault/Needs_Action/FILE_invoice.md

# 2. You see it (can review anytime)
cat AI_Employee_Vault/Needs_Action/FILE_invoice.md

# 3. You trigger Claude
claude code AI_Employee_Vault
# Prompt: "Read /Needs_Action and create a plan"

# 4. Claude creates a plan
AI_Employee_Vault/Plans/Plan_Invoice_Processing.md

# 5. You execute the plan
# Then move the original file
mv AI_Employee_Vault/Needs_Action/FILE_invoice.md \
   AI_Employee_Vault/Done/FILE_invoice.md
```

#### What You Can Do Here

✅ **CAN DO**:
- Read files (check what's there)
- Note observations
- Leave comments for Claude

❌ **DON'T DO**:
- Delete files (let Claude or you move them to Done)
- Manually create FILES_*.md (let Watcher do it)
- Move files here (let Watcher put them here)

#### Commands
```bash
# See what's pending
ls -la AI_Employee_Vault/Needs_Action/

# Count pending items
ls AI_Employee_Vault/Needs_Action/ | wc -l

# Read a specific task
cat AI_Employee_Vault/Needs_Action/FILE_something.md

# View all pending items at once
cat AI_Employee_Vault/Needs_Action/*

# Update Dashboard with count
# (Tell Claude how many items pending)
```

**Pro Tips**:
- Keep /Needs_Action clean - process items regularly
- If too many items accumulate, trigger Claude more often
- Review items before running Claude to provide context
- Don't create files here - let Watcher do it

---

### 4. Plans/ - YOUR ACTION PLANS

**Purpose**: Plans created by Claude for you to execute
**Workability**: 🟡 READ-ONLY (You read, execute, don't edit)
**Who creates**: Claude Code
**Who reads**: You (human)

#### What Goes Here (Created by Claude)

```markdown
---
type: plan
created_by: Claude
created_at: 2026-03-12T10:45:00
status: pending_execution
priority: medium
---

# Plan: Invoice Processing - Invoice.pdf

## Summary
You have a new invoice that needs to be recorded and processed.

## Analysis
- File: invoice.pdf (145 KB)
- Source: Unknown (check file content)
- Action: Review, verify, record amount

## Steps to Complete
- [ ] Step 1: Open invoice.pdf
- [ ] Step 2: Extract invoice number, amount, date
- [ ] Step 3: Verify vendor and amount
- [ ] Step 4: Record in accounting (when available)
- [ ] Step 5: File in appropriate folder

## Timeline
- Estimated time: 10 minutes
- Due by: Today (documents should be processed same day)

## Next Steps After Complete
Once complete, move FILE_invoice.md to /Done/

---

**Notes for User**: Review invoice for authenticity before recording. If amount seems unusual, flag for verification.
```

#### How to Use It

**Workflow**:
1. Claude creates Plan_*.md in /Plans/
2. You read the plan
3. You follow the checkboxes (manual execution)
4. You mark items complete as you go
5. When done, move original file to /Done/

**Example Execution**:
```bash
# 1. Claude created a plan
cat AI_Employee_Vault/Plans/Plan_Invoice_Processing.md

# 2. You execute each step
# - Open the invoice
# - Extract information
# - Verify details
# - Record it

# 3. You update the plan (optional)
# Check off items as you complete them

# 4. You move original to Done
mv AI_Employee_Vault/Needs_Action/FILE_invoice.md \
   AI_Employee_Vault/Done/FILE_invoice.md

# 5. You update Dashboard
# Add: "Completed: Invoice processing for invoice.pdf"
```

#### What You Can Do Here

✅ **CAN DO**:
- Read plans (understand what to do)
- Check off items as you complete them
- Add notes about execution
- Reference for context

❌ **DON'T DO**:
- Delete plans (keep for audit trail)
- Edit Claude's analysis (change Company_Handbook if you disagree)
- Move files (let them stay in /Plans/ as records)

#### Commands
```bash
# See all plans
ls -la AI_Employee_Vault/Plans/

# Read latest plan
ls -t AI_Employee_Vault/Plans/ | head -1 | xargs -I {} cat AI_Employee_Vault/Plans/{}

# Find plan by keyword
grep -r "invoice" AI_Employee_Vault/Plans/

# Mark item as done
# (Use text editor to check [ ] boxes)
```

**Pro Tips**:
- Review plan before executing
- If Claude's plan seems wrong, check Company_Handbook for clarity
- Keep plans as historical record (audit trail)
- Use them to improve Company_Handbook rules

---

### 5. Done/ - YOUR COMPLETED ARCHIVE

**Purpose**: Archive completed tasks and files
**Workability**: ✅ You control this (WRITE)
**Who creates**: You (move files here)
**Who reads**: You (optional, for history)

#### What Goes Here

After completing a task:
1. Original file from Needs_Action/
2. Corresponding Plan from Plans/ (optional)
3. Any notes about completion

Example:
```bash
AI_Employee_Vault/Done/
├── FILE_invoice.md              # Original task
├── Plan_Invoice_Processing.md   # The plan you executed
└── FILE_report.md               # Another completed task
```

#### How to Use It

**Workflow**:
```bash
# After completing a task in your plan:

# 1. Move original file to Done
mv AI_Employee_Vault/Needs_Action/FILE_invoice.md \
   AI_Employee_Vault/Done/FILE_invoice.md

# 2. Optionally move the plan too (for history)
mv AI_Employee_Vault/Plans/Plan_Invoice_Processing.md \
   AI_Employee_Vault/Done/Plan_Invoice_Processing.md

# 3. Update Dashboard
echo "- [x] Processed invoice.pdf" >> AI_Employee_Vault/Dashboard.md
```

#### What You Can Do Here

✅ **CAN DO**:
- Move files here (mark as done)
- Create completion notes
- Review history
- Delete old items (after archiving)

❌ **DON'T DO**:
- Work on items here (work on them while in Needs_Action/)
- Lose historical records (backup before deleting)

#### Commands
```bash
# Move file from Needs_Action to Done
mv AI_Employee_Vault/Needs_Action/FILE_something.md \
   AI_Employee_Vault/Done/

# See what you've completed
ls AI_Employee_Vault/Done/

# Count completed items
ls AI_Employee_Vault/Done/ | wc -l

# Review specific completed task
cat AI_Employee_Vault/Done/FILE_something.md

# Archive old items (optional cleanup)
mkdir -p AI_Employee_Vault/Archive
mv AI_Employee_Vault/Done/* AI_Employee_Vault/Archive/  # if folder gets large
```

**Pro Tips**:
- Keep items in Done/ for at least 1 month (audit trail)
- Use Done/ to track your productivity
- Review Done/ weekly to see patterns
- Archive to separate folder after 90 days if needed

---

### 6. References/ - YOUR KNOWLEDGE BASE

**Purpose**: Store documents, templates, and reference material
**Workability**: ✅ You control this (READ & WRITE)
**Who creates**: You
**Who reads**: You + Claude (if referenced)

#### What Goes Here

```
References/
├── Templates/
│   ├── Email_Template_Professional.md
│   ├── Email_Template_Casual.md
│   └── Invoice_Template.md
├── Contacts/
│   ├── Important_Contacts.md
│   └── Client_List.md
├── Knowledge/
│   ├── Project_Guidelines.md
│   ├── Company_Procedures.md
│   └── Product_Info.md
└── Logs/
    └── Monthly_Summary_Feb_2026.md
```

#### How to Use It

**Organize by Category**:
```bash
# Create subfolders
mkdir -p AI_Employee_Vault/References/{Templates,Contacts,Knowledge,Logs}

# Add your templates
nano AI_Employee_Vault/References/Templates/Email_Template_Professional.md
```

**Example Template**:
```markdown
# Email Template - Professional Response

Dear [Client Name],

Thank you for reaching out regarding [topic].

[Your response here]

Best regards,
[Your Name]
[Your Title]
[Your Contact Info]
```

**Reference in Plans**:
Claude can reference these when creating plans:
> "See Email_Template_Professional.md in /References/ for proper formatting"

#### What You Can Do Here

✅ **CAN DO**:
- Add templates
- Store contacts
- Add procedures and guidelines
- Store reference documents
- Organize in subfolders

❌ **DON'T DO**:
- Store sensitive data (passwords, API keys - keep locally)
- Keep files that don't need syncing
- Ignore organization (keep it neat)

#### Commands
```bash
# Add a template
cat > AI_Employee_Vault/References/Templates/Email_Template.md << 'EOF'
# Professional Email Template
...
EOF

# Create contacts file
nano AI_Employee_Vault/References/Contacts/Clients.md

# List all references
find AI_Employee_Vault/References/ -type f

# Search references
grep -r "payment" AI_Employee_Vault/References/
```

**Pro Tips**:
- Create templates before you need them
- Keep contacts updated
- Reference these in Company_Handbook
- Help Claude follow your preferred formats

---

## Daily Workflow - How to Use Everything Together

### Morning Routine (5 minutes)
```bash
# 1. Check pending items
ls AI_Employee_Vault/Needs_Action/

# 2. View dashboard
cat AI_Employee_Vault/Dashboard.md

# 3. Note count of pending items
# "I have 3 items waiting"
```

### Processing Time (15 minutes)
```bash
# 1. Trigger Claude
cd /c/Users/HP/Desktop/H/FTEs/Bronze\ Tier
claude code AI_Employee_Vault

# 2. In Claude, type:
# "Read /Needs_Action and create plans for all items"

# 3. Claude processes and creates /Plans/Plan_*.md

# 4. Review the plans created
ls AI_Employee_Vault/Plans/
cat AI_Employee_Vault/Plans/Plan_*.md
```

### Execution Time (varies)
```bash
# 1. Follow each plan's checklist
# 2. Execute the steps (real world actions)
# 3. Check items off as complete

# 4. Move completed item to Done
mv AI_Employee_Vault/Needs_Action/FILE_something.md \
   AI_Employee_Vault/Done/
```

### Closing Routine (5 minutes)
```bash
# 1. Update Dashboard
nano AI_Employee_Vault/Dashboard.md
# - Update "Completed Today" count
# - Log what you completed
# - Set tomorrow's goals

# 2. Save changes
# File is automatically saved by editor
```

---

## Practical Examples

### Example 1: Process a File (Invoice)

**Start State**:
- Watcher detects: `invoice.pdf` in Downloads
- Creates: `FILE_invoice.md` in Needs_Action/

**Your Actions**:
```bash
# 1. See what's waiting
ls AI_Employee_Vault/Needs_Action/
# Output: FILE_invoice.md

# 2. Trigger Claude
claude code AI_Employee_Vault
# Prompt: "Create a plan for processing the invoice in /Needs_Action"

# 3. Claude creates plan
# Output: Plan_Invoice_Processing.md in /Plans/

# 4. Review the plan
cat AI_Employee_Vault/Plans/Plan_Invoice_Processing.md

# 5. Execute: Follow the checklist
# - Open the invoice PDF
# - Check invoice number, amount, date
# - Verify it's legitimate
# - (In future tiers: record in Odoo)

# 6. Mark item as done
mv AI_Employee_Vault/Needs_Action/FILE_invoice.md \
   AI_Employee_Vault/Done/FILE_invoice.md

# 7. Update Dashboard
nano AI_Employee_Vault/Dashboard.md
# Add: "- [x] Processed invoice for $1,500"
```

**Result**: Invoice processed, logged, archived. Done.

### Example 2: Update Rules (Company Handbook)

**Situation**: Claude made a decision you don't like

```bash
# 1. Read the plan Claude created
cat AI_Employee_Vault/Plans/Plan_*.md

# 2. See why Claude made that decision
# Review the Company_Handbook

# 3. Update the handbook with clearer rule
nano AI_Employee_Vault/Company_Handbook.md

# BEFORE:
# "Flag large payments"

# AFTER:
# "Flag all payments over $500 for approval"

# 4. Next time Claude will follow new rule

# 5. Save and exit
# Changes take effect on next Claude run
```

**Result**: Claude learns from your feedback.

### Example 3: Reference Template

**Situation**: Creating email response in a plan

```bash
# 1. Claude's plan says:
# "Create professional email response to client"

# 2. You have a template ready
cat AI_Employee_Vault/References/Templates/Email_Template_Professional.md

# 3. You use the template
# Copy the format
# Fill in the specific content
# Send the email

# 4. Work completed faster with consistent format
```

**Result**: Consistent, professional communication.

---

## Quick Reference - What To Do In Each Directory

| Directory | What Happens | Your Role |
|-----------|--------------|-----------|
| Dashboard.md | Status hub | Update daily |
| Company_Handbook.md | Rules guide | Write rules, Claude reads |
| Needs_Action/ | Tasks to process | Read, let Watcher create files |
| Plans/ | Claude's recommendations | Read, follow, execute |
| Done/ | Completed items | Move files here |
| References/ | Knowledge base | Add templates & guides |

---

## Troubleshooting - Common Issues

### "I don't see my file in Needs_Action"
```bash
# 1. Check watcher is running
ps aux | grep filesystem_watcher

# 2. Check file is in Downloads
ls ~/Downloads/

# 3. Check file was created recently
ls -lt AI_Employee_Vault/Needs_Action/

# 4. Wait 30 seconds (watcher checks every 30 seconds)
# 5. Restart watcher if needed
python3 watchers/filesystem_watcher.py
```

### "Claude didn't create a plan"
```bash
# 1. Check /Needs_Action has files
ls AI_Employee_Vault/Needs_Action/

# 2. Try with simpler prompt
claude code AI_Employee_Vault
# Prompt: "What's in /Needs_Action?"

# 3. Check Claude has vault access
claude code AI_Employee_Vault
# Prompt: "List all files in /Plans"
```

### "I want to clear Needs_Action and start fresh"
```bash
# 1. Archive old items (safe)
mkdir -p AI_Employee_Vault/Archive/Needs_Action_2026-03-12
mv AI_Employee_Vault/Needs_Action/* \
   AI_Employee_Vault/Archive/Needs_Action_2026-03-12/

# 2. Folder is now empty, ready for new items
ls AI_Employee_Vault/Needs_Action/
# (empty)
```

---

## Best Practices

### DO:
- ✅ Update Dashboard daily
- ✅ Review plans before executing
- ✅ Move completed items to Done
- ✅ Keep Company_Handbook updated
- ✅ Use References for templates
- ✅ Let Watcher create files in Needs_Action
- ✅ Trigger Claude regularly (at least daily)

### DON'T:
- ❌ Manually create files in Needs_Action (let Watcher)
- ❌ Delete Plans without reviewing
- ❌ Leave files in Needs_Action forever (process regularly)
- ❌ Store passwords in Company_Handbook
- ❌ Ignore Claude's plans (provide feedback instead)
- ❌ Forget to update Dashboard (keeps you aware)

---

## Commands Cheat Sheet

```bash
# Check what's waiting
ls AI_Employee_Vault/Needs_Action/
wc -l AI_Employee_Vault/Needs_Action/*

# Read a task
cat AI_Employee_Vault/Needs_Action/FILE_*.md

# Trigger Claude
cd /c/Users/HP/Desktop/H/FTEs/Bronze\ Tier
claude code AI_Employee_Vault

# View plans
ls AI_Employee_Vault/Plans/
cat AI_Employee_Vault/Plans/Plan_*.md

# Mark as done
mv AI_Employee_Vault/Needs_Action/FILE_*.md AI_Employee_Vault/Done/

# Update dashboard
nano AI_Employee_Vault/Dashboard.md

# Check status
cat AI_Employee_Vault/Dashboard.md

# View references
ls AI_Employee_Vault/References/
cat AI_Employee_Vault/References/*/

# Start watcher
python3 watchers/filesystem_watcher.py

# Test setup
python3 test_setup.py
```

---

## Summary

**Remember**:
- Watcher creates files in `/Needs_Action`
- Claude reads files and creates `/Plans`
- You execute plans and move items to `/Done`
- Dashboard tracks everything
- Company_Handbook guides Claude
- References provides templates

**Your main workflows**:
1. Drop file → Watcher creates task → Claude plans → You execute → Mark done
2. Update rules → Company_Handbook → Claude follows on next run
3. Add templates → References → Use when needed → Consistent results

**That's it!** Simple, repeatable cycle that scales to Silver, Gold, and Platinum tiers.
