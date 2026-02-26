---
name: github-sync-auto
description: Automated GitHub synchronization for OpenClaw workspace with 20-hour intervals. Automatically commits and pushes all workspace changes to configured GitHub repository, ensuring continuous backup of memory files, configurations, and workspace data. Use when you need reliable, scheduled backup of your OpenClaw environment to GitHub.
---

# GitHub Auto-Sync Skill

This skill provides automated, scheduled synchronization of your OpenClaw workspace to GitHub every 20 hours, ensuring your data is continuously backed up.

## Key Features

### 🔄 Automatic Synchronization
- **20-hour intervals**: Syncs every 20 hours automatically
- **Full workspace backup**: Includes memory files, configurations, and all workspace data
- **Smart commit messages**: Auto-generated descriptive commit messages
- **Conflict resolution**: Handles merge conflicts gracefully
- **Error recovery**: Continues after temporary failures

### 🔒 Safety & Reliability
- **Dry-run capability**: Test sync without making changes
- **Selective file handling**: Respects .gitignore patterns
- **Backup verification**: Confirms successful push to remote
- **Activity logging**: Detailed logs of all sync operations
- **Resource monitoring**: Prevents excessive resource usage

### ⚙️ Configuration Options
- **Custom intervals**: Override default 20-hour schedule
- **Repository selection**: Support for multiple GitHub repos
- **Branch management**: Specify target branch for sync
- **File filtering**: Include/exclude specific file patterns
- **Notification settings**: Alert on sync success/failure

## Quick Start

### Basic Auto-Sync Setup
```bash
github-sync setup --interval 20h
```
Configures automatic 20-hour sync with your current GitHub repository.

### Manual Sync Trigger
```bash
github-sync run --now
```
Immediately performs a sync operation.

### Check Sync Status
```bash
github-sync status
```
Shows last sync time, next scheduled sync, and configuration.

## Usage Guide

### 1. Initial Setup

#### Configure Auto-Sync (20-hour default)
```bash
github-sync setup
```
This command:
- Verifies your GitHub repository is properly configured
- Sets up cron job for 20-hour intervals
- Creates necessary configuration files
- Performs initial sync test

#### Custom Interval Setup
```bash
github-sync setup --interval 12h
```
Sets up sync with custom interval (supports h/m/s suffixes).

### 2. Running Sync Operations

#### Immediate Sync
```bash
github-sync run --now
```
Performs immediate sync regardless of schedule.

#### Scheduled Sync (automatic)
The system automatically runs every 20 hours based on your configuration.

#### Dry Run Test
```bash
github-sync run --dry-run
```
Tests the sync process without making actual changes.

### 3. Monitoring & Management

#### View Sync History
```bash
github-sync history --limit 10
```
Shows recent sync operations and their results.

#### Check Current Status
```bash
github-sync status
```
Displays current configuration and timing information.

#### Stop Auto-Sync
```bash
github-sync stop
```
Disables automatic synchronization.

#### Resume Auto-Sync
```bash
github-sync start
```
Re-enables automatic synchronization.

## Configuration Files

Configuration is stored in `~/.openclaw/workspace/.github-sync/`:

- `config.json` - Main configuration (interval, repository, branch)
- `sync.log` - Activity log of all sync operations
- `last-sync.txt` - Timestamp of last successful sync
- `cron-setup.sh` - Cron job configuration script

## Safety & Best Practices

### ✅ Recommended Practices
- **Verify initial setup**: Always check that your first sync works correctly
- **Monitor logs**: Regularly review sync logs for any issues
- **Test recovery**: Periodically verify you can restore from GitHub
- **Keep SSH keys secure**: Ensure GitHub SSH authentication is properly configured
- **Respect rate limits**: The 20-hour interval helps avoid GitHub API limits

### ⚠️ Important Considerations
- **Internet connectivity**: Sync requires working internet connection
- **GitHub permissions**: Ensure your SSH key has write access to the repository
- **Large file handling**: Very large files may cause sync delays
- **Merge conflicts**: Manual intervention may be needed for complex conflicts
- **Workspace integrity**: Only sync clean, working workspace states

## When to Use This Skill

Use this GitHub auto-sync skill when you need:
- **Continuous backup** of your OpenClaw workspace and memory files
- **Automated version control** for your AI assistant's knowledge base
- **Disaster recovery capability** through GitHub as backup storage
- **Scheduled synchronization** without manual intervention
- **Reliable data persistence** across system restarts or failures
- **Collaborative backup strategy** using GitHub's infrastructure

## Scripts Overview

- `scripts/github-sync-core.sh` - Main synchronization logic
- `scripts/cron-manager.sh` - Cron job setup and management
- `scripts/git-operations.sh` - Git commit/push operations with error handling
- `scripts/config-manager.sh` - Configuration file management
- `scripts/log-handler.sh` - Logging and monitoring functionality
- `scripts/conflict-resolver.sh` - Merge conflict handling
- `scripts/health-check.sh` - Pre-sync validation and health checks