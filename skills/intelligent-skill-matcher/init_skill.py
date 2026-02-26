#!/usr/bin/env python3
"""
智能技能匹配器初始化脚本
创建必要的目录结构和文件
"""

import os
import json

def init_skill_structure():
    """初始化技能目录结构"""
    skill_name = "intelligent-skill-matcher"
    base_path = f"~/.openclaw/workspace/skills/{skill_name}"
    base_path = os.path.expanduser(base_path)
    
    # 创建目录结构
    directories = [
        base_path,
        f"{base_path}/scripts",
        f"{base_path}/references",
        f"{base_path}/assets"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"创建目录: {directory}")
    
    # 创建初始文件
    init_files = {
        f"{base_path}/SKILL.md": "# 智能技能匹配器\n\n智能分析用户命令并自动匹配最适合的现有技能",
        f"{base_path}/README.md": "# 智能技能匹配器\n\n自动分析用户输入并推荐最合适的技能来处理任务。",
        f"{base_path}/assets/icon.png": "",  # 占位符
        f"{base_path}/package.json": json.dumps({
            "name": "intelligent-skill-matcher",
            "version": "1.0.0",
            "description": "智能技能匹配器 - 自动分析用户命令并匹配最适合的技能",
            "main": "scripts/analyze_command.py",
            "scripts": {
                "test": "python scripts/test_improved_matcher.py"
            }
        }, indent=2)
    }
    
    for file_path, content in init_files.items():
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"创建文件: {file_path}")
    
    print(f"\n技能 '{skill_name}' 初始化完成!")
    print(f"路径: {base_path}")

if __name__ == "__main__":
    init_skill_structure()