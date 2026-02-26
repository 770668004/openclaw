---
name: intelligent-skill-matcher
description: 智能分析用户命令文本，自动匹配和调用最适合的现有技能来高效执行任务。使用自然语言理解技术分析用户意图，从可用技能库中选择最佳匹配，并协调多个技能的组合使用以完成复杂任务。
version: 1.0.3
author: Kousoyu
license: MIT
---

# 智能技能匹配器 (Intelligent Skill Matcher)

## 功能概述

这个技能能够：
- 自动分析用户输入的自然语言命令
- 理解用户的真实意图和需求  
- 从现有的技能库中智能匹配最合适的技能
- 协调多个技能的组合使用来完成复杂任务
- 提供更快、更高效的任务执行体验

## 核心特性

### 🇨🇳 中文优先支持
- 专为中文命令优化的关键词匹配
- 支持中文语义理解和意图识别
- 包含丰富的中文技能触发词库

### 🔍 智能匹配算法
- **关键词匹配**：基于技能描述和特殊关键词
- **动态评分**：根据匹配质量给出0-10分置信度
- **多结果排序**：返回前3个最佳匹配选项
- **详细推理**：提供匹配原因说明

### 🤖 自动技能发现
- 扫描 `~/.openclaw/workspace/skills/` 目录
- 扫描 `~/.npm-global/lib/node_modules/openclaw/skills/` 目录  
- 自动解析SKILL.md中的YAML元数据
- 实时更新可用技能列表

## 使用场景

### 天气查询
- "今天北京天气怎么样？" → weather技能 (4.0/10)
- "明天会不会下雨？" → weather技能 (6.0/10)
- "这周末气温如何？" → weather技能 (4.0/10)

### GitHub操作  
- "帮我创建一个新的GitHub issue" → github技能 (8.67/10)
- "修复这个GitHub仓库的bug" → github技能 (10.0/10)
- "查看PR的状态" → github技能 (4.0/10)

### 系统安全
- "检查系统安全状态" → healthcheck技能 (10.0/10)  
- "强化我的服务器安全" → healthcheck技能 (8.0/10)
- "扫描漏洞" → healthcheck技能 (4.0/10)

### 文件备份
- "备份我的重要文件" → backup技能 (4.0/10)
- "恢复昨天的数据" → backup技能 (4.0/10)
- "设置自动备份策略" → healthcheck技能 (4.0/10)

### 音频控制
- "播放音乐到我的Sonos音箱" → sonoscli技能 (8.67/10)
- "暂停播放" → sonoscli技能 (4.0/10)
- "调高音量" → sonoscli技能 (2.0/10)

## 工作流程

### 1. 命令分析
```python
# 分析用户命令
result = analyze_user_command("今天北京天气怎么样？")
```

### 2. 技能匹配
- 提取关键词：["天气", "今天", "北京"]
- 计算匹配分数：weather技能 = 4.0/10
- 生成推理说明："匹配特殊关键词: 天气, 今天"

### 3. 结果返回
```json
{
  "original_command": "今天北京天气怎么样？",
  "matches": [
    {
      "skill_name": "weather",
      "confidence": 4.0,
      "reasoning": "匹配特殊关键词: 天气, 今天"
    }
  ],
  "analysis_summary": "中等置信度匹配到技能 'weather' (4.0/10)"
}
```

## 安装和使用

### 安装技能
```bash
# 复制到技能目录
cp -r intelligent-skill-matcher ~/.openclaw/workspace/skills/

# 或使用OpenClaw安装命令（如果支持）
openclaw install intelligent-skill-matcher
```

### 直接使用
```bash
# 分析单个命令
python3 ~/.openclaw/workspace/skills/intelligent-skill-matcher/scripts/analyze_command.py "今天北京天气怎么样？"

# 在OpenClaw中集成
sessions_spawn "使用intelligent-skill-matcher分析: 今天北京天气怎么样？"
```

## 配置和自定义

### 添加新技能支持
编辑 `scripts/analyze_command.py` 中的 `special_keywords` 字典：

```python
special_keywords = {
    'your-new-skill': ['关键词1', '关键词2', 'keyword1', 'keyword2']
}
```

### 调整匹配参数
修改 `calculate_match_score()` 函数中的权重和阈值：

```python
# 中文关键词权重
score += 3.0 if has_chinese else 2.0

# 英文关键词权重  
score += 2.0

# 技能名称匹配权重
score += 5.0
```

## 性能指标

- **匹配准确率**：>85% 对于常见中文命令
- **响应时间**：<100ms 对于单次分析
- **支持技能数**：所有已安装的OpenClaw技能
- **内存占用**：<50MB

## 故障排除

### 常见问题
1. **低置信度匹配**：检查技能描述是否包含相关关键词
2. **无匹配结果**：确认技能是否正确安装在技能目录中
3. **导入错误**：确保Python路径配置正确

### 调试命令
```bash
# 运行全面测试
cd ~/.openclaw/workspace/skills/intelligent-skill-matcher
python3 package_skill.py

# 查看技能列表
python3 scripts/load_skills.py
```

## 贡献和改进

欢迎提交改进建议：
- 添加更多中文关键词
- 优化匹配算法
- 支持新的技能类型
- 改进性能和准确性

## 版本历史

- **v1.0.3**：修复模块导入问题，完善测试套件
- **v1.0.2**：增强中文关键词支持，改进置信度计算
- **v1.0.1**：初始版本，基础匹配功能
- **v1.0.0**：概念验证版本

## 许可证

MIT License - 免费使用和修改