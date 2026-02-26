#!/usr/bin/env python3
"""
智能命令分析器
分析用户命令并匹配最适合的技能
"""

import json
import re
from typing import List, Dict, Tuple
from load_skills import load_available_skills

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
    
    # 基于技能名称的直接匹配（高权重）
    if name in command:
        score += 5.0
    
    # 基于描述中的关键词匹配
    keywords = extract_keywords(description)
    for keyword in keywords:
        if len(keyword) > 2 and keyword in command:
            score += 2.0
    
    # 基于触发条件匹配（Use when / 当...时）
    triggers = extract_triggers(description)
    for trigger in triggers:
        if trigger in command:
            score += 3.0
    
    # 特定技能的特殊关键词匹配
    special_keywords = {
        'github': ['github', 'git', 'issue', 'pr', 'pull request', 'repository', 'repo', 'commit', 'branch', '代码', '仓库', '提交', '分支'],
        'weather': ['天气', 'temperature', 'forecast', 'rain', 'snow', 'wind', 'humidity', '气温', '预报', '下雨', '下雪', '温度', '气候'],
        'backup': ['backup', 'restore', 'recover', '备份', '恢复', '数据', 'archive', '存档', '数据备份', '文件备份'],
        'healthcheck': ['security', '安全', 'hardening', 'firewall', 'ssh', 'audit', 'risk', 'exposure', '防火墙', '审计', '风险', '加固', '漏洞', '检查'],
        'sonoscli': ['sonos', 'speaker', 'music', 'audio', 'volume', 'play', 'pause', '音箱', '音乐', '音量', '播放', '暂停', '音响'],
        'concise-output': ['concise', '简洁', '简明', '输出', '格式化', '清晰', '精简']
    }
    
    if name in special_keywords:
        for keyword in special_keywords[name]:
            if keyword in command:
                score += 3.0
    
    # 归一化分数 (0-10范围)
    # 使用固定的最大分数来避免过低的归一化
    max_score = 15.0  # 最大可能分数
    normalized_score = min(10.0, (score / max_score) * 10.0)
    
    return round(normalized_score, 2)

def extract_keywords(description: str) -> List[str]:
    """从技能描述中提取关键词"""
    # 提取英文单词
    english_words = re.findall(r'\b[a-zA-Z]{3,}\b', description)
    
    # 提取中文词语（2个或更多字符）
    chinese_words = re.findall(r'[\u4e00-\u9fff]{2,}', description)
    
    # 合并并去重
    all_words = english_words + chinese_words
    
    # 过滤常见停用词
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'when', 'use', 'not', 'via', 'api', 'user', 'asks', 'about', 'any', 'location'}
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
                if condition and len(condition) > 2:
                    triggers.append(condition)
    
    # 查找中文触发条件
    if '当' in description:
        parts = description.split('当')
        for part in parts[1:]:
            if '时' in part:
                when_content = part.split('时')[0].strip()
                if when_content and len(when_content) > 2:
                    triggers.append(when_content)
            elif '使用' in part:
                when_content = part.split('使用')[0].strip()
                if when_content and len(when_content) > 2:
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
    matched_keywords = [kw for kw in keywords if len(kw) > 2 and kw in command]
    if matched_keywords:
        reasons.append(f"匹配关键词: {', '.join(matched_keywords[:3])}")
    
    # 检查触发条件匹配
    triggers = extract_triggers(description)
    matched_triggers = [t for t in triggers if t in command]
    if matched_triggers:
        reasons.append(f"满足触发条件: {', '.join(matched_triggers[:2])}")
    
    # 检查特殊关键词匹配
    special_keywords = {
        'github': ['github', 'git', 'issue', 'pr', 'pull request', 'repository', 'repo', 'commit', 'branch', '代码', '仓库', '提交', '分支'],
        'weather': ['天气', 'temperature', 'forecast', 'rain', 'snow', 'wind', 'humidity', '气温', '预报', '下雨', '下雪', '温度', '气候'],
        'backup': ['backup', 'restore', 'recover', '备份', '恢复', '数据', 'archive', '存档', '数据备份', '文件备份'],
        'healthcheck': ['security', '安全', 'hardening', 'firewall', 'ssh', 'audit', 'risk', 'exposure', '防火墙', '审计', '风险', '加固', '漏洞', '检查'],
        'sonoscli': ['sonos', 'speaker', 'music', 'audio', 'volume', 'play', 'pause', '音箱', '音乐', '音量', '播放', '暂停', '音响'],
        'concise-output': ['concise', '简洁', '简明', '输出', '格式化', '清晰', '精简']
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