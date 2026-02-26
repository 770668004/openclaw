# MEMORY.md - Memory System Overview

> **This is your main memory index** - All actual memory content is now organized in specialized modules

## 🧠 Multi-Module Memory Architecture

### 🔑 CORE_MEMORY.md (Permanent)
- **Purpose**: Core instructions, permanent commands, behavioral guidelines
- **Retention**: Never auto-deleted, requires explicit confirmation for changes
- **Location**: `/home/kousoyu/.openclaw/workspace/CORE_MEMORY.md`

### 📝 WORKING_MEMORY.md (Temporary)  
- **Purpose**: Project notes, temporary records, working context
- **Retention**: Auto-cleanable after 30 days, safe to delete
- **Location**: `/home/kousoyu/.openclaw/workspace/WORKING_MEMORY.md`

### 💬 SESSION_HISTORY/ (Archival)
- **Purpose**: Complete interaction history, all commands and conversations
- **Retention**: Requires user confirmation before any cleanup
- **Location**: `/home/kousoyu/.openclaw/workspace/SESSION_HISTORY/`

## 🔄 Memory Management Workflow

1. **Core Instructions** → Always store in `CORE_MEMORY.md`
2. **Working Context** → Store in `WORKING_MEMORY.md` 
3. **Full History** → Automatically logged in `SESSION_HISTORY/YYYY-MM-DD.md`
4. **Backup** → All files automatically synced to GitHub via `memory-git-sync`

## 🛡️ Safety Features

- **No accidental deletion**: Core memory requires explicit confirmation
- **Automatic backup**: All changes pushed to GitHub repository
- **Clear separation**: Temporary vs permanent data clearly distinguished
- **Audit trail**: All cleanup operations logged in `SESSION_HISTORY/cleanup_log.md`

## 📋 Current Status

- ✅ Multi-module system created and configured
- ✅ GitHub remote sync enabled (770668004/openclaw)
- ✅ Initial session history recorded (2026-02-25)
- ✅ All files backed up to remote repository

---

*Last updated: 2026-02-27 01:08*
*Memory restored from GitHub repository github.com/770668004/openclaw*