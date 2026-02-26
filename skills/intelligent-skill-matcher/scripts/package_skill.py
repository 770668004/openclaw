#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能技能匹配器打包脚本
用于将技能打包成OpenClaw可安装的格式
"""

import os
import sys
import json
import shutil
from pathlib import Path

def package_skill():
    """打包技能"""
    skill_dir = Path(__file__).parent.parent
    skill_name = skill_dir.name
    
    print(f"正在打包技能: {skill_name}")
    
    # 创建打包目录
    package_dir = skill_dir / "dist"
    package_dir.mkdir(exist_ok=True)
    
    # 复制必要的文件
    files_to_copy = [
        "SKILL.md",
        "scripts/analyze_command.py",
        "scripts/load_skills.py",
        "scripts/init_skill.py",
        "scripts/test_skill_matcher.py",
        "references/skill_matching_rules.md",
        "references/skill_matching_examples.md"
    ]
    
    for file_path in files_to_copy:
        src = skill_dir / file_path
        if src.exists():
            dst = package_dir / file_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  已复制: {file_path}")
    
    # 创建package.json
    package_info = {
        "name": skill_name,
        "version": "1.0.0",
        "description": "智能技能匹配器 - 自动分析用户命令并匹配最适合的OpenClaw技能",
        "main": "scripts/analyze_command.py",
        "scripts": {
            "test": "python scripts/test_skill_matcher.py",
            "init": "python scripts/init_skill.py"
        },
        "keywords": ["skill", "matcher", "ai", "command", "analysis", "chinese"],
        "author": "OpenClaw Community",
        "license": "MIT",
        "openclaw": {
            "skill_version": "1.0",
            "requires": {
                "python": ">=3.8"
            }
        }
    }
    
    with open(package_dir / "package.json", "w", encoding="utf-8") as f:
        json.dump(package_info, f, indent=2, ensure_ascii=False)
    
    print(f"\n技能已成功打包到: {package_dir}")
    print("可以使用以下命令安装:")
    print(f"openclaw skill install {package_dir}")

if __name__ == "__main__":
    package_skill()