#!/bin/bash

# GitHub Auto Sync Script
# Automatically syncs OpenClaw workspace to GitHub repository
# Runs every 20 hours as configured

set -euo pipefail

# Configuration
WORKSPACE_DIR="${OPENCLAW_WORKSPACE:-/home/kousoyu/.openclaw/workspace}"
LOG_FILE="$WORKSPACE_DIR/logs/github-sync.log"
MAX_LOG_SIZE=10485760  # 10MB
GIT_REMOTE="origin"
GIT_BRANCH="main"

# Colors for logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create logs directory if it doesn't exist
mkdir -p "$WORKSPACE_DIR/logs"

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# Rotate log file if too large
rotate_log() {
    if [ -f "$LOG_FILE" ] && [ $(stat -c%s "$LOG_FILE") -gt $MAX_LOG_SIZE ]; then
        mv "$LOG_FILE" "$LOG_FILE.old"
        log "INFO" "Rotated log file due to size limit"
    fi
}

# Check if git is available
check_git() {
    if ! command -v git &> /dev/null; then
        log "ERROR" "Git is not installed or not in PATH"
        exit 1
    fi
}

# Check if we're in a git repository
check_git_repo() {
    if ! git -C "$WORKSPACE_DIR" rev-parse --git-dir > /dev/null 2>&1; then
        log "ERROR" "Workspace directory is not a git repository"
        exit 1
    fi
}

# Check git remote configuration
check_git_remote() {
    if ! git -C "$WORKSPACE_DIR" remote get-url "$GIT_REMOTE" > /dev/null 2>&1; then
        log "ERROR" "Git remote '$GIT_REMOTE' not configured"
        exit 1
    fi
}

# Add and commit changes
commit_changes() {
    local commit_message="Auto-sync: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Check if there are any changes
    if ! git -C "$WORKSPACE_DIR" diff --quiet --cached && ! git -C "$WORKSPACE_DIR" diff --quiet; then
        log "INFO" "No changes to commit"
        return 0
    fi
    
    # Add all changes
    git -C "$WORKSPACE_DIR" add .
    
    # Check if there are staged changes
    if git -C "$WORKSPACE_DIR" diff --cached --quiet; then
        log "INFO" "No new changes to commit"
        return 0
    fi
    
    # Commit changes
    if git -C "$WORKSPACE_DIR" commit -m "$commit_message"; then
        log "INFO" "Successfully committed changes: $commit_message"
        return 0
    else
        log "ERROR" "Failed to commit changes"
        return 1
    fi
}

# Pull latest changes from remote
pull_latest() {
    log "INFO" "Pulling latest changes from $GIT_REMOTE/$GIT_BRANCH"
    if git -C "$WORKSPACE_DIR" pull "$GIT_REMOTE" "$GIT_BRANCH" --rebase; then
        log "INFO" "Successfully pulled latest changes"
        return 0
    else
        log "WARN" "Failed to pull latest changes, may have conflicts"
        # Try to continue anyway
        return 0
    fi
}

# Push changes to remote
push_changes() {
    log "INFO" "Pushing changes to $GIT_REMOTE/$GIT_BRANCH"
    if git -C "$WORKSPACE_DIR" push "$GIT_REMOTE" "$GIT_BRANCH"; then
        log "INFO" "Successfully pushed changes to remote"
        return 0
    else
        log "ERROR" "Failed to push changes to remote"
        return 1
    fi
}

# Main sync function
main() {
    log "INFO" "Starting GitHub auto-sync process"
    
    # Rotate log if needed
    rotate_log
    
    # Check prerequisites
    check_git
    check_git_repo
    check_git_remote
    
    # Ensure we're on the correct branch
    current_branch=$(git -C "$WORKSPACE_DIR" rev-parse --abbrev-ref HEAD)
    if [ "$current_branch" != "$GIT_BRANCH" ]; then
        log "INFO" "Switching to branch $GIT_BRANCH"
        if ! git -C "$WORKSPACE_DIR" checkout "$GIT_BRANCH"; then
            log "ERROR" "Failed to switch to branch $GIT_BRANCH"
            exit 1
        fi
    fi
    
    # Pull latest changes first (to avoid conflicts)
    if ! pull_latest; then
        log "WARN" "Continuing despite pull issues"
    fi
    
    # Commit any local changes
    if ! commit_changes; then
        log "ERROR" "Failed to commit changes, aborting sync"
        exit 1
    fi
    
    # Push to remote
    if ! push_changes; then
        log "ERROR" "Failed to push changes, sync incomplete"
        exit 1
    fi
    
    log "INFO" "GitHub auto-sync completed successfully"
}

# Handle interrupts gracefully
cleanup() {
    log "WARN" "Sync interrupted by signal"
    exit 1
}

trap cleanup SIGINT SIGTERM

# Run main function
main "$@"