#!/usr/bin/env python3
"""
智能命令分析器
分析用户命令并匹配最适合的技能
"""

import json
import re
import os
import sys
from typing import List, Dict, Tuple

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def load_available_skills():
    """加载可用技能 - 简化版本用于测试"""
    # 这里使用简化版本，实际使用时会调用load_skills.py
    skills = [
        {
            'name': 'weather',
            'description': 'Get current weather and forecasts via wttr.in or Open-Meteo. Use when: user asks about weather, temperature, or forecasts for any location. NOT for: historical weather data, severe weather alerts, or detailed meteorological analysis. No API key needed.',
            'path': '/home/kousoyu/.npm-global/lib/node_modules/openclaw/skills/weather/SKILL.md'
        },
        {
            'name': 'github',
            'description': 'GitHub operations via `gh` CLI: issues, PRs, CI runs, code review, API queries. Use when: (1) checking PR status or CI, (2) creating/commenting on issues, (3) listing/filtering PRs or issues, (4) viewing run logs. NOT for: complex web UI interactions requiring manual browser flows (use browser tooling when available), bulk operations across many repos (script with gh api), or when gh auth is not configured.',
            'path': '/home/kousoyu/.npm-global/lib/node_modules/openclaw/skills/github/SKILL.md'
        },
        {
            'name': 'backup',
            'description': 'Advanced backup and restore system with intelligent scheduling, multiple storage backends, encryption, and AI-powered retention policies. Supports cloud storage, local backups, incremental snapshots, and automated recovery testing.',
            'path': '/home/kousoyu/.openclaw/workspace/skills/backup-upgraded/SKILL.md'
        },
        {
            'name': 'healthcheck',
            'description': 'Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw (laptop, workstation, Pi, VPS).',
            'path': '/home/kousoyu/.npm-global/lib/node_modules/openclaw/skills/healthcheck/SKILL.md'
        },
        {
            'name': 'sonoscli',
            'description': 'Control Sonos speakers (discover/status/play/volume/group).',
            'path': '/home/kousoyu/.openclaw/workspace/skills/sonoscli/SKILL.md'
        },
        {
            'name': 'concise-output',
            'description': 'Optimize text output to be concise, clear, and well-formatted. Use when user requests responses that are non-redundant, focused on key points, easy to understand, appropriately detailed without being verbose, and visually clean with good formatting.',
            'path': '/home/kousoyu/.openclaw/workspace/skills/concise-output/SKILL.md'
        },
        {
            'name': 'Find',
            'description': 'Locate anything with progressive search expansion, multi-source validation, and iterative refinement until found.',
            'path': '/home/kousoyu/.openclaw/workspace/skills/find/SKILL.md'
        },
        {
            'name': 'multi-memory-manager',
            'description': 'Multi-module memory management system with automatic cleanup, GitHub sync, and different retention policies for core vs working memory.',
            'path': '/home/kousoyu/.openclaw/workspace/skills/multi-memory-manager/SKILL.md'
        },
        {
            'name': 'skill-evolution-manager',
            'description': '智能技能进化管理系统：自动分类、审计和升级OpenClaw技能，按功能分组（安全与审计、文件管理、通信协作等），执行严格的代码审计，支持24小时周期性自我升级，优先级低于当前任务。',
            'path': '/home/kousoyu/.openclaw/workspace/skills/skill-evolution-manager/SKILL.md'
        }
    ]
    return skills

def analyze_user_command(command: str) -> Dict:
    """
    分析用户命令并返回匹配的技能建议
    
    Args:
        command: 用户输入的命令文本
        
    Returns:
        包含匹配技能和置信度的字典
    """
    # 加载可用技能
    available_skills = load_available_skills()
    
    # 预处理命令文本
    command_lower = command.lower().strip()
    
    # 初始化匹配结果
    matches = []
    
    # 为每个可用技能计算匹配分数
    for skill in available_skills:
        score = calculate_match_score(command_lower, skill)
        if score > 0:
            matches.append({
                'skill_name': skill['name'],
                'description': skill['description'],
                'confidence': score,
                'reasoning': get_match_reasoning(command_lower, skill)
            })
    
    # 按置信度排序
    matches.sort(key=lambda x: x['confidence'], reverse=True)
    
    return {
        'original_command': command,
        'matches': matches[:3],  # 返回前3个最佳匹配
        'analysis_summary': generate_analysis_summary(command, matches)
    }

def calculate_match_score(command: str, skill: Dict) -> float:
    """计算命令与技能的匹配分数"""
    score = 0.0
    description = skill['description'].lower()
    name = skill['name'].lower()
    
    # 检测是否为中文命令
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', command))
    
    # 基于技能名称的直接匹配（高权重）
    if name in command:
        score += 5.0
    
    # 基于描述中的关键词匹配
    keywords = extract_keywords(description)
    for keyword in keywords:
        if len(keyword) > 1 and keyword in command:  # 降低最小长度要求
            if re.search(r'[\u4e00-\u9fff]', keyword):  # 中文关键词
                score += 3.0 if has_chinese else 2.0
            else:  # 英文关键词
                score += 2.0
    
    # 基于触发条件匹配（Use when / 当...时）
    triggers = extract_triggers(description)
    for trigger in triggers:
        if trigger in command:
            score += 3.0
    
    # 特定技能的特殊关键词匹配（增强中文支持）
    special_keywords = {
        'github': ['github', 'git', 'issue', 'pr', 'pull request', 'repository', 'repo', 'commit', 'branch', '代码', '仓库', '提交', '分支', 'bug', '错误', '问题', '开发', '编程'],
        'weather': ['天气', 'temperature', 'forecast', 'rain', 'snow', 'wind', 'humidity', '气温', '预报', '下雨', '下雪', '温度', '气候', '冷', '热', '暖', '凉', '阴', '晴', '多云', '雷', '雨', '雪', '风', '湿度', '今天', '明天', '后天', '周末'],
        'backup': ['backup', 'restore', 'recover', '备份', '恢复', '数据', 'archive', '存档', '数据备份', '文件备份', '重要', '保存', '存储', '保护', '复制', '镜像', '灾难恢复', '快照', '增量'],
        'healthcheck': ['security', '安全', 'hardening', 'firewall', 'ssh', 'audit', 'risk', 'exposure', '防火墙', '审计', '风险', '加固', '漏洞', '检查', '状态', '健康', '扫描', '测试', '防护', '监控', '强化', '服务器', '系统', '网络', '主机', '渗透', '入侵', '恶意', '病毒', '木马', '后门', '权限', '访问控制', '加密', '证书', '日志', '告警', '威胁', '攻击', '防御', '隔离', '沙箱', '更新', '补丁', '升级', '配置', '策略', '合规', '标准', '最佳实践', '保护', '验证', '认证', '授权', '身份', '会话', '超时', '锁定', '失败', '重试', '限制', '速率', '带宽', '流量', '异常', '行为', '模式', '分析', '检测', '预防', '响应', '恢复', '备份', '容灾', '高可用', '负载', '压力', '性能', '资源', 'CPU', '内存', '磁盘', '网络', '连接', '端口', '服务', '进程', '用户', '组', '角色', '权限', 'ACL', 'RBAC', 'ABAC', '零信任', '最小权限', '纵深防御', '系统安全', '网络安全', '主机安全', '渗透测试'],
        'sonoscli': ['sonos', 'speaker', 'music', 'audio', 'volume', 'play', 'pause', '音箱', '音乐', '音量', '播放', '暂停', '音响', '声音', '歌曲', '专辑', '艺术家', '流媒体'],
        'concise-output': ['concise', '简洁', '简明', '输出', '格式化', '清晰', '精简', '简短', '摘要', '总结', '要点', '重点', '简化', '压缩'],
        'find': ['find', 'locate', 'search', '查找', '搜索', '定位', '发现', '寻找', '查询', '检索'],
        'multi-memory-manager': ['memory', '记忆', '存储', '记录', '历史', '日志', '备份', '管理', '组织', '分类'],
        'skill-evolution-manager': ['skill', 'evolution', 'upgrade', 'update', 'manage', '技能', '进化', '升级', '更新', '管理', '自动化', '智能', '维护']
    }
    
    if name in special_keywords:
        for keyword in special_keywords[name]:
            if keyword in command:
                if re.search(r'[\u4e00-\u9fff]', keyword):  # 中文关键词
                    score += 3.0 if has_chinese else 2.0
                else:  # 英文关键词
                    score += 2.0
    
    # 动态归一化：基于实际最大可能分数
    if score == 0:
        return 0.0
    
    # 使用更合理的归一化方法
    # 最大分数基于特殊关键词数量和权重
    max_possible_score = 15.0  # 保守估计的最大分数
    
    # 如果检测到中文且有中文匹配，提高基础分数
    if has_chinese and score < 3.0:
        # 对于中文命令，即使只匹配一个关键词也应该有合理的基础分数
        base_score = min(5.0, score * 2.0)  # 提高基础分数
        normalized_score = min(10.0, base_score)
    else:
        normalized_score = min(10.0, (score / max_possible_score) * 10.0)
    
    return round(normalized_score, 2)

def extract_keywords(description: str) -> List[str]:
    """从技能描述中提取关键词"""
    # 提取英文单词（包括带连字符的）
    english_words = re.findall(r'\b[a-zA-Z][a-zA-Z\-]{2,}\b', description)
    
    # 提取中文词语（1个或更多字符，因为中文单字也有意义）
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', description)
    chinese_words = re.findall(r'[\u4e00-\u9fff]{2,}', description)
    
    # 合并并去重
    all_words = english_words + chinese_words + chinese_chars
    
    # 过滤常见停用词
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'when', 'use', 'not', 'via', 'api', 'user', 'asks', 'about', 'any', 'location', 'this', 'that', 'these', 'those'}
    keywords = [word for word in all_words if word.lower() not in stop_words]
    return list(set(keywords))

def extract_triggers(description: str) -> List[str]:
    """从技能描述中提取触发词"""
    triggers = []
    
    # 查找 "Use when" 相关的触发条件
    if 'use when' in description:
        use_when_part = description.split('use when')[-1]
        # 提取括号内的内容
        bracket_content = re.findall(r'\(([^)]+)\)', use_when_part)
        for content in bracket_content:
            # 分割条件
            conditions = re.split(r'[,\n]', content)
            for condition in conditions:
                condition = condition.strip()
                if condition and len(condition) > 1:  # 降低最小长度要求
                    triggers.append(condition)
    
    # 查找中文触发条件
    if '当' in description:
        parts = description.split('当')
        for part in parts[1:]:
            if '时' in part:
                when_content = part.split('时')[0].strip()
                if when_content and len(when_content) > 1:
                    triggers.append(when_content)
            elif '使用' in part:
                when_content = part.split('使用')[0].strip()
                if when_content and len(when_content) > 1:
                    triggers.append(when_content)
    
    return list(set(triggers))

def get_match_reasoning(command: str, skill: Dict) -> str:
    """生成匹配推理说明"""
    description = skill['description'].lower()
    name = skill['name']
    
    reasons = []
    
    # 检查技能名称匹配
    if name.lower() in command:
        reasons.append(f"包含技能名称: {name}")
    
    # 检查关键词匹配
    keywords = extract_keywords(description)
    matched_keywords = [kw for kw in keywords if len(kw) > 0 and kw in command]
    if matched_keywords:
        reasons.append(f"匹配关键词: {', '.join(matched_keywords[:3])}")
    
    # 检查触发条件匹配
    triggers = extract_triggers(description)
    matched_triggers = [t for t in triggers if t in command]
    if matched_triggers:
        reasons.append(f"满足触发条件: {', '.join(matched_triggers[:2])}")
    
    # 检查特殊关键词匹配
    special_keywords = {
        'github': ['github', 'git', 'issue', 'pr', 'pull request', 'repository', 'repo', 'commit', 'branch', '代码', '仓库', '提交', '分支', 'bug', '错误', '问题', '开发', '编程'],
        'weather': ['天气', 'temperature', 'forecast', 'rain', 'snow', 'wind', 'humidity', '气温', '预报', '下雨', '下雪', '温度', '气候', '冷', '热', '暖', '凉', '阴', '晴', '多云', '雷', '雨', '雪', '风', '湿度', '今天', '明天', '后天', '周末'],
        'backup': ['backup', 'restore', 'recover', '备份', '恢复', '数据', 'archive', '存档', '数据备份', '文件备份', '重要', '保存', '存储', '安全', '保护', '复制', '镜像'],
        'healthcheck': ['security', '安全', 'hardening', 'firewall', 'ssh', 'audit', 'risk', 'exposure', '防火墙', '审计', '风险', '加固', '漏洞', '检查', '状态', '健康', '扫描', '测试', '防护', '监控', '强化', '服务器', '系统', '网络', '主机', '渗透', '入侵', '恶意', '病毒', '木马', '后门', '权限', '访问控制', '加密', '证书', '日志', '告警', '威胁', '攻击', '防御', '隔离', '沙箱', '更新', '补丁', '升级', '配置', '策略', '合规', '标准', '最佳实践', '保护', '验证', '认证', '授权', '身份', '会话', '超时', '锁定', '失败', '重试', '限制', '速率', '带宽', '流量', '异常', '行为', '模式', '分析', '检测', '预防', '响应', '恢复', '备份', '容灾', '高可用', '负载', '压力', '性能', '资源', 'CPU', '内存', '磁盘', '网络', '连接', '端口', '服务', '进程', '用户', '组', '角色', '权限', 'ACL', 'RBAC', 'ABAC', '零信任', '最小权限', '纵深防御'],
        'sonoscli': ['sonos', 'speaker', 'music', 'audio', 'volume', 'play', 'pause', '音箱', '音乐', '音量', '播放', '暂停', '音响', '声音', '歌曲', '专辑', '艺术家', '流媒体'],
        'concise-output': ['concise', '简洁', '简明', '输出', '格式化', '清晰', '精简', '简短', '摘要', '总结', '要点', '重点', '简化', '压缩'],
        'find': ['find', 'locate', 'search', '查找', '搜索', '定位', '发现', '寻找', '查询', '检索'],
        'multi-memory-manager': ['memory', '记忆', '存储', '记录', '历史', '日志', '备份', '管理', '组织', '分类'],
        'skill-evolution-manager': ['skill', 'evolution', 'upgrade', 'update', 'manage', '技能', '进化', '升级', '更新', '管理', '自动化', '智能', '维护']
    }
    
    if name in special_keywords:
        matched_special = [kw for kw in special_keywords[name] if kw in command]
        if matched_special:
            reasons.append(f"匹配特殊关键词: {', '.join(matched_special[:2])}")
    
    return "; ".join(reasons) if reasons else "基于语义相似性匹配"

def generate_analysis_summary(command: str, matches: List[Dict]) -> str:
    """生成分析摘要"""
    if not matches:
        return "未找到匹配的技能，可能需要创建新技能或使用通用方法处理。"
    
    best_match = matches[0]
    if best_match['confidence'] >= 7.0:
        return f"高置信度匹配到技能 '{best_match['skill_name']}' ({best_match['confidence']}/10)"
    elif best_match['confidence'] >= 4.0:
        return f"中等置信度匹配到技能 '{best_match['skill_name']}' ({best_match['confidence']}/10)"
    else:
        return f"低置信度匹配到技能 '{best_match['skill_name']}' ({best_match['confidence']}/10)，建议人工确认"

def main():
    """主函数 - 用于测试"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python analyze_command.py <command>")
        sys.exit(1)
    
    command = sys.argv[1]
    result = analyze_user_command(command)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()