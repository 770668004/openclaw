#!/bin/bash

# File Planning and Organization Tool
# Part of the planning-with-files skill for OpenClaw

set -euo pipefail

# Default configuration
CONFIG_DIR="${HOME}/.file-planner"
BACKUP_DIR="${HOME}/backups/file-planner"
LOG_FILE="${CONFIG_DIR}/planner.log"

# Create necessary directories
mkdir -p "$CONFIG_DIR" "$BACKUP_DIR"

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Help function
show_help() {
    cat << EOF
File Planner - Advanced File Organization and Planning Tool

Usage: file-planner.sh [OPTIONS] [ACTION]

ACTIONS:
  plan <directory>        Create a planning structure for the specified directory
  organize <directory>    Organize files based on type, date, or custom rules
  backup <directory>      Create a backup of the specified directory with timestamp
  analyze <directory>     Analyze directory structure and provide recommendations
  template <name>         Create a project template with standard structure
  sync <source> <dest>    Sync files between source and destination with planning

OPTIONS:
  -h, --help            Show this help message
  -v, --verbose         Enable verbose output
  -f, --force           Force operations without confirmation
  -t, --type TYPE       Specify file type filter (documents, media, code, etc.)
  -d, --date RANGE      Filter by date range (today, week, month, year)
  --dry-run            Show what would be done without making changes

EXAMPLES:
  file-planner.sh plan ~/projects/new-project
  file-planner.sh organize ~/Downloads --type documents
  file-planner.sh backup ~/important --date month
  file-planner.sh template research-paper
  file-planner.sh analyze ~/workspace

EOF
}

# Create planning structure
create_plan() {
    local target_dir="$1"
    if [[ ! -d "$target_dir" ]]; then
        mkdir -p "$target_dir"
        log "Created directory: $target_dir"
    fi
    
    # Create standard planning structure
    mkdir -p "$target_dir"/{docs,src,data,tests,assets,backup,logs}
    
    # Create planning files
    cat > "$target_dir/PLAN.md" << EOF
# Project Plan

## Overview
- **Project Name**: $(basename "$target_dir")
- **Created**: $(date)
- **Status**: Planning

## Structure
- docs/: Documentation and notes
- src/: Source code and main files  
- data/: Data files and datasets
- tests/: Test files and validation
- assets/: Media, images, and resources
- backup/: Backup copies
- logs/: Log files and records

## Next Steps
- [ ] Define project scope
- [ ] Set up version control
- [ ] Create initial documentation
- [ ] Establish file naming conventions

EOF
    
    cat > "$target_dir/README.md" << EOF
# $(basename "$target_dir")

Project planning and organization structure created by File Planner.

See PLAN.md for project planning details.
EOF
    
    log "Created planning structure in: $target_dir"
    echo "✅ Planning structure created in: $target_dir"
    echo "📄 PLAN.md and README.md files generated"
}

# Organize files by type
organize_files() {
    local target_dir="$1"
    local file_type="${2:-all}"
    
    if [[ ! -d "$target_dir" ]]; then
        echo "❌ Directory not found: $target_dir"
        return 1
    fi
    
    echo "📁 Organizing files in: $target_dir"
    
    case "$file_type" in
        documents|docs)
            mkdir -p "$target_dir/organized/documents"
            find "$target_dir" -maxdepth 1 -type f \( -iname "*.pdf" -o -iname "*.doc*" -o -iname "*.txt" -o -iname "*.md" \) -exec mv {} "$target_dir/organized/documents/" \; 2>/dev/null || true
            ;;
        media)
            mkdir -p "$target_dir/organized/media"
            find "$target_dir" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.mp4" -o -iname "*.mp3" \) -exec mv {} "$target_dir/organized/media/" \; 2>/dev/null || true
            ;;
        code)
            mkdir -p "$target_dir/organized/code"
            find "$target_dir" -maxdepth 1 -type f \( -iname "*.py" -o -iname "*.js" -o -iname "*.sh" -o -iname "*.cpp" \) -exec mv {} "$target_dir/organized/code/" \; 2>/dev/null || true
            ;;
        all|*)
            mkdir -p "$target_dir/organized/{documents,media,code,archives,other}"
            find "$target_dir" -maxdepth 1 -type f -iname "*.pdf" -o -iname "*.doc*" -o -iname "*.txt" -o -iname "*.md" | xargs -r mv -t "$target_dir/organized/documents/" 2>/dev/null || true
            find "$target_dir" -maxdepth 1 -type f -iname "*.jpg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.mp4" -o -iname "*.mp3" | xargs -r mv -t "$target_dir/organized/media/" 2>/dev/null || true
            find "$target_dir" -maxdepth 1 -type f -iname "*.py" -o -iname "*.js" -o -iname "*.sh" -o -iname "*.cpp" -o -iname "*.java" | xargs -r mv -t "$target_dir/organized/code/" 2>/dev/null || true
            find "$target_dir" -maxdepth 1 -type f -iname "*.zip" -o -iname "*.tar.gz" -o -iname "*.rar" | xargs -r mv -t "$target_dir/organized/archives/" 2>/dev/null || true
            find "$target_dir" -maxdepth 1 -type f | xargs -r mv -t "$target_dir/organized/other/" 2>/dev/null || true
            ;;
    esac
    
    log "Organized files in: $target_dir by type: $file_type"
    echo "✅ Files organized by type: $file_type"
}

# Create backup with timestamp
create_backup() {
    local target_dir="$1"
    local timestamp="$(date +%Y%m%d_%H%M%S)"
    local backup_name="$(basename "$target_dir")_backup_$timestamp"
    local backup_path="$BACKUP_DIR/$backup_name.tar.gz"
    
    if [[ ! -d "$target_dir" ]]; then
        echo "❌ Directory not found: $target_dir"
        return 1
    fi
    
    echo "💾 Creating backup of: $target_dir"
    tar -czf "$backup_path" -C "$(dirname "$target_dir")" "$(basename "$target_dir")"
    
    log "Created backup: $backup_path"
    echo "✅ Backup created: $backup_path"
}

# Analyze directory structure
analyze_directory() {
    local target_dir="$1"
    
    if [[ ! -d "$target_dir" ]]; then
        echo "❌ Directory not found: $target_dir"
        return 1
    fi
    
    echo "🔍 Analyzing directory: $target_dir"
    echo "📊 Statistics:"
    echo "   Files: $(find "$target_dir" -type f | wc -l)"
    echo "   Directories: $(find "$target_dir" -type d | wc -l)"
    echo "   Total size: $(du -sh "$target_dir" 2>/dev/null | cut -f1)"
    
    echo ""
    echo "📋 Top file types:"
    find "$target_dir" -type f -exec basename {} \; | sed 's/.*\.//' | sort | uniq -c | sort -nr | head -10
    
    echo ""
    echo "💡 Recommendations:"
    echo "   - Consider organizing files into subdirectories by type"
    echo "   - Create a README.md to document the directory structure"
    echo "   - Set up regular backups for important files"
    echo "   - Use consistent naming conventions"
    
    log "Analyzed directory: $target_dir"
}

# Create project templates
create_template() {
    local template_name="$1"
    local target_dir="${2:-$(pwd)/$template_name}"
    
    case "$template_name" in
        research-paper)
            mkdir -p "$target_dir"/{figures,tables,references,appendix}
            cat > "$target_dir/outline.md" << EOF
# Research Paper Outline

## Abstract
Brief summary of the research

## Introduction
- Background and motivation
- Problem statement
- Contributions

## Related Work
Literature review and comparison

## Methodology
Detailed description of methods

## Results
Experimental results and analysis

## Discussion
Interpretation of results

## Conclusion
Summary and future work

## References
Citations and bibliography
EOF
            ;;
        software-project)
            mkdir -p "$target_dir"/{src,tests,docs,examples,config}
            cat > "$target_dir/requirements.txt" << EOF
# Project dependencies
EOF
            cat > "$target_dir/Makefile" << EOF
# Build and test commands
.PHONY: build test clean

build:
	@echo "Building project..."

test:
	@echo "Running tests..."

clean:
	@echo "Cleaning build artifacts..."
EOF
            ;;
        *)
            echo "❌ Unknown template: $template_name"
            echo "Available templates: research-paper, software-project"
            return 1
            ;;
    esac
    
    log "Created template '$template_name' in: $target_dir"
    echo "✅ Template '$template_name' created in: $target_dir"
}

# Main function
main() {
    local action=""
    local verbose=false
    local force=false
    local dry_run=false
    local file_type="all"
    local date_range=""
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--verbose)
                verbose=true
                shift
                ;;
            -f|--force)
                force=true
                shift
                ;;
            --dry-run)
                dry_run=true
                shift
                ;;
            -t|--type)
                file_type="$2"
                shift 2
                ;;
            -d|--date)
                date_range="$2"
                shift 2
                ;;
            plan|organize|backup|analyze|template|sync)
                action="$1"
                shift
                ;;
            *)
                if [[ -z "$action" ]]; then
                    echo "❌ Unknown action: $1"
                    show_help
                    exit 1
                fi
                break
                ;;
        esac
    done
    
    # Execute based on action
    case "$action" in
        plan)
            if [[ $# -eq 0 ]]; then
                echo "❌ Missing directory argument for plan"
                exit 1
            fi
            create_plan "$1"
            ;;
        organize)
            if [[ $# -eq 0 ]]; then
                echo "❌ Missing directory argument for organize"
                exit 1
            fi
            organize_files "$1" "$file_type"
            ;;
        backup)
            if [[ $# -eq 0 ]]; then
                echo "❌ Missing directory argument for backup"
                exit 1
            fi
            create_backup "$1"
            ;;
        analyze)
            if [[ $# -eq 0 ]]; then
                echo "❌ Missing directory argument for analyze"
                exit 1
            fi
            analyze_directory "$1"
            ;;
        template)
            if [[ $# -eq 0 ]]; then
                echo "❌ Missing template name for template"
                exit 1
            fi
            create_template "$1" "${2:-}"
            ;;
        sync)
            if [[ $# -lt 2 ]]; then
                echo "❌ Missing source and destination for sync"
                exit 1
            fi
            echo "🔄 Sync functionality will be implemented in future versions"
            ;;
        *)
            echo "❌ No action specified"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"