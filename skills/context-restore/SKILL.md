# Context Restore Skill

## Purpose
This skill automatically restores context and resumes interrupted tasks after system events like:
- Task completion
- Task interruption
- System freezes or unresponsiveness
- Session resets
- Model switches
- Network disconnections

## How It Works
1. Detects session restart or interruption events
2. Reads essential context files to rebuild understanding of current state
3. Identifies any in-progress tasks from memory logs
4. Offers to resume or complete pending tasks

## Files Read During Restoration
- `SOUL.md` - Assistant identity and behavior guidelines
- `USER.md` - User preferences and settings
- `MEMORY.md` - Long-term memory and important context
- `WORKFLOW_AUTO.md` - Automated workflow configurations
- Recent daily memory files (`memory/YYYY-MM-DD.md`)

## Implementation Details
The skill hooks into the session initialization process to ensure context is always restored before proceeding with new requests. It maintains a task registry in memory files to track ongoing work.

## Usage
This skill runs automatically during session startup and doesn't require explicit invocation. It ensures continuity of experience across interruptions.