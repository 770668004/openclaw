---
name: skill-evolution-manager
description: "智能技能进化管理系统：自动分类、审计和升级OpenClaw技能，按功能分组（安全与审计、文件管理、通信协作等），执行严格的代码审计，支持24小时周期性自我升级，优先级低于当前任务。"
metadata:
  {
    "openclaw": { "emoji": "🚀", "requires": { "bins": ["git", "curl"] } }
  }
---

# 技能进化管理系统

## 功能概述

这是一个智能的技能管理系统，能够：
- **自动分类**：将所有技能按功能分为5-8个清晰的类别
- **严格审计**：升级前进行完整的代码和逻辑审计
- **智能进化**：基于新知识和最佳实践自动优化技能
- **周期执行**：24小时为周期进行自我升级（优先级低于当前任务）

## 功能分类体系

系统将63个技能分为以下8个功能类别：

### 1. 安全与审计 🔒
- healthcheck：主机安全加固和风险配置
- backup：文件和系统配置的备份恢复
- model-usage：模型使用监控和优化

### 2. 文件与数据管理 📁
- backup：综合备份功能
- gifgrep：GIF内容搜索
- xurl：URL管理和处理

### 3. 通信与协作 💬
- bluebubbles：iOS消息集成
- imsg：iMessage控制
- voice-call：语音通话功能
- blucli：蓝牙设备控制

### 4. 开发与编码 🧩
- coding-agent：委托编码任务给专业代理
- github：GitHub操作和CI/CD管理
- tmux：终端会话管理

### 5. 系统与设备控制 🖥️
- camsnap：摄像头快照
- peekaboo：隐私保护工具
- things-mac：Mac任务管理
- openhue：Philips Hue灯光控制
- sonoscli：Sonos音响控制

### 6. 天气与环境 🌤️
- weather：天气预报和当前天气
- songsee：音乐识别和推荐

### 7. 密码与身份管理 🔑
- 1password：1Password密码管理集成
- apple-reminders：Apple提醒事项

### 8. 工具与实用程序 🛠️
- notion：Notion工作区集成
- skill-creator：技能创建和更新
- find-skills：技能发现和安装
- concise-output：优化输出格式
- context-restore：上下文恢复

## 核心工作流程

### 阶段1：技能发现与分类
```
1. 扫描三个目录中的所有技能：
   - 系统技能：~/.npm-global/lib/node_modules/openclaw/skills/
   - 工作区技能：~/.openclaw/workspace/skills/
   - 代理技能：~/.agents/skills/
2. 读取每个SKILL.md文件的name和description字段
3. 基于功能描述自动分配到8个预定义类别
4. 生成技能分类报告
```

### 阶段2：审计与评估
```
1. 对每个技能进行代码审计：
   - 检查安全漏洞
   - 验证功能逻辑
   - 评估性能瓶颈
   - 确认依赖完整性
2. 生成审计报告，标记需要改进的技能
3. 识别可以合并或优化的重复功能
```

### 阶段3：智能升级
```
1. 基于审计结果制定升级计划
2. 应用最新的安全最佳实践
3. 优化性能和用户体验
4. 更新技能描述和元数据
5. 保持向后兼容性
```

### 阶段4：部署与验证
```
1. 在隔离环境中测试升级后的技能
2. 验证所有功能正常工作
3. 更新文档和示例
4. 提交更改并通知用户
```

## 执行策略

### 24小时周期性执行
- **触发条件**：每24小时自动检查一次
- **优先级规则**：始终低于当前正在执行的任务
- **资源限制**：在系统空闲时执行（CPU使用率<50%）
- **中断恢复**：支持任务中断后恢复执行

### 用户控制选项
用户可以通过以下命令控制进化过程：

```bash
# 查看当前技能分类
skill-evolution-manager list --categories

# 手动触发技能审计
skill-evolution-manager audit --all

# 查看升级计划
skill-evolution-manager plan

# 执行升级（需要确认）
skill-evolution-manager upgrade --confirm

# 设置自动升级策略
skill-evolution-manager config --auto-upgrade true --schedule "0 2 * * *"
```

## 安全保障

### 升级前必须的确认步骤
1. **完整备份**：升级前自动备份所有技能文件
2. **沙箱测试**：在隔离环境中验证升级效果
3. **回滚计划**：准备完整的回滚方案
4. **用户确认**：关键升级需要用户明确同意

### 审计标准
- **代码质量**：遵循OpenClaw编码规范
- **安全性**：无敏感信息泄露风险
- **性能**：响应时间在可接受范围内
- **兼容性**：与现有系统完全兼容

## 智能特性

### 自我学习能力
- 分析用户使用模式，优化常用技能
- 学习新的最佳实践，应用到技能升级中
- 基于社区反馈改进技能功能

### 上下文感知
- 根据当前任务调整升级优先级
- 在用户活跃时段避免打扰性操作
- 根据系统资源状况动态调整执行策略

## 使用示例

### 查看技能分类
```bash
skill-evolution-manager list --category "安全与审计"
```

### 执行完整进化周期
```bash
skill-evolution-manager evolve --full-cycle
```

### 监控进化状态
```bash
skill-evolution-manager status
```

## 注意事项

- **权限要求**：需要对技能目录的读写权限
- **网络依赖**：部分功能需要网络连接获取最新信息
- **存储空间**：升级过程需要额外的临时存储空间
- **时间消耗**：完整进化周期可能需要30-60分钟

## 版本演进

此技能本身也会参与24小时进化周期，在每次执行时：
1. 检查是否有新的管理策略可用
2. 学习其他技能的最佳实践
3. 优化自身的分类算法和审计逻辑
4. 改进用户体验和错误处理