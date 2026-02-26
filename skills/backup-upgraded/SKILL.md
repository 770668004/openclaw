---
name: backup
description: Advanced backup and restore system with intelligent scheduling, multiple storage backends, encryption, and AI-powered retention policies. Supports cloud storage, local backups, incremental snapshots, and automated recovery testing.
---

# Advanced Backup System

This enhanced backup skill provides enterprise-grade data protection with intelligent features, multiple storage options, and automated management.

## Key Upgrades

### 🚀 Enhanced Features
- **Multi-cloud support**: AWS S3, Google Cloud Storage, Azure Blob Storage
- **Advanced encryption**: AES-256 encryption with key management
- **Intelligent scheduling**: AI-powered backup timing based on usage patterns
- **Automated recovery testing**: Periodic restore verification
- **Smart retention policies**: Automatic cleanup based on importance and age
- **Differential backups**: More efficient than traditional incremental
- **Bandwidth optimization**: Throttling and compression for network backups

### 🔒 Security Enhancements
- **Zero-knowledge encryption**: Only you have the decryption keys
- **Secure key storage**: Integration with system keychains
- **Audit logging**: Complete backup activity tracking
- **Tamper detection**: Verify backup integrity automatically

### 📊 Management Dashboard
- **Real-time monitoring**: Backup status and progress
- **Storage analytics**: Usage trends and predictions
- **Alert system**: Notifications for failures or issues
- **Recovery point objectives**: Track backup effectiveness

## Quick Start

### Basic Backup Commands

- **Backup home directory**: `backup home`
- **Backup with encryption**: `backup encrypt home`  
- **Cloud backup**: `backup cloud aws /path/to/data`
- **List all backups**: `backup list --all`
- **Restore with verification**: `backup restore --verify <backup-name>`

### Advanced Operations

- **Test restore**: `backup test-restore <backup-name>`
- **Set retention policy**: `backup retention 30d /path/to/data`
- **Schedule intelligent backup**: `backup schedule smart /path/to/data`
- **Export backup catalog**: `backup export-catalog`

## Usage Guide

### 1. Creating Backups

#### Smart Home Backup
```bash
backup home --smart
```
Creates an optimized backup of your home directory with intelligent file selection and compression.

#### Encrypted Cloud Backup
```bash
backup cloud --encrypt --compress aws://my-bucket/backups /important/data
```
Backs up to AWS S3 with encryption and compression.

#### Differential Backup
```bash
backup diff --base "backup-2026-02-25" /project/directory
```
Creates a differential backup based on a previous full backup.

### 2. Restoring & Recovery

#### Verified Restore
```bash
backup restore --verify "backup-2026-02-26-smart"
```
Restores and automatically verifies file integrity.

#### Point-in-Time Recovery
```bash
backup restore --timestamp "2026-02-25T14:30:00" /project
```
Recovers files as they existed at a specific time.

#### Emergency Recovery
```bash
backup emergency-restore /critical/system
```
Prioritizes speed over verification for critical situations.

### 3. Backup Intelligence

#### Automated Testing
```bash
backup test-schedule weekly
```
Sets up automatic restore testing on a weekly basis.

#### Smart Retention
```bash
backup retention --smart /project
```
Applies AI-driven retention based on file importance and change frequency.

#### Usage Analytics
```bash
backup analytics --report monthly
```
Generates monthly backup effectiveness reports.

## Configuration

Enhanced configuration in `~/.backup-config/`:
- `config.json` - Main configuration with cloud credentials
- `encryption-keys/` - Secure key storage
- `policies/` - Retention and scheduling policies  
- `destinations/` - Multi-cloud destination configurations
- `analytics/` - Usage tracking and reporting settings

## Safety & Best Practices

### ✅ Recommended Practices
- **Enable automated testing** to ensure backup reliability
- **Use multi-location storage** for critical data
- **Implement smart retention** to optimize storage costs
- **Regular key rotation** for enhanced security
- **Monitor backup health** through the dashboard

### ⚠️ Critical Considerations
- **Test emergency procedures** before relying on them
- **Secure your encryption keys** - loss means permanent data loss
- **Verify cloud permissions** before enabling cloud backups
- **Monitor storage quotas** to prevent backup failures

## When to Use This Skill

Use this enhanced backup skill when you need:
- **Enterprise-grade data protection** for critical systems
- **Multi-cloud backup strategies** with redundancy
- **Compliance-ready backup solutions** with audit trails
- **Automated backup intelligence** that adapts to your needs
- **Secure, encrypted backups** for sensitive information
- **Professional backup management** with monitoring and alerts

## Scripts Overview

- `scripts/backup-core.sh` - Enhanced core backup functionality
- `scripts/cloud-integration.sh` - Multi-cloud storage support
- `scripts/encryption-manager.sh` - Secure key management
- `scripts/intelligence-engine.sh` - AI-powered scheduling and retention
- `scripts/monitoring-dashboard.sh` - Real-time backup monitoring
- `scripts/recovery-tester.sh` - Automated restore verification
- `scripts/analytics-reporter.sh` - Usage analytics and reporting