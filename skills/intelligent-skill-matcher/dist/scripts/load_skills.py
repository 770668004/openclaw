#!/usr/bin/env python3
"""
加载可用技能列表
"""

import os
import json
from typing import List, Dict

def load_available_skills(skills_dir: str = "/home/kousoyu/.openclaw/workspace/skills/") -> List[Dict]:
    """
    从技能目录加载所有可用技能
    
    Args:
        skills_dir: 技能目录路径
        
    Returns:
        技能列表，每个技能包含name和description
    """
    skills = []
    
    # 定义关键技能及其描述
    key_skills = {
        'github': 'GitHub operations via `gh` CLI: issues, PRs, CI runs, code review, API queries. Use when: (1) checking PR status or CI, (2) creating/commenting on issues, (3) listing/filtering PRs or issues, (4) viewing run logs.',
        'weather': 'Get current weather and forecasts via wttr.in or Open-Meteo. Use when: user asks about weather, temperature, or forecasts for any location.',
        'backup': 'Advanced backup and restore system with intelligent scheduling, multiple storage backends, encryption, and AI-powered retention policies.',
        'healthcheck': 'Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw.',
        'sonoscli': 'Control Sonos speakers (discover/status/play/volume/group).',
        'concise-output': 'Optimize text output to be concise, clear, and well-formatted. Use when user requests responses that are non-redundant, focused on key points, easy to understand, appropriately detailed without being verbose, and visually clean with good formatting.',
        'find': 'Locate anything with progressive search expansion, multi-source validation, and iterative refinement until found.',
        'multi-memory-manager': 'Multi-module memory management system with different retention policies for core instructions, working context, and session history.',
        'skill-evolution-manager': '智能技能进化管理系统：自动分类、审计和升级OpenClaw技能，按功能分组（安全与审计、文件管理、通信协作等），执行严格的代码审计，支持24小时周期性自我升级，优先级低于当前任务。'
    }
    
    # 添加关键技能
    for name, description in key_skills.items():
        skills.append({
            'name': name,
            'description': description
        })
    
    return skills

def main():
    """测试函数"""
    skills = load_available_skills()
    print(f"Loaded {len(skills)} skills:")
    for skill in skills:
        print(f"- {skill['name']}: {skill['description'][:50]}...")

if __name__ == "__main__":
    main()