#!/usr/bin/env python3
"""
Dotfiles status script - verify symlinks and check installation state.
"""

import os
import sys
import argparse
from pathlib import Path
import yaml


class DotfilesStatus:
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

    def check_status(self, source_name, destination):
        """
        Check installation status of a single dotfile.

        Returns: (status: str, is_ok: bool, message: str)
        """
        source_path = self._get_source_path(source_name)
        dest_path = self._expand_path(destination)

        # Check if source exists in repo
        if not source_path.exists():
            return "ERROR", False, f"Source file missing in repo: {source_path}"

        # Check if destination is a symlink first (is_symlink works even for broken symlinks)
        if not dest_path.is_symlink():
            # Not a symlink - either doesn't exist or is a regular file
            if not dest_path.exists():
                return "NOT_INSTALLED", False, "Not installed"
            else:
                return "WARNING", False, "File exists but not symlinked"

        # Check if symlink points to correct location
        try:
            link_target = dest_path.resolve()
            if link_target == source_path:
                return "OK", True, f"Installed (symlinked to {source_path})"
            else:
                return "WARNING", False, f"Symlink points to wrong location: {link_target}"
        except (OSError, RuntimeError):
            return "ERROR", False, "Broken symlink"

    def verify_all(self):
        """
        Verify all dotfiles and print status report.

        Returns: True if all dotfiles are correctly installed, False otherwise
        """
        print("Dotfile Status:\n")

        all_ok = True
        status_counts = {'OK': 0, 'WARNING': 0, 'ERROR': 0, 'NOT_INSTALLED': 0}

        for source_name, destination in self.manifest.items():
            status, is_ok, message = self.check_status(source_name, destination)
            status_counts[status] += 1

            if not is_ok:
                all_ok = False

            # Format output with status indicator
            indicator = "✓" if is_ok else "✗"
            print(f"  {indicator} {source_name:<20} {message}")

        # Print summary
        print(f"\nSummary:")
        print(f"  Installed correctly: {status_counts['OK']}")
        if status_counts['NOT_INSTALLED'] > 0:
            print(f"  Not installed: {status_counts['NOT_INSTALLED']}")
        if status_counts['WARNING'] > 0:
            print(f"  Warnings: {status_counts['WARNING']}")
        if status_counts['ERROR'] > 0:
            print(f"  Errors: {status_counts['ERROR']}")

        return all_ok



def main():
    parser = argparse.ArgumentParser(
        description='Check status and verify dotfiles installation',
        epilog='Examples:\n'
               '  %(prog)s              # Show status of all dotfiles\n'
               '  %(prog)s --check      # Exit with error if any issues',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Exit with error code if any dotfiles have issues'
    )
    parser.add_argument(
        '--manifest',
        default='dotfiles.yaml',
        help='Path to manifest file (default: dotfiles.yaml)'
    )

    args = parser.parse_args()

    # Create status checker and verify
    status = DotfilesStatus(manifest_path=args.manifest)
    all_ok = status.verify_all()

    if args.check and not all_ok:
        sys.exit(1)


if __name__ == '__main__':
    main()
