#!/usr/bin/env python3
"""
Test script to verify Bronze Tier setup
Run: python3 test_setup.py
"""

import sys
from pathlib import Path

def test_vault_structure():
    """Verify Obsidian vault folder structure"""
    print("=" * 60)
    print("Testing Vault Structure...")
    print("=" * 60)

    vault_path = Path(__file__).parent / "AI_Employee_Vault"
    required_folders = ["Inbox", "Needs_Action", "Done", "Plans", "References"]
    required_files = ["Dashboard.md", "Company_Handbook.md"]

    all_ok = True

    # Check folders
    print("\nChecking folders:")
    for folder in required_folders:
        folder_path = vault_path / folder
        if folder_path.exists() and folder_path.is_dir():
            print(f"  [OK] {folder}/")
        else:
            print(f"  [FAIL] {folder}/ - MISSING")
            all_ok = False

    # Check files
    print("\nChecking files:")
    for file in required_files:
        file_path = vault_path / file
        if file_path.exists() and file_path.is_file():
            size = file_path.stat().st_size
            print(f"  [OK] {file} ({size} bytes)")
        else:
            print(f"  [FAIL] {file} - MISSING")
            all_ok = False

    return all_ok


def test_watcher_files():
    """Verify Watcher script files exist"""
    print("\n" + "=" * 60)
    print("Testing Watcher Scripts...")
    print("=" * 60)

    base_path = Path(__file__).parent / "watchers"
    required_files = ["base_watcher.py", "filesystem_watcher.py"]

    all_ok = True

    print("\nChecking watcher files:")
    for file in required_files:
        file_path = base_path / file
        if file_path.exists() and file_path.is_file():
            size = file_path.stat().st_size
            print(f"  [OK] {file} ({size} bytes)")
        else:
            print(f"  [FAIL] {file} - MISSING")
            all_ok = False

    return all_ok


def test_imports():
    """Test that base_watcher can be imported"""
    print("\n" + "=" * 60)
    print("Testing Python Imports...")
    print("=" * 60)

    sys.path.insert(0, str(Path(__file__).parent / "watchers"))

    try:
        from base_watcher import BaseWatcher
        print("  [OK] Successfully imported BaseWatcher")
        return True
    except ImportError as e:
        print(f"  [FAIL] Failed to import BaseWatcher: {e}")
        return False


def test_watcher_instantiation():
    """Test that FileSystemWatcher can be instantiated"""
    print("\n" + "=" * 60)
    print("Testing Watcher Instantiation...")
    print("=" * 60)

    sys.path.insert(0, str(Path(__file__).parent / "watchers"))

    try:
        from filesystem_watcher import FileSystemWatcher
        vault_path = Path(__file__).parent / "AI_Employee_Vault"
        watch_folder = Path.home() / "Downloads"

        if not watch_folder.exists():
            print(f"  [WARN] Watch folder doesn't exist: {watch_folder}")
            print(f"    (This is OK - watcher will still work)")
            return True

        watcher = FileSystemWatcher(str(vault_path), str(watch_folder))
        print(f"  [OK] FileSystemWatcher initialized successfully")
        print(f"    - Vault: {vault_path}")
        print(f"    - Watch: {watch_folder}")
        return True
    except Exception as e:
        print(f"  [FAIL] Failed to instantiate FileSystemWatcher: {e}")
        return False


def main():
    """Run all tests"""
    print("\n")
    print("=" * 60)
    print("BRONZE TIER SETUP TEST".center(60))
    print("=" * 60)

    results = []

    results.append(("Vault Structure", test_vault_structure()))
    results.append(("Watcher Files", test_watcher_files()))
    results.append(("Python Imports", test_imports()))
    results.append(("Watcher Instantiation", test_watcher_instantiation()))

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n[OK] All tests passed! Bronze Tier is ready.")
        print("\nNext steps:")
        print("  1. Test the Watcher: python3 watchers/filesystem_watcher.py")
        print("  2. Drop a file in ~/Downloads")
        print("  3. Check AI_Employee_Vault/Needs_Action for new .md file")
        print("  4. Run: claude code AI_Employee_Vault")
        return 0
    else:
        print("\n[FAIL] Some tests failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
