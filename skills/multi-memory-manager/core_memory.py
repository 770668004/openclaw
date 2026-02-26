#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心记忆管理模块
处理最重要的命令、主要事情、永久性指令
"""

import os
import json
from datetime import datetime
from pathlib import Path

class CoreMemoryManager:
    def __init__(self, workspace_path="/home/kousoyu/.openclaw/workspace"):
        self.workspace_path = Path(workspace_path)
        self.core_file = self.workspace_path / "CORE_MEMORY.md"
        
    def initialize_core_memory(self):
        """初始化核心记忆文件"""
        if not self.core_file.exists():
            initial_content = """# CORE_MEMORY.md - 核心记忆文件

> **这是最重要的记忆文件** - 包含永久性指令、核心行为准则和重要偏好

## 核心指令

## 重要偏好

## 行为准则

## 安全规则

---

*最后更新: {timestamp}*
*此文件永不自动删除，修改需要用户确认*
""".format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"))
            
            with open(self.core_file, 'w', encoding='utf-8') as f:
                f.write(initial_content)
                
    def save_core_instruction(self, instruction):
        """
        保存核心指令
        Args:
            instruction (str): 核心指令内容
        """
        # 确保核心文件存在
        if not self.core_file.exists():
            self.initialize_core_memory()
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 读取现有内容
        with open(self.core_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 找到核心指令部分并添加新指令
        if "## 核心指令" in content:
            # 在核心指令部分添加新条目
            core_section_start = content.find("## 核心指令")
            core_section_end = content.find("\n## ", core_section_start + 1)
            if core_section_end == -1:
                core_section_end = len(content)
                
            core_section = content[core_section_start:core_section_end]
            
            # 检查是否已经存在相同的指令
            if instruction.strip() not in core_section:
                new_entry = f"\n- [{timestamp}] {instruction.strip()}"
                updated_core_section = core_section + new_entry
                
                updated_content = content[:core_section_start] + updated_core_section + content[core_section_end:]
                
                with open(self.core_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                    
                print(f"✅ 核心指令已保存到 {self.core_file}")
            else:
                print("ℹ️  核心指令已存在，跳过重复保存")
        else:
            # 如果没有核心指令部分，直接追加
            with open(self.core_file, 'a', encoding='utf-8') as f:
                f.write(f"\n- [{timestamp}] {instruction.strip()}\n")
                
            print(f"✅ 核心指令已追加到 {self.core_file}")
            
    def load_core_memory(self):
        """
        加载核心记忆
        Returns:
            str: 核心记忆内容
        """
        if not self.core_file.exists():
            return ""
            
        with open(self.core_file, 'r', encoding='utf-8') as f:
            return f.read()
            
    def get_core_summary(self):
        """获取核心记忆摘要"""
        if not self.core_file.exists():
            return "无核心记忆"
            
        with open(self.core_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 提取核心指令部分
        if "## 核心指令" in content:
            core_start = content.find("## 核心指令")
            core_end = content.find("\n## ", core_start + 1)
            if core_end == -1:
                core_end = len(content)
            core_instructions = content[core_start:core_end]
            
            # 统计指令数量
            instruction_count = core_instructions.count('\n- ')
            
            return f"包含 {instruction_count} 条核心指令"
        else:
            return "核心记忆文件存在但无核心指令部分"

# 使用示例
if __name__ == "__main__":
    core_manager = CoreMemoryManager()
    
    # 初始化核心记忆
    core_manager.initialize_core_memory()
    
    # 保存核心指令
    core_manager.save_core_instruction("总是先确认再执行敏感操作")
    core_manager.save_core_instruction("默认使用中文交流")
    
    # 加载核心记忆
    core_memory = core_manager.load_core_memory()
    print("核心记忆内容:")
    print(core_memory)
    
    # 获取摘要
    summary = core_manager.get_core_summary()
    print("\n核心记忆摘要:")
    print(summary)