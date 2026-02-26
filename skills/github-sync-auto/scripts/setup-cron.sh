#!/bin/bash
# GitHub Sync Auto - Cron Setup Script
# Sets up automatic 20-hour GitHub sync for OpenClaw workspace

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYNC_SCRIPT="$SCRIPT_DIR/github-sync.sh"
CRON_JOB_FILE="/tmp/github-sync-cron-job"
OPENCLAW_WORKSPACE="$HOME/.openclaw/workspace"

log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Check if OpenClaw workspace exists
if [ ! -d "$OPENCLAW_WORKSPACE" ]; then
    error "OpenClaw workspace not found at: $OPENCLAW_WORKSPACE"
    exit 1
fi

# Check if sync script exists and is executable
if [ ! -f "$SYNC_SCRIPT" ]; then
    error "Sync script not found: $SYNC_SCRIPT"
    exit 1
fi

chmod +x "$SYNC_SCRIPT"

# Create cron job entry
# Run every 20 hours (at 00:00, 20:00, 16:00, 12:00, 08:00, then repeat)
# Using */20 doesn't work as expected, so we use specific hours
CRON_SCHEDULE="0 0,4,8,12,16,20 * * *"
CRON_COMMAND="$SYNC_SCRIPT >> \"$OPENCLAW_WORKSPACE/logs/github-sync.log\" 2>&1"

# Create cron job file
cat > "$CRON_JOB_FILE" << EOF
# GitHub Sync Auto - Automatic backup every 20 hours
$CRON_SCHEDULE $CRON_COMMAND
EOF

# Add existing cron jobs (excluding our job to avoid duplicates)
(crontab -l 2>/dev/null | grep -v "github-sync.sh" || true) > /tmp/existing-cron
cat /tmp/existing-cron "$CRON_JOB_FILE" | crontab -

# Cleanup
rm -f /tmp/existing-cron "$CRON_JOB_FILE"

# Create logs directory
mkdir -p "$OPENCLAW_WORKSPACE/logs"

log "GitHub sync cron job installed successfully!"
log "Schedule: Every 20 hours (00:00, 04:00, 08:00, 12:00, 16:00, 20:00)"
log "Logs will be written to: $OPENCLAW_WORKSPACE/logs/github-sync.log"
log "To remove the cron job, run: crontab -l | grep -v 'github-sync.sh' | crontab -"

# Test the sync script
log "Testing sync script..."
if "$SYNC_SCRIPT" --dry-run; then
    log "Dry run completed successfully!"
else
    warn "Dry run failed - please check GitHub configuration"
fi