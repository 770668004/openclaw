# Planning with Files Skill

## Description
A comprehensive skill for planning, organizing, and managing files and directories. This skill provides tools for:
- Creating project structures and file hierarchies
- Generating planning documents and templates
- Organizing existing files into logical structures
- Tracking file changes and versions
- Creating file-based workflows and checklists

## Usage
Use when you need to:
1. Plan a new project structure
2. Organize existing files into categories
3. Create planning documents (roadmaps, checklists, timelines)
4. Set up file-based workflows
5. Generate templates for consistent file organization

## Commands
- `plan-project <project-name>` - Create a complete project structure with planning files
- `organize-files <source-dir> <target-dir>` - Organize files into categorized structure
- `create-planning-docs <type>` - Generate planning templates (roadmap, checklist, timeline, etc.)
- `file-workflow <workflow-type>` - Set up file-based workflow templates
- `plan-status` - Show current planning status and recommendations

## Examples
- `/planning-with-files plan-project my-website`
- `/planning-with-files create-planning-docs roadmap`
- `/planning-with-files organize-files ~/Downloads ~/Organized`

## Dependencies
- Standard Unix tools (mkdir, touch, cp, mv, find, etc.)
- Git (optional, for version tracking)

## Security
- Only operates within user's home directory by default
- Requires explicit confirmation for destructive operations
- Creates backup copies before major reorganizations