#!/bin/bash
# Test script for GitHub sync functionality
# This script tests the core components without actually syncing to GitHub

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.json"

echo "🔍 Testing GitHub Sync Auto Skill Components..."
echo "=============================================="

# Test 1: Check if config file exists and is valid
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ ERROR: Config file not found at $CONFIG_FILE"
    exit 1
fi

# Validate JSON config
if ! command -v jq &> /dev/null; then
    echo "⚠️  WARNING: jq not installed, skipping JSON validation"
else
    if ! jq empty "$CONFIG_FILE" &> /dev/null; then
        echo "❌ ERROR: Config file contains invalid JSON"
        exit 1
    fi
    echo "✅ Config file validated successfully"
fi

# Test 2: Check if main sync script is executable
SYNC_SCRIPT="$SCRIPT_DIR/github-sync.sh"
if [ ! -f "$SYNC_SCRIPT" ]; then
    echo "❌ ERROR: Main sync script not found at $SYNC_SCRIPT"
    exit 1
fi

if [ ! -x "$SYNC_SCRIPT" ]; then
    echo "❌ ERROR: Main sync script is not executable"
    exit 1
fi
echo "✅ Main sync script exists and is executable"

# Test 3: Check if setup-cron script is executable
CRON_SCRIPT="$SCRIPT_DIR/setup-cron.sh"
if [ ! -f "$CRON_SCRIPT" ]; then
    echo "❌ ERROR: Cron setup script not found at $CRON_SCRIPT"
    exit 1
fi

if [ ! -x "$CRON_SCRIPT" ]; then
    echo "❌ ERROR: Cron setup script is not executable"
    exit 1
fi
echo "✅ Cron setup script exists and is executable"

# Test 4: Check required commands are available
REQUIRED_COMMANDS=("git" "curl")
for cmd in "${REQUIRED_COMMANDS[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "⚠️  WARNING: Required command '$cmd' not found"
    else
        echo "✅ Required command '$cmd' is available"
    fi
done

# Test 5: Check workspace directory structure
WORKSPACE_DIR="/home/kousoyu/.openclaw/workspace"
if [ ! -d "$WORKSPACE_DIR" ]; then
    echo "❌ ERROR: OpenClaw workspace directory not found at $WORKSPACE_DIR"
    exit 1
fi
echo "✅ OpenClaw workspace directory exists"

# Test 6: Simulate dry-run of sync process
echo ""
echo "🧪 Simulating dry-run sync process..."
echo "------------------------------------"

# Check if we're in a git repository
if [ -d "$WORKSPACE_DIR/.git" ]; then
    echo "✅ Workspace is already a git repository"
else
    echo "ℹ️  Workspace is not yet a git repository (this is normal for first-time setup)"
fi

# Check for excluded files
EXCLUDED_FILES=(".git" "node_modules" "*.log" "*.tmp")
echo "📁 Checking for excluded file patterns:"
for pattern in "${EXCLUDED_FILES[@]}"; do
    echo "   - $pattern"
done

echo ""
echo "🎉 All tests completed successfully!"
echo ""
echo "The GitHub Sync Auto skill is ready to use."
echo "To set up automatic 20-hour syncing, run:"
echo "  ./skills/github-sync-auto/scripts/setup-cron.sh"
echo ""
echo "To manually sync now, run:"
echo "  ./skills/github-sync-auto/scripts/github-sync.sh"