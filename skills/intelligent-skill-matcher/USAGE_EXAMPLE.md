# 智能技能匹配器使用示例

## 基本用法

```bash
# 直接调用分析脚本
python3 /home/kousoyu/.openclaw/workspace/skills/intelligent-skill-matcher/scripts/analyze_command.py "今天北京天气怎么样？"

# 在OpenClaw中作为工具调用
/openclaw skill intelligent-skill-matcher "备份我的重要文件"
```

## 集成到OpenClaw工作流

### 1. 自动技能路由
在用户输入命令时，先通过智能匹配器分析，然后自动调用最匹配的技能：

```python
# 伪代码示例
user_command = "检查系统安全状态"
analysis_result = analyze_user_command(user_command)

if analysis_result['matches']:
    best_match = analysis_result['matches'][0]
    if best_match['confidence'] >= 7.0:
        # 高置信度 - 自动执行
        execute_skill(best_match['skill_name'], user_command)
    elif best_match['confidence'] >= 4.0:
        # 中等置信度 - 询问用户确认
        ask_user_confirmation(best_match, user_command)
    else:
        # 低置信度 - 提供选项
        show_skill_options(analysis_result['matches'])
```

### 2. 多技能协调
对于复杂命令，可能需要多个技能协作：

```python
# 示例： "备份我的GitHub仓库并检查安全性"
user_command = "备份我的GitHub仓库并检查安全性"
analysis_result = analyze_user_command(user_command)

# 可能返回多个高置信度匹配
# - backup (6.0/10): 匹配"备份"
# - github (6.0/10): 匹配"GitHub", "仓库"  
# - healthcheck (4.0/10): 匹配"安全", "检查"

# 协调执行多个技能
execute_workflow(['backup', 'github', 'healthcheck'], user_command)
```

## 中文命令支持示例

| 用户命令 | 匹配技能 | 置信度 | 关键词匹配 |
|---------|---------|--------|-----------|
| 今天北京天气怎么样？ | weather | 4.0/10 | 天气, 今天 |
| 明天会不会下雨？ | weather | 6.0/10 | 下雨, 雨 |
| 备份我的重要文件 | backup | 4.0/10 | 备份, 重要 |
| 检查系统安全状态 | healthcheck | 10.0/10 | 安全, 检查 |
| 强化我的服务器安全 | healthcheck | 8.0/10 | 安全, 强化 |
| 帮我创建一个新的GitHub issue | github | 8.67/10 | github, git |
| 播放音乐到我的Sonos音箱 | sonoscli | 8.67/10 | sonos, 音箱 |
| 简化这段文字的输出 | concise-output | 4.0/10 | 输出, 简化 |

## 配置和自定义

### 添加新的特殊关键词
编辑 `scripts/analyze_command.py` 中的 `special_keywords` 字典：

```python
special_keywords = {
    'your-new-skill': ['关键词1', '关键词2', 'keyword1', 'keyword2'],
    # ... 其他技能
}
```

### 调整匹配阈值
修改置信度阈值以控制自动执行的严格程度：

```python
# 在集成代码中
HIGH_CONFIDENCE_THRESHOLD = 7.0    # 自动执行
MEDIUM_CONFIDENCE_THRESHOLD = 4.0  # 询问确认
```

## 性能优化建议

1. **缓存技能列表**: 避免每次调用都重新加载技能
2. **预编译正则表达式**: 提高关键词提取速度
3. **限制搜索范围**: 对于特定场景只加载相关技能
4. **异步处理**: 对于批量命令分析使用异步处理

## 故障排除

### 常见问题
- **匹配分数过低**: 检查技能描述中的关键词是否包含中文
- **未找到匹配**: 确认技能目录路径配置正确
- **导入错误**: 确保Python路径包含所有必要模块

### 调试模式
启用详细日志来查看匹配过程：

```python
# 在analyze_command.py中设置
DEBUG_MODE = True
```