"""Vault Processor - Watches Needs_Action for checked items and auto-processes them"""

import time
import logging
import re
from pathlib import Path
from datetime import datetime


class VaultProcessor:
    """Monitor Needs_Action/ for files with all checkboxes checked, then auto-process"""

    def __init__(self, vault_path: str, check_interval: int = 5):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.plans = self.vault_path / 'Plans'
        self.done = self.vault_path / 'Done'
        self.check_interval = check_interval

        # Setup logging
        self.logger = logging.getLogger('VaultProcessor')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Ensure folders exist
        for folder in [self.needs_action, self.plans, self.done]:
            folder.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Vault Processor started")
        self.logger.info(f"Watching: {self.needs_action}")
        self.logger.info(f"Checking every {self.check_interval} seconds")

    def is_fully_checked(self, file_path: Path) -> bool:
        """Check if all checkboxes in file are checked [x]"""
        try:
            content = file_path.read_text(encoding='utf-8')
            unchecked = re.findall(r'- \[ \]', content)
            checked = re.findall(r'- \[x\]', content, re.IGNORECASE)

            # All boxes must be checked, and at least one must exist
            return len(checked) > 0 and len(unchecked) == 0
        except Exception as e:
            self.logger.error(f"Error reading {file_path}: {e}")
            return False

    def extract_metadata(self, content: str) -> dict:
        """Extract YAML metadata from file"""
        metadata = {}
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                for line in parts[1].strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip()
        return metadata

    def read_source_file(self, source_path: str) -> str:
        """Read the original source file content"""
        try:
            path = Path(source_path)
            if path.exists():
                content = path.read_text(encoding='utf-8')
                # Return first 2000 chars for summary
                return content[:2000]
            return "Source file not found"
        except Exception as e:
            return f"Could not read source: {e}"

    def create_plan(self, action_file: Path) -> Path:
        """Create a plan file from the processed action item"""
        content = action_file.read_text(encoding='utf-8')
        metadata = self.extract_metadata(content)

        original_name = metadata.get('original_name', action_file.stem)
        source_path = metadata.get('source_path', '')
        file_size = metadata.get('file_size_kb', '0')
        detected = metadata.get('detected_at', '')

        # Read source file for analysis
        source_content = self.read_source_file(source_path) if source_path else ""

        # Create plan filename
        safe_name = original_name.replace(' ', '_').replace('.', '_')
        plan_file = self.plans / f"Plan_{safe_name}.md"

        # Avoid duplicates
        counter = 1
        while plan_file.exists():
            plan_file = self.plans / f"Plan_{safe_name}_{counter}.md"
            counter += 1

        now = datetime.now()

        # Generate summary from source content
        summary = self.generate_summary(original_name, source_content)

        plan_content = f"""---
type: plan
source_file: {action_file.name}
original_file: {original_name}
created: {now.isoformat()}
status: completed
processed_by: vault_processor
---

# Plan: {original_name}

## File Info
- **Name**: {original_name}
- **Size**: {file_size} KB
- **Detected**: {detected}
- **Processed**: {now.strftime('%Y-%m-%d %H:%M:%S')}

## Summary

{summary}

## Source Preview

```
{source_content[:500] if source_content else 'No source content available'}
```

## Status
- [x] File detected by watcher
- [x] User reviewed and approved
- [x] Plan created
- [x] Moved to Done

---

**Auto-processed by**: Vault Processor (Bronze Tier)
**Date**: {now.strftime('%Y-%m-%d %H:%M:%S')}
"""

        plan_file.write_text(plan_content, encoding='utf-8')
        self.logger.info(f"Plan created: {plan_file.name}")
        return plan_file

    def generate_summary(self, filename: str, content: str) -> str:
        """Generate a basic summary based on file content"""
        if not content or content == "Source file not found":
            return f"File '{filename}' was detected and approved for processing. Source file was not available for analysis."

        # Count some basic stats
        lines = content.split('\n')
        words = len(content.split())
        headings = [l for l in lines if l.startswith('#')]

        summary = f"File '{filename}' contains approximately {words} words"
        if headings:
            summary += f" with {len(headings)} sections"
            summary += ":\n"
            for h in headings[:10]:
                summary += f"- {h.strip()}\n"
        else:
            summary += "."

        return summary

    def update_dashboard(self, original_name: str, plan_name: str):
        """Update Dashboard.md with latest activity"""
        dashboard = self.vault_path / 'Dashboard.md'
        now = datetime.now()

        # Count items in each folder
        needs_count = len(list(self.needs_action.glob('*.md')))
        plans_count = len(list(self.plans.glob('*.md')))
        done_count = len(list(self.done.glob('*.md')))

        dashboard_content = f"""# Dashboard

**Last Updated**: {now.strftime('%Y-%m-%d %H:%M:%S')}
**Status**: Bronze Tier - ACTIVE
**System**: Vault Processor Running

## Status Summary

- **Pending Items**: {needs_count}
- **Completed Today**: {done_count}
- **Plans Created**: {plans_count}
- **Active Projects**: {plans_count}

## Latest Activity

| Time | Item | Action | Status |
|------|------|--------|--------|
| {now.strftime('%H:%M')} | {original_name} | Auto-processed, plan created | Done |

## Folder Status

| Folder | Items |
|--------|-------|
| Needs_Action/ | {needs_count} |
| Plans/ | {plans_count} |
| Done/ | {done_count} |
| Downloads/ | Being monitored |

## Recent Plans

"""
        # List recent plans
        for plan in sorted(self.plans.glob('*.md'), key=lambda p: p.stat().st_mtime, reverse=True)[:5]:
            dashboard_content += f"- **{plan.name}**\n"

        dashboard_content += f"""
## System Health

- FileSystem Watcher: Running (monitors Downloads/)
- Vault Processor: Running (monitors Needs_Action/)
- Last Process: {now.strftime('%Y-%m-%d %H:%M:%S')}

## How It Works

1. Drop file in Downloads/ folder
2. FileSystem Watcher creates task in Needs_Action/
3. Open the .md file in Obsidian
4. Check all boxes: [x] Review, [x] Determine action, [x] Move to Done
5. Vault Processor auto-detects and processes it
6. Plan created in Plans/, file moved to Done/
7. Dashboard updated automatically

---
**Auto-updated by Vault Processor**
"""

        dashboard.write_text(dashboard_content, encoding='utf-8')
        self.logger.info("Dashboard updated")

    def process_file(self, action_file: Path):
        """Full processing: create plan, move to done, update dashboard"""
        self.logger.info(f"Processing: {action_file.name}")

        content = action_file.read_text(encoding='utf-8')
        metadata = self.extract_metadata(content)
        original_name = metadata.get('original_name', action_file.stem)

        # Step 1: Create plan
        plan_file = self.create_plan(action_file)

        # Step 2: Move to Done
        done_file = self.done / action_file.name
        counter = 1
        while done_file.exists():
            stem = action_file.stem
            done_file = self.done / f"{stem}_{counter}.md"
            counter += 1

        action_file.rename(done_file)
        self.logger.info(f"Moved to Done: {done_file.name}")

        # Step 3: Update Dashboard
        self.update_dashboard(original_name, plan_file.name)

        self.logger.info(f"COMPLETE: {original_name} -> Plan created, Dashboard updated")

    def run(self):
        """Main loop: check Needs_Action for fully-checked files"""
        self.logger.info("=" * 50)
        self.logger.info("Vault Processor RUNNING")
        self.logger.info("Waiting for checked files in Needs_Action/...")
        self.logger.info("=" * 50)

        while True:
            try:
                for md_file in self.needs_action.glob('*.md'):
                    if self.is_fully_checked(md_file):
                        self.process_file(md_file)
            except Exception as e:
                self.logger.error(f"Error: {e}")

            time.sleep(self.check_interval)


def main():
    VAULT_PATH = str(Path(__file__).parent.parent / "AI_Employee_Vault")

    try:
        processor = VaultProcessor(VAULT_PATH, check_interval=5)
        processor.run()
    except KeyboardInterrupt:
        print("\nVault Processor stopped.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
