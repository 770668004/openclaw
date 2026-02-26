#!/usr/bin/env python3
"""
智能技能匹配器 - 包管理脚本
用于打包、测试和部署智能技能匹配器
"""

import os
import json
import shutil
from pathlib import Path

def create_package():
    """创建技能包"""
    skill_dir = Path(__file__).parent.absolute()
    package_file = skill_dir / "package.json"
    
    # 读取现有的 package.json
    if package_file.exists():
        with open(package_file, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
    else:
        package_data = {
            "name": "intelligent-skill-matcher",
            "version": "1.0.0",
            "description": "智能技能匹配器 - 自动分析用户命令并匹配最适合的技能",
            "main": "scripts/analyze_command.py",
            "scripts": {
                "test": "python3 scripts/test_improved_matcher.py",
                "analyze": "python3 scripts/analyze_command.py"
            },
            "keywords": ["skill", "matcher", "ai", "command", "analysis", "chinese", "智能", "匹配", "技能"],
            "author": "OpenClaw AI Assistant",
            "license": "MIT",
            "dependencies": {},
            "openclaw": {
                "skill_type": "utility",
                "language_support": ["zh", "en"],
                "requires_permissions": []
            }
        }
    
    # 更新版本号
    current_version = package_data.get("version", "1.0.0")
    version_parts = current_version.split('.')
    version_parts[-1] = str(int(version_parts[-1]) + 1)
    new_version = '.'.join(version_parts)
    package_data["version"] = new_version
    
    # 写回 package.json
    with open(package_file, 'w', encoding='utf-8') as f:
        json.dump(package_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 技能包已更新到版本 {new_version}")
    return package_data

def validate_skill_structure():
    """验证技能结构"""
    skill_dir = Path(__file__).parent.absolute()
    
    required_files = [
        "SKILL.md",
        "package.json",
        "scripts/analyze_command.py",
        "scripts/load_skills.py",
        "scripts/test_improved_matcher.py",
        "references/skill_matching_rules.md",
        "references/skill_matching_examples.md",
        "README.md"
    ]
    
    missing_files = []
    for file in required_files:
        if not (skill_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
        return False
    else:
        print("✅ 所有必要文件都存在")
        return True

def run_comprehensive_test():
    """运行全面测试"""
    print("🧪 运行全面测试...")
    
    # 测试中文天气命令
    test_commands = [
        "今天北京天气怎么样？",
        "备份我的重要文件",
        "检查系统安全状态",
        "帮我创建一个新的GitHub issue"
    ]
    
    from scripts.analyze_command import analyze_user_command
    
    all_passed = True
    for command in test_commands:
        result = analyze_user_command(command)
        if not result['matches']:
            print(f"❌ 命令 '{command}' 未找到匹配")
            all_passed = False
        else:
            best_match = result['matches'][0]
            confidence = best_match['confidence']
            if confidence < 2.0:
                print(f"⚠️  命令 '{command}' 置信度较低 ({confidence}/10)")
            else:
                print(f"✅ 命令 '{command}' 匹配成功 ({confidence}/10)")
    
    if all_passed:
        print("✅ 所有测试通过!")
    else:
        print("⚠️  部分测试需要关注")
    
    return all_passed

def main():
    """主函数"""
    print("📦 智能技能匹配器 - 包管理工具")
    print("=" * 50)
    
    # 验证结构
    if not validate_skill_structure():
        return
    
    # 创建/更新包
    package_data = create_package()
    
    # 运行测试
    print("\n" + "=" * 50)
    run_comprehensive_test()
    
    print("\n" + "=" * 50)
    print("🎯 技能包准备完成!")
    print(f"名称: {package_data['name']}")
    print(f"版本: {package_data['version']}")
    print(f"描述: {package_data['description']}")
    print("\n下一步:")
    print("1. 使用 openclaw install 来安装此技能")
    print("2. 或直接在 OpenClaw 中使用 scripts/analyze_command.py")

if __name__ == "__main__":
    main()