#!/usr/bin/env python3
"""
改进的智能技能匹配器测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analyze_command import analyze_user_command

def run_comprehensive_tests():
    """运行全面的测试用例"""
    test_cases = [
        # 天气相关
        "今天北京天气怎么样？",
        "明天会不会下雨？",
        "这周末气温如何？",
        "查看上海的天气预报",
        
        # GitHub相关
        "帮我创建一个新的GitHub issue",
        "修复这个GitHub仓库的bug",
        "查看PR的状态",
        "提交代码到main分支",
        
        # 备份相关
        "备份我的重要文件",
        "设置自动备份策略",
        "恢复昨天的数据",
        "创建系统快照",
        
        # 安全相关
        "检查系统安全状态",
        "强化我的服务器安全",
        "扫描漏洞",
        "审计防火墙配置",
        
        # 音频相关
        "播放音乐到我的Sonos音箱",
        "调高音量",
        "暂停播放",
        "播放周杰伦的歌",
        
        # 其他
        "创建一个新技能来处理数据分析",
        "查找丢失的文件",
        "简化这段文字的输出",
        "管理我的记忆存储"
    ]
    
    print("=== 改进的智能技能匹配器全面测试 ===\n")
    
    for i, command in enumerate(test_cases, 1):
        result = analyze_user_command(command)
        best_match = result['matches'][0] if result['matches'] else None
        
        print(f"测试 {i}: {command}")
        if best_match:
            print(f"  最佳匹配: {best_match['skill_name']} (置信度: {best_match['confidence']}/10)")
            print(f"  推理: {best_match['reasoning']}")
        else:
            print("  未找到匹配的技能")
        print(f"  摘要: {result['analysis_summary']}\n")

if __name__ == "__main__":
    run_comprehensive_tests()