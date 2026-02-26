#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能技能匹配器初始化脚本
"""

import os
import sys
import json
from pathlib import Path

def init_skill_directory():
    """初始化技能目录结构"""
    skill_dir = Path(__file__).parent.parent
    
    # 创建必要的子目录
    directories = [
        "scripts",
        "references", 
        "assets"
    ]
    
    for dir_name in directories:
        dir_path = skill_dir / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"✓ 创建目录: {dir_path}")
    
    # 创建空的资产文件（如果不存在）
    assets_dir = skill_dir / "assets"
    if not (assets_dir / ".gitkeep").exists():
        with open(assets_dir / ".gitkeep", "w") as f:
            f.write("# Asset files go here\n")
        print("✓ 创建资产目录标记文件")
    
    print("✓ 技能目录初始化完成")

def validate_skill_structure():
    """验证技能结构是否完整"""
    skill_dir = Path(__file__).parent.parent
    
    required_files = [
        "SKILL.md",
        "scripts/analyze_command.py",
        "scripts/load_skills.py", 
        "scripts/test_skill_matcher.py",
        "references/skill_matching_rules.md",
        "references/skill_matching_examples.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = skill_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)
        else:
            print(f"✓ 找到文件: {file_path}")
    
    if missing_files:
        print("❌ 缺少以下必需文件:")
        for missing in missing_files:
            print(f"  - {missing}")
        return False
    
    print("✓ 技能结构验证通过")
    return True

def main():
    """主函数"""
    print("=== 智能技能匹配器初始化 ===\n")
    
    init_skill_directory()
    print()
    validate_skill_structure()
    
    print("\n=== 初始化完成 ===")
    print("技能已准备好进行测试和打包")

if __name__ == "__main__":
    main()