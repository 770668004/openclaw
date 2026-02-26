#!/usr/bin/env python33
# -*- coding: utf-8 -*-
"""
智能技能匹配器测试脚本
"""

import sys
import os

# 添加脚本目录到Python路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from analyze_command import analyze_user_command

def test_skill_matcher():
    """测试智能技能匹配器"""
    print("=== 智能技能匹配器测试 ===\n")
    
    # 测试用例
    test_cases = [
        "今天北京天气怎么样？",
        "帮我创建一个新的GitHub issue",
        "备份我的重要文件",
        "检查系统安全状态",
        "播放音乐到我的Sonos音箱",
        "创建一个新技能来处理数据分析",
        "明天会不会下雨？",
        "修复这个GitHub仓库的bug",
        "设置自动备份策略",
        "强化我的服务器安全"
    ]
    
    for i, command in enumerate(test_cases, 1):
        print(f"测试 {i}: {command}")
        result = analyze_user_command(command)
        if result and result['matches']:
            best_match = result['matches'][0]
            print(f"  最佳匹配: {best_match['skill_name']} (置信度: {best_match['confidence']:.2f}/10)")
            print(f"  推理: {best_match['reasoning']}")
            print(f"  摘要: {result['analysis_summary']}")
        else:
            print("  无匹配结果")
        print()

if __name__ == "__main__":
    test_skill_matcher()