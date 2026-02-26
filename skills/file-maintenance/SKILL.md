# File Maintenance Skill

## Purpose
Automatically reviews, cleans, and optimizes files in the workspace directory. Detects and handles problematic files while maintaining system integrity.

## Capabilities
- **Security Review**: Identifies potentially malicious or dangerous files
- **Quality Assurance**: Detects logical errors, syntax issues, and inconsistencies  
- **Deduplication**: Finds and consolidates redundant or duplicate files
- **Content Optimization**: Upgrades and refines file content for better organization
- **Safe Operations**: Never modifies files critical to OpenClaw's operation without explicit confirmation

## Execution Schedule
- Runs every 24 hours with flexible timing
- Automatically yields to higher-priority tasks
- Can be manually triggered or paused when needed

## Safety Protocols
- **Read-only by default**: Only reports issues without making changes
- **Confirmation required**: Any destructive operations (deletions/modifications) require explicit user approval
- **Backup first**: Creates backups before modifying important files
- **Exclusion list**: Respects protected files and directories

## Protected Files (Never Modified Automatically)
- AGENTS.md, SOUL.md, USER.md, MEMORY.md
- Identity and configuration files
- Active session files
- System-critical OpenClaw files

## Usage
```
/file-maintenance run          # Manual execution
/file-maintenance status       # Check last run status  
/file-maintenance pause        # Temporarily disable scheduled runs
/file-maintenance resume       # Re-enable scheduled runs
```

## Configuration
Customize behavior via `skills/file-maintenance/config.json`:
```json
{
  "autoFix": false,
  "excludedPaths": [],
  "priority": "low",
  "scheduleHours": 24
}
```