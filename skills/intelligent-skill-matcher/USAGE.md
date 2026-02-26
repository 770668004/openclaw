# 智能技能匹配器使用指南

## 功能概述

智能技能匹配器能够分析用户输入的中文命令，并自动匹配最适合的现有技能，提高任务处理效率和智能化水平。

## 使用方法

### 1. 命令行使用

```bash
# 分析单个命令
python scripts/analyze_command.py "今天北京天气怎么样？"

# 运行完整测试
python scripts/test_skill_matcher.py
```

### 2. 集成到OpenClaw

在OpenClaw中，可以通过以下方式调用：

```python
from skills.intelligent_skill_matcher.scripts.analyze_command import analyze_user_command

result = analyze_user_command("用户输入的命令")
best_match = result['matches'][0] if result['matches'] else None
```

## 匹配示例

| 用户命令 | 匹配技能 | 置信度 | 推理 |
|---------|---------|--------|------|
| "今天北京天气怎么样？" | weather | 2.0/10 | 匹配特殊关键词: 天气 |
| "帮我创建一个新的GitHub issue" | github | 10.0/10 | 包含技能名称: github; 匹配关键词: github; 匹配特殊关键词: github, git |
| "备份我的重要文件" | backup | 2.0/10 | 匹配特殊关键词: 备份 |
| "检查系统安全状态" | healthcheck | 4.0/10 | 匹配特殊关键词: 安全, 检查 |
| "播放音乐到我的Sonos音箱" | sonoscli | 9.33/10 | 匹配关键词: sonos; 匹配特殊关键词: sonos, 音箱 |

## 配置说明

### 特殊关键词配置

在 `analyze_command.py` 中的 `special_keywords` 字典定义了每个技能的特殊关键词，包括中英文关键词。

### 置信度阈值

- **高置信度 (≥7.0)**：可以直接执行匹配的技能
- **中等置信度 (4.0-6.9)**：建议用户确认后再执行
- **低置信度 (<4.0)**：需要人工确认或考虑其他选项

## 扩展开发

### 添加新技能支持

1. 在 `special_keywords` 字典中添加新技能的关键词
2. 确保新技能的SKILL.md文件包含足够的描述信息
3. 测试匹配效果并调整关键词权重

### 改进匹配算法

当前使用基于规则的匹配算法，未来可以考虑：
- 集成中文分词库（如jieba）提高关键词提取准确性
- 添加语义相似度计算
- 支持模糊匹配和同义词扩展

## 注意事项

- 技能匹配基于现有的技能描述和关键词
- 对于复杂的多技能组合任务，可能需要人工干预
- 置信度分数仅供参考，实际使用时应结合上下文判断