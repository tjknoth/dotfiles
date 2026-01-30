# Dotfiles Management

A simple, symlink-based dotfiles management system. Edit your configs anywhere - changes automatically sync to the repo.

## Quick Start

### Setup on a New Machine

```bash
# Clone the repo
git clone <repo-url> ~/dotfiles
cd ~/dotfiles

# Install PyYAML (required dependency)
pip install pyyaml
# OR on Debian/Ubuntu:
# sudo apt install python3-yaml

# Install all dotfiles
./setup.py

# Verify installation
./status.py
```

That's it! Your dotfiles are now symlinked to files in this repo.

## How It Works

This system uses **symlinks** instead of copying files. When you run `./setup.py`:

1. It reads `dotfiles.yaml` to see which files to manage
2. Creates symlinks from your home directory to files in this repo
3. Now when you edit `~/.tmux.conf`, you're actually editing `~/dotfiles/.tmux.conf`

**Key benefit:** No sync needed! Changes to `~/.tmux.conf` automatically appear in git.

## Adding a New Dotfile

```bash
# 1. Copy the config file to the repo
cp ~/.gitconfig ~/dotfiles/

# 2. Add it to the manifest
echo "  .gitconfig: ~/.gitconfig" >> dotfiles.yaml

# 3. Install the symlink
./setup.py .gitconfig

# 4. Commit to git
git add .gitconfig dotfiles.yaml
git commit -m "Add gitconfig"
```

## Common Workflows

### Editing Configs

Edit from anywhere - both locations are the same file:

```bash
# Edit via home directory symlink
vim ~/.tmux.conf

# OR edit directly in repo
vim ~/dotfiles/.tmux.conf

# Both work! Check changes:
cd ~/dotfiles
git diff
```

### Installing a Specific Dotfile

```bash
# Install just one file
./setup.py .tmux.conf

# Install multiple specific files
./setup.py .tmux.conf .gitconfig
```

### Previewing Changes (Dry Run)

```bash
# See what would happen without making changes
./setup.py --dry-run
```

### Force Overwrite

```bash
# Overwrite existing files without prompting
./setup.py --force
```

### Checking Status

```bash
# Show status of all dotfiles
./status.py

# Exit with error if any issues (useful for scripts)
./status.py --check
```

## File Structure

```
~/dotfiles/
├── dotfiles.yaml          # Manifest - defines which files to manage
├── setup.py               # Installation script
├── status.py              # Status checker and repair tool
├── README.md              # This file
├── .tmux.conf            # Active dotfile
├── .claude/              # Claude settings (not symlinked)
└── archive/              # Old configs for reference
```

## Manifest Format

The `dotfiles.yaml` file is simple and human-readable:

```yaml
# Dotfiles manifest - maps repo files to system locations

dotfiles:
  .tmux.conf: ~/.tmux.conf      # Format: repo_file: destination_path
  .gitconfig: ~/.gitconfig
  .vimrc: ~/.vimrc
```

- **Left side:** File name in this repo
- **Right side:** Where to create the symlink (supports `~` and environment variables)

## Conflict Handling

When you run `./setup.py` and a file already exists at the destination:

- **Interactive mode:** Prompts you to overwrite (y/n)
- **Force mode (`--force`):** Automatically overwrites without prompting
- **Already installed:** Skips if symlink already points to correct location

No automatic backups are created (git history provides versioning).

## Troubleshooting

### "Source file not found" error

The file listed in `dotfiles.yaml` doesn't exist in the repo. Either:
- Add the file to the repo, or
- Remove the entry from `dotfiles.yaml`

### Symlink points to wrong location

Run with force to recreate:
```bash
./setup.py .tmux.conf --force
```

### Permission denied

Make sure scripts are executable:
```bash
chmod +x setup.py status.py
```

### Broken symlink detected

Usually happens if you moved/deleted the repo. Fix with:
```bash
./setup.py --force
```

## Requirements

- Python 3.6+
- PyYAML (`pip install pyyaml` or `apt install python3-yaml`)

## Comparison with Old Approach

**Old system (archived):**
- Used `setup_all.py` and `update_all.py`
- Required running update script to sync changes
- Bidirectional copying between home and repo

**New system:**
- Symlink-based (no sync needed)
- Edit anywhere, changes auto-reflect in repo
- Simpler: just `setup.py` once per machine
- Declarative manifest (YAML)

Old scripts are in `archive/` for reference.

## Migration Notes

Currently managed dotfiles:
- `.tmux.conf` - Active tmux configuration

Previously used configs (now archived):
- `.bashrc`, `.zshrc`, `.vimrc` - In `archive/` directory
- Old i3, i3blocks configs and scripts - In `archive/` directory

To restore an archived config, copy it back to repo root and add to `dotfiles.yaml`.
