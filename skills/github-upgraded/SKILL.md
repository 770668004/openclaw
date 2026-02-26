---
name: github-upgraded
description: "Enhanced GitHub operations with advanced PR management, automated code review, intelligent issue triage, and integrated CI monitoring. Includes AI-powered suggestions, batch operations, and cross-repository workflows."
metadata:
  {
    "openclaw":
      {
        "emoji": "🐙",
        "requires": { "bins": ["gh"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (brew)",
            },
            {
              "id": "apt",
              "kind": "apt",
              "package": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (apt)",
            },
          ],
      },
  }
---

# GitHub Enhanced Skill

Advanced GitHub operations with AI-powered insights, automated workflows, and comprehensive repository management.

## Enhanced Features

✅ **NEW Capabilities:**

- **AI-Powered Code Review**: Automatic code quality analysis and security vulnerability detection
- **Smart Issue Triage**: Intelligent issue categorization and priority assignment
- **Batch Operations**: Multi-repository issue/PR management
- **Cross-Repository Workflows**: Unified view across multiple repositories
- **Automated PR Summaries**: AI-generated PR descriptions and changelog entries
- **CI/CD Pipeline Monitoring**: Real-time build status and performance analytics
- **Dependency Management**: Automated dependency updates and security alerts
- **Team Collaboration Tools**: Enhanced team member tracking and workload balancing

## When to Use

✅ **USE this skill when:**

- Need comprehensive repository health assessment
- Managing multiple repositories simultaneously
- Requiring AI-assisted code review and quality analysis
- Automating repetitive GitHub workflows
- Monitoring CI/CD pipeline performance across projects
- Performing bulk operations on issues or PRs
- Setting up automated dependency management
- Analyzing team collaboration patterns and bottlenecks

## Advanced Commands

### AI-Powered Code Review

```bash
# Comprehensive code review with AI analysis
gh enhanced review --pr 55 --repo owner/repo --security --performance --style

# Generate automated PR description
gh enhanced pr-describe --pr 55 --repo owner/repo --changelog

# Security vulnerability scan
gh enhanced security-scan --repo owner/repo --branch feature-branch
```

### Smart Issue Management

```bash
# Auto-triage and categorize issues
gh enhanced triage --repo owner/repo --auto-assign --priority

# Bulk issue operations
gh enhanced issues batch --repos owner/repo1,owner/repo2 --state open --label "bug" --add-label "triaged"

# Generate issue templates based on repository patterns
gh enhanced templates generate --repo owner/repo --type bug,feature,question
```

### Cross-Repository Operations

```bash
# Unified PR dashboard across multiple repos
gh enhanced pr dashboard --repos owner/repo1,owner/repo2,owner/repo3

# Synchronized releases across repositories
gh enhanced release sync --repos owner/core,owner/web,owner/mobile --version v1.2.0

# Dependency version alignment
gh enhanced deps align --repos owner/frontend,owner/backend --package react
```

### CI/CD Enhanced Monitoring

```bash
# Build performance analytics
gh enhanced ci analytics --repo owner/repo --days 30 --metrics duration,success-rate

# Flaky test detection
gh enhanced tests flaky --repo owner/repo --threshold 0.8

# Automated build optimization suggestions
gh enhanced ci optimize --repo owner/repo --suggest
```

### Team Collaboration

```bash
# Team workload analysis
gh enhanced team workload --repo owner/repo --period week --members @all

# Code ownership mapping
gh enhanced ownership map --repo owner/repo --output json

# Review bottleneck identification
gh enhanced reviews bottlenecks --repo owner/repo --threshold 24h
```

## JSON Output & Integration

Enhanced JSON support with AI-generated insights:

```bash
# Get PR with AI analysis
gh enhanced pr view 55 --repo owner/repo --json title,body,ai-risk-score,ai-suggestions

# Repository health score
gh enhanced repo health --repo owner/repo --json score,metrics,recommendations

# Team performance metrics
gh enhanced team metrics --repo owner/repo --json members,throughput,quality
```

## Templates

### Comprehensive Repository Audit

```bash
# Full repository health check
REPO=owner/repo
echo "## Repository Health Report: $REPO"
gh enhanced repo health $REPO
gh enhanced security audit $REPO
gh enhanced team metrics $REPO
gh enhanced ci analytics $REPO --days 7
```

### Automated Release Preparation

```bash
# Prepare for release with automated checks
REPO=owner/repo VERSION=v1.2.0
echo "## Release Preparation: $VERSION"
gh enhanced pr list --repo $REPO --state merged --since $(date -d '7 days ago' +%Y-%m-%d)
gh enhanced security scan --repo $REPO --branch main
gh enhanced tests coverage --repo $REPO --threshold 80
gh enhanced deps outdated --repo $REPO
```

## Setup Requirements

```bash
# Enhanced setup (includes additional dependencies)
gh auth login
npm install -g @openclaw/github-enhanced  # Optional enhanced features

# Verify enhanced capabilities
gh enhanced --version
```

## Safety & Best Practices

- **Rate Limit Awareness**: Enhanced operations may consume more API quota
- **Backup Before Bulk Operations**: Always verify before large-scale changes
- **Gradual Rollout**: Test enhanced features on non-critical repositories first
- **Team Coordination**: Coordinate with team members before enabling automated workflows
- **Monitoring**: Set up alerts for automated operations that may require intervention

## Integration with Other Skills

- **coding-agent**: For detailed code analysis and refactoring suggestions
- **healthcheck**: For repository security and compliance auditing
- **backup**: For backing up critical repository configurations and workflows
- **skill-evolution-manager**: For continuous improvement of GitHub workflows