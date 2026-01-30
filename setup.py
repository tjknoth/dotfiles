#!/usr/bin/env python3
"""
Dotfiles setup script - creates symlinks from system locations to repo files.
"""

import os
import sys
import argparse
from pathlib import Path
import yaml


class DotfilesManager:
    def __init__(self, manifest_path='dotfiles.yaml'):
        self.repo_root = Path(__file__).parent.resolve()
        self.manifest_path = self.repo_root / manifest_path
        self.manifest = self._load_manifest()

    def _load_manifest(self):
        """Load YAML manifest and validate structure"""
        if not self.manifest_path.exists():
            print(f"Error: Manifest file not found at {self.manifest_path}")
            sys.exit(1)

        try:
            with open(self.manifest_path, 'r') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error: Failed to parse manifest: {e}")
            sys.exit(1)

        if not data or 'dotfiles' not in data:
            print("Error: Invalid manifest format - missing 'dotfiles' key")
            sys.exit(1)

        return data['dotfiles']

    def _expand_path(self, path):
        """Expand ~ and environment variables in path"""
        expanded = os.path.expanduser(os.path.expandvars(path))
        return Path(expanded).absolute()

    def _get_source_path(self, source_name):
        """Get absolute path to source file in repo"""
        return self.repo_root / source_name

    def _prompt_overwrite(self, dest_path):
        """Prompt user to confirm overwriting existing file"""
        while True:
            response = input(f"File exists at {dest_path}. Overwrite? (y/n): ").lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'")

    def install_dotfile(self, source_name, destination, dry_run=False, force=False):
        """
        Install a single dotfile by creating a symlink.

        Returns: (success: bool, message: str)
        """
        source_path = self._get_source_path(source_name)
        dest_path = self._expand_path(destination)

        # Check if source file exists in repo
        if not source_path.exists():
            return False, f"Source file not found: {source_path}"

        # Check if destination already exists
        if dest_path.exists() or dest_path.is_symlink():
            # Check if it's already correctly symlinked
            if dest_path.is_symlink():
                try:
                    link_target = dest_path.resolve()
                    if link_target == source_path:
                        return True, f"Already installed (symlink correct)"
                except (OSError, RuntimeError):
                    # Broken symlink
                    if not dry_run:
                        if not force:
                            print(f"Broken symlink found at {dest_path}")
                            if not self._prompt_overwrite(dest_path):
                                return False, "Skipped by user"
                        dest_path.unlink()
                    else:
                        return True, f"Would remove broken symlink"

            # File or incorrect symlink exists
            if not force:
                if dry_run:
                    return True, f"Would prompt to overwrite existing file"
                else:
                    if not self._prompt_overwrite(dest_path):
                        return False, "Skipped by user"

            if not dry_run:
                if dest_path.is_symlink():
                    dest_path.unlink()
                else:
                    dest_path.unlink()

        # Create parent directories if needed
        if not dry_run:
            dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Create symlink
        if dry_run:
            return True, f"Would create symlink: {dest_path} -> {source_path}"
        else:
            try:
                os.symlink(source_path, dest_path)
                return True, f"Installed (symlinked to {source_path})"
            except OSError as e:
                return False, f"Failed to create symlink: {e}"

    def install_all(self, dry_run=False, force=False, specific_files=None):
        """
        Install all dotfiles from manifest (or specific files if provided).

        Args:
            dry_run: Preview without making changes
            force: Overwrite without prompting
            specific_files: List of specific files to install (None = all)
        """
        if specific_files:
            # Filter manifest to only include specific files
            dotfiles_to_install = {k: v for k, v in self.manifest.items()
                                  if k in specific_files}
            # Check for files not in manifest
            missing = set(specific_files) - set(self.manifest.keys())
            if missing:
                print(f"Warning: Files not in manifest: {', '.join(missing)}")
        else:
            dotfiles_to_install = self.manifest

        if not dotfiles_to_install:
            print("No dotfiles to install")
            return

        if dry_run:
            print("DRY RUN - No changes will be made\n")

        results = {'success': 0, 'failed': 0, 'skipped': 0}

        for source_name, destination in dotfiles_to_install.items():
            print(f"Processing {source_name}...")
            success, message = self.install_dotfile(
                source_name, destination, dry_run=dry_run, force=force
            )
            print(f"  {message}")

            if success:
                if "skip" in message.lower():
                    results['skipped'] += 1
                else:
                    results['success'] += 1
            else:
                results['failed'] += 1

        # Print summary
        print(f"\nSummary:")
        print(f"  Successful: {results['success']}")
        print(f"  Failed: {results['failed']}")
        print(f"  Skipped: {results['skipped']}")

        if results['failed'] > 0:
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Install dotfiles by creating symlinks to repo files',
        epilog='Examples:\n'
               '  %(prog)s                    # Install all dotfiles\n'
               '  %(prog)s .tmux.conf        # Install specific file\n'
               '  %(prog)s --dry-run         # Preview without changes\n'
               '  %(prog)s --force           # Overwrite without prompting',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Specific dotfiles to install (default: all)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without making them'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing files without prompting'
    )
    parser.add_argument(
        '--manifest',
        default='dotfiles.yaml',
        help='Path to manifest file (default: dotfiles.yaml)'
    )

    args = parser.parse_args()

    # Create manager and install
    manager = DotfilesManager(manifest_path=args.manifest)
    manager.install_all(
        dry_run=args.dry_run,
        force=args.force,
        specific_files=args.files if args.files else None
    )


if __name__ == '__main__':
    main()
