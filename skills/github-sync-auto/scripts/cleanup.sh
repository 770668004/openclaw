#!/bin/bash

# GitHub Sync Auto - Cleanup Script
# Cleans up old logs and temporary files

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.json"
LOG_DIR="$SCRIPT_DIR/../logs"
MAX_LOG_AGE_DAYS=30

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" >&2
}

# Check if config exists
if [[ ! -f "$CONFIG_FILE" ]]; then
    error "Configuration file not found: $CONFIG_FILE"
    exit 1
fi

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Clean up old log files
log "Cleaning up log files older than $MAX_LOG_AGE_DAYS days..."
find "$LOG_DIR" -name "*.log" -type f -mtime +$MAX_LOG_AGE_DAYS -delete 2>/dev/null || true

# Clean up temporary files
log "Cleaning up temporary files..."
find "$SCRIPT_DIR" -name "*.tmp" -type f -delete 2>/dev/null || true
find "$SCRIPT_DIR" -name "*.bak" -type f -delete 2>/dev/null || true

# Clean up old sync state files (keep last 5)
log "Cleaning up old sync state files..."
ls -t "$LOG_DIR"/sync-state-*.json 2>/dev/null | tail -n +6 | xargs -r rm

# Clean up empty directories
log "Cleaning up empty directories..."
find "$LOG_DIR" -type d -empty -delete 2>/dev/null || true

log "Cleanup completed successfully!"
exit 0