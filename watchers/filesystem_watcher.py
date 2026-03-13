"""FileSystem Watcher - Monitors a folder for new files"""

import sys
from pathlib import Path
from datetime import datetime
from base_watcher import BaseWatcher


class FileSystemWatcher(BaseWatcher):
    """Monitor a folder for new files and create action items"""

    def __init__(self, vault_path: str, watch_folder: str, check_interval: int = 30):
        """
        Initialize FileSystem Watcher.

        Args:
            vault_path: Path to Obsidian vault
            watch_folder: Folder to monitor (e.g., ~/Downloads)
            check_interval: Seconds between checks (default 30)
        """
        super().__init__(vault_path, check_interval)
        self.watch_folder = Path(watch_folder).expanduser()
        self.processed_files = set()

        if not self.watch_folder.exists():
            self.logger.error(f"Watch folder does not exist: {self.watch_folder}")
            raise ValueError(f"Watch folder not found: {self.watch_folder}")

        self.logger.info(f"Monitoring folder: {self.watch_folder}")

    def check_for_updates(self) -> list:
        """
        Check for new files in watch folder.

        Returns:
            List of new file paths
        """
        if not self.watch_folder.exists():
            return []

        new_files = []
        try:
            for file in self.watch_folder.iterdir():
                if file.is_file():
                    file_path_str = str(file.absolute())
                    if file_path_str not in self.processed_files:
                        new_files.append(file)
                        self.processed_files.add(file_path_str)
        except PermissionError as e:
            self.logger.error(f"Permission denied accessing {self.watch_folder}: {e}")

        return new_files

    def create_action_file(self, source_file: Path) -> Path:
        """
        Create markdown action file for new file.

        Args:
            source_file: Path to the new file

        Returns:
            Path to created action file
        """
        # Create safe filename
        safe_name = source_file.name.replace(' ', '_')
        filename = f"FILE_{safe_name.replace(source_file.suffix, '')}.md"
        action_file = self.needs_action / filename

        # Avoid duplicates
        counter = 1
        while action_file.exists():
            name_part = f"FILE_{safe_name.replace(source_file.suffix, '')}_{counter}"
            action_file = self.needs_action / f"{name_part}.md"
            counter += 1

        try:
            file_size = source_file.stat().st_size
            file_size_kb = round(file_size / 1024, 2)
        except (OSError, ValueError):
            file_size = 0
            file_size_kb = 0

        # Create action file with metadata
        metadata = self.create_metadata_header(
            type='file_drop',
            original_name=source_file.name,
            file_size_bytes=file_size,
            file_size_kb=file_size_kb,
            source_path=str(source_file.absolute()),
            detected_at=datetime.now().isoformat(),
            status='pending'
        )

        content = f"""{metadata}

# New File: {source_file.name}

A new file has been detected in your watch folder.

## File Details
- **Name**: {source_file.name}
- **Size**: {file_size_kb} KB
- **Type**: {source_file.suffix if source_file.suffix else 'No extension'}
- **Location**: {source_file.parent}
- **Detected**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Status
- [ ] Review file
- [ ] Determine action needed
- [ ] Move to Done when processed

## Notes
Add any analysis or next steps below.

---

**Next Step**: Claude will process this file and create a plan if needed.
"""

        try:
            action_file.write_text(content, encoding='utf-8')
            self.logger.info(f"Created action file: {action_file}")
            return action_file
        except Exception as e:
            self.logger.error(f"Error creating action file: {e}")
            raise


def main():
    """Main entry point"""
    # Configuration - update these paths
    VAULT_PATH = "/c/Users/HP/Desktop/H/FTEs/Bronze Tier/AI_Employee_Vault"
    WATCH_FOLDER = "~/Downloads"

    try:
        watcher = FileSystemWatcher(VAULT_PATH, WATCH_FOLDER, check_interval=30)
        watcher.run()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nUsage: python3 filesystem_watcher.py")
        print(f"\nMake sure to update VAULT_PATH and WATCH_FOLDER in the script.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nWatcher stopped by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
