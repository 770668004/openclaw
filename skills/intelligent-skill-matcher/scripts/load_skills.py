#!/usr/bin/env python3
"""
加载可用技能列表 - 改进版本
支持从多个目录加载技能并解析SKILL.md文件
"""

import os
import re
from typing import List, Dict

def load_available_skills() -> List[Dict]:
    """
    从多个目录加载所有可用技能
    
    Returns:
        技能列表，每个技能包含name和description
    """
    skills = []
    
    # 定义要搜索的技能目录
    skill_dirs = [
        "/home/kousoyu/.openclaw/workspace/skills/",
        "/home/kousoyu/.npm-global/lib/node_modules/openclaw/skills/",
        "/home/kousoyu/.agents/skills/"
    ]
    
    # 从每个目录加载技能
    for skill_dir in skill_dirs:
        if os.path.exists(skill_dir):
            for item in os.listdir(skill_dir):
                item_path = os.path.join(skill_dir, item)
                if os.path.isdir(item_path):
                    # 尝试读取SKILL.md文件
                    skill_md_path = os.path.join(item_path, "SKILL.md")
                    if os.path.exists(skill_md_path):
                        try:
                            with open(skill_md_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            # 提取YAML frontmatter中的name和description
                            name, description = extract_skill_metadata(content)
                            if name and description:
                                skills.append({
                                    'name': name,
                                    'description': description
                                })
                        except Exception as e:
                            # 如果解析失败，使用目录名作为技能名
                            skills.append({
                                'name': item,
                                'description': f"Skill from directory: {item}"
                            })
    
    # 添加一些关键的内置技能（如果上面没找到）
    built_in_skills = {
        'github': 'GitHub operations via `gh` CLI: issues, PRs, CI runs, code review, API queries. Use when: (1) checking PR status or CI, (2) creating/commenting on issues, (3) listing/filtering PRs or issues, (4) viewing run logs.',
        'weather': 'Get current weather and forecasts via wttr.in or Open-Meteo. Use when: user asks about weather, temperature, or forecasts for any location. NOT for: historical weather data, severe weather alerts, or detailed meteorological analysis. No API key needed.',
        'backup': 'Advanced backup and restore system with intelligent scheduling, multiple storage backends, encryption, and AI-powered retention policies. Supports cloud storage, local backups, incremental snapshots, and automated recovery testing.',
        'healthcheck': 'Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw (laptop, workstation, Pi, VPS).',
        'sonoscli': 'Control Sonos speakers (discover/status/play/volume/group).',
        'concise-output': 'Optimize text output to be concise, clear, and well-formatted. Use when user requests responses that are non-redundant, focused on key points, easy to understand, appropriately detailed without being verbose, and visually clean with good formatting.',
        'find': 'Locate anything with progressive search expansion, multi-source validation, and iterative refinement until found.',
        'multi-memory-manager': 'Multi-module memory management system with different retention policies for core instructions, working context, and session history.',
        'skill-evolution-manager': '智能技能进化管理系统：自动分类、审计和升级OpenClaw技能，按功能分组（安全与审计、文件管理、通信协作等），执行严格的代码审计，支持24小时周期性自我升级，优先级低于当前任务。'
    }
    
    # 检查是否已经加载了这些内置技能
    existing_names = {skill['name'].lower() for skill in skills}
    for name, description in built_in_skills.items():
        if name.lower() not in existing_names:
            skills.append({
                'name': name,
                'description': description
            })
    
    # 去重：确保每个技能名称只出现一次
    unique_skills = []
    seen_names = set()
    for skill in skills:
        skill_name = skill['name'].lower()
        if skill_name not in seen_names:
            unique_skills.append(skill)
            seen_names.add(skill_name)
    
    return unique_skills

def extract_skill_metadata(content: str) -> tuple[str, str]:
    """从SKILL.md内容中提取name和description"""
    name = ""
    description = ""
    
    # 查找YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            yaml_content = parts[1]
            # 提取name
            name_match = re.search(r'name:\s*(.+)', yaml_content, re.IGNORECASE)
            if name_match:
                name = name_match.group(1).strip().strip('"\'')
            
            # 提取description
            desc_match = re.search(r'description:\s*(.+)', yaml_content, re.IGNORECASE)
            if desc_match:
                description = desc_match.group(1).strip().strip('"\'')
    
    return name, description

def main():
    """测试函数"""
    skills = load_available_skills()
    print(f"Loaded {len(skills)} skills:")
    for skill in skills:
        print(f"- {skill['name']}: {skill['description'][:60]}...")

if __name__ == "__main__":
    main()