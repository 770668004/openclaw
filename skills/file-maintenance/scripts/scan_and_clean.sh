#!/bin/bash

# File Maintenance Skill - Scan and Clean Script
# This script performs automated file review, cleanup, and optimization

set -euo pipefail

WORKSPACE_DIR="$HOME/.openclaw/workspace"
LOG_FILE="$WORKSPACE_DIR/memory/file-maintenance-$(date +%Y-%m-%d).log"

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to check for dangerous content
check_dangerous_content() {
    local file="$1"
    
    # Skip binary files
    if ! file "$file" | grep -q "text"; then
        return 0
    fi
    
    # Check for obvious dangerous patterns
    if grep -l -E "(rm -rf|:(){ :|:& };:|dd if=/dev/zero|mkfs|/dev/null >)" "$file" >/dev/null 2>&1; then
        log "WARNING: Potentially dangerous content detected in $file"
        return 1
    fi
    
    return 0
}

# Function to find duplicate files
find_duplicates() {
    local dir="$1"
    log "Scanning for duplicate files in $dir"
    
    # Simple duplicate detection based on content hash
    find "$dir" -type f -name "*.md" -exec md5sum {} \; | sort | uniq -w32 -d > /tmp/duplicates.tmp
    
    if [ -s /tmp/duplicates.tmp ]; then
        log "Found potential duplicates:"
        cat /tmp/duplicates.tmp >> "$LOG_FILE"
    fi
    
    rm -f /tmp/duplicates.tmp
}

# Function to validate file structure
validate_files() {
    local dir="$1"
    log "Validating file structure in $dir"
    
    # Check for common file issues
    find "$dir" -type f -name "*.md" | while read -r file; do
        # Check if file is readable
        if ! [ -r "$file" ]; then
            log "ERROR: File not readable: $file"
            continue
        fi
        
        # Check for dangerous content
        if ! check_dangerous_content "$file"; then
            log "ACTION: Flagging suspicious file for review: $file"
            # In a real implementation, this would move to quarantine or notify user
        fi
    done
}

# Main execution
main() {
    log "Starting file maintenance scan"
    
    # Validate workspace files
    validate_files "$WORKSPACE_DIR"
    
    # Find duplicates
    find_duplicates "$WORKSPACE_DIR"
    
    # Check memory directory specifically
    if [ -d "$WORKSPACE_DIR/memory" ]; then
        validate_files "$WORKSPACE_DIR/memory"
    fi
    
    # Check skills directory
    if [ -d "$WORKSPACE_DIR/skills" ]; then
        validate_files "$WORKSPACE_DIR/skills"
    fi
    
    log "File maintenance scan completed"
}

# Run main function
main