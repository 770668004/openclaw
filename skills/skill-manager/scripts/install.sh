#!/bin/bash
# Skill Manager Installation Script

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$SKILL_DIR/scripts"

# Create necessary directories
mkdir -p "$SCRIPTS_DIR"

# Make scripts executable
chmod +x "$SCRIPTS_DIR/list-skills.sh"

# Create symbolic link for easy access (optional)
if [ -d "$HOME/.local/bin" ]; then
    ln -sf "$SCRIPTS_DIR/list-skills.sh" "$HOME/.local/bin/skill-manager" 2>/dev/null || true
fi

echo "✅ Skill Manager installed successfully!"
echo "Usage: skill-manager [category] or skill-manager --help"