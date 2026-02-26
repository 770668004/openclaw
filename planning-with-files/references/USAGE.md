# Planning with Files - 使用指南

## 功能概述
这个技能提供强大的文件规划和管理功能，帮助你：
- 分析目录结构和文件组织
- 创建项目规划和文件清单
- 自动化文件分类和整理
- 生成文件报告和统计信息
- 批量重命名和移动文件

## 主要命令

### 1. 文件分析和规划
```bash
# 分析目录结构并生成规划建议
planning-with-files analyze /path/to/directory

# 生成详细的文件报告
planning-with-files report /path/to/directory

# 创建项目文件清单
planning-with-files inventory /path/to/project
```

### 2. 文件组织和整理
```bash
# 按类型自动分类文件
planning-with-files organize /path/to/directory --by-type

# 按日期分类文件
planning-with-files organize /path/to/directory --by-date

# 按大小分类文件
planning-with-files organize /path/to/directory --by-size
```

### 3. 批量操作
```bash
# 批量重命名文件（支持模式匹配）
planning-with-files rename /path/to/directory --pattern "IMG_*.jpg" --format "photo-{date}-{counter}.jpg"

# 批量移动文件到目标目录
planning-with-files move /source/directory /target/directory --filter "*.log"
```

### 4. 规划模板
```bash
# 创建项目目录模板
planning-with-files template project-name --type web-app

# 创建文档结构模板
planning-with-files template docs-project --type documentation
```

## 安全特性
- 所有破坏性操作都会先显示预览
- 支持 `--dry-run` 参数进行模拟运行
- 自动创建备份点（可选）
- 详细的操作日志记录

## 配置选项
配置文件位于 `~/.config/planning-with-files/config.json`，支持自定义：
- 默认备份目录
- 文件类型映射规则
- 命名约定模板
- 排除文件模式

## 示例工作流

### 项目启动规划
```bash
# 1. 分析现有文件结构
planning-with-files analyze ~/my-project

# 2. 创建标准化的项目模板
planning-with-files template my-project --type full-stack

# 3. 组织现有文件到新结构
planning-with-files organize ~/my-project --by-type
```

### 文档整理
```bash
# 1. 生成文档清单
planning-with-files inventory ~/documents --output docs-inventory.json

# 2. 按年份和月份分类
planning-with-files organize ~/documents --by-date --format "YYYY/MM"

# 3. 生成最终报告
planning-with-files report ~/documents --format markdown
```

## 注意事项
- 在执行批量操作前，建议先使用 `--dry-run` 参数预览结果
- 大型目录操作可能需要较长时间，请耐心等待
- 建议定期备份重要数据
- 如遇到权限问题，请确保对目标目录有适当的读写权限