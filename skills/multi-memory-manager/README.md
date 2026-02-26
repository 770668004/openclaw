# Multi-Memory Manager - 多记忆管理系统

## 🧠 概述
这是一个高级记忆管理系统，将记忆分为5个专门的文件类型，每个都有特定的用途、重要性和生命周期管理策略。

## 📁 记忆文件分类

### 1. **CORE_MEMORY.md** (核心记忆)
- **用途**: 保存最重要的命令、主要事情、永久性指令
- **特点**: 永久保存，永不自动删除
- **内容**: 用户明确要求记住的核心指令、行为准则、重要偏好
- **读取优先级**: 最高 - 启动时立即加载

### 2. **WORKING_CONTEXT.md** (工作上下文)
- **用途**: 临时工作上下文、当前项目状态  
- **特点**: 3天周期自动清理
- **内容**: 当前任务上下文、临时变量、正在进行的工作
- **读取优先级**: 高 - 会话开始时加载

### 3. **LOGIC_HISTORY.md** (逻辑历史)
- **用途**: 聊天逻辑摘要、重点优化记录
- **特点**: 长期保存，定期优化整理
- **内容**: 对话模式、用户偏好演变、重要决策逻辑
- **读取优先级**: 中 - 需要时加载

### 4. **OPERATION_LOG.md** (操作日志)
- **用途**: 代码修改、JSON配置变更等操作记录
- **特点**: 重要记录永久保存，普通记录1天后删除
- **内容**: 系统操作、文件修改、配置变更
- **读取优先级**: 低 - 审计时加载

### 5. **TASK_RECOVERY.md** (任务恢复)
- **用途**: 正在执行的任务状态，用于网络中断恢复
- **特点**: 任务完成后自动删除
- **内容**: 当前任务状态、进度、参数
- **读取优先级**: 最高 - 启动时立即检查

## 🚀 使用方法

### 初始化记忆系统
```bash
memory-init
```

### 保存核心指令
```bash
memory-core "记住：总是先确认再执行敏感操作"
```

### 保存工作上下文
```bash
memory-context "当前项目：多记忆管理系统开发"
memory-context --priority high "重要任务：完成记忆系统"
```

### 保存逻辑历史
```bash
memory-logic --topic "记忆管理" --importance high "用户要求将记忆分为多个文件类型"
```

### 记录操作日志
```bash
memory-log "创建了multi-memory-manager技能目录"
memory-log --importance critical --file-path "/path/to/file" "关键配置修改"
```

### 管理任务状态
```bash
# 保存新任务
memory-task "正在开发核心记忆模块" --priority high

# 完成任务
memory-task --complete --task-id TASK_ID
```

### 清理和维护
```bash
memory-cleanup    # 清理过期记忆
memory-summary    # 查看记忆摘要
memory-startup    # 启动时加载关键记忆
```

## ⚡ 自动化特性

- **启动时自动加载**: CORE_MEMORY.md 和 TASK_RECOVERY.md 在每次启动时自动读取
- **智能提取**: 自动识别用户语句中的核心指令并建议保存到核心记忆
- **生命周期管理**: 自动清理过期的上下文和日志文件
- **恢复机制**: 网络中断后自动从TASK_RECOVERY.md恢复任务
- **高效读取**: 核心记忆文件优化为快速加载格式

## 🛡️ 安全特性

- **核心记忆保护**: 核心记忆文件的修改需要用户确认
- **备份机制**: 所有记忆文件自动备份到GitHub
- **审计追踪**: 所有记忆操作都记录在OPERATION_LOG.md中

## 🔧 技术架构

- **模块化设计**: 每个记忆类型都有独立的Python模块
- **命令行接口**: 提供简洁的bash命令接口
- **JSON兼容**: 支持结构化数据存储
- **跨平台**: 基于Python标准库，支持Linux/macOS/Windows

## 📝 安装和集成

将此技能目录放置在 `~/.openclaw/workspace/skills/multi-memory-manager/` 目录下。

将命令行脚本添加到PATH:
```bash
export PATH="$PATH:/home/kousoyu/.openclaw/workspace/skills/multi-memory-manager"
```

或者在OpenClaw启动脚本中添加:
```bash
# 在 ~/.openclaw/startup.sh 中添加
source /home/kousoyu/.openclaw/workspace/skills/multi-memory-manager/memory-startup
```

## 💡 最佳实践

1. **核心指令要精简**: 只保存真正重要的长期指令
2. **上下文要及时清理**: 定期运行 `memory-cleanup`
3. **任务要及时完成**: 避免TASK_RECOVERY.md积累过多未完成任务
4. **重要操作要记录**: 使用 `memory-log` 记录关键系统变更
5. **定期备份**: 确保所有记忆文件都同步到远程仓库

---
*Created: 2026-02-26*
*Author: Kousoyu*
*License: MIT*