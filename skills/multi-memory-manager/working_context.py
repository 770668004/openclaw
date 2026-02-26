#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作上下文管理模块
处理临时工作上下文，3天周期自动清理
"""

import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

class WorkingContextManager:
    def __init__(self, workspace_path="/home/kousoyu/.openclaw/workspace"):
        self.workspace_path = Path(workspace_path)
        self.context_file = self.workspace_path / "WORKING_CONTEXT.md"
        self.cleanup_threshold = 3 * 24 * 3600  # 3天（秒）
        
    def save_context(self, context_data, priority="normal"):
        """
        保存工作上下文
        Args:
            context_data (str): 上下文内容
            priority (str): 优先级 (high/normal/low)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        context_entry = f"## {timestamp} - Priority: {priority}\n{context_data}\n\n"
        
        # 追加到文件
        with open(self.context_file, 'a', encoding='utf-8') as f:
            f.write(context_entry)
            
        print(f"✅ 工作上下文已保存到 {self.context_file}")
        
    def load_context(self):
        """
        加载当前有效的工作上下文（3天内）
        Returns:
            str: 有效的工作上下文内容
        """
        if not self.context_file.exists():
            return ""
            
        current_time = time.time()
        valid_contexts = []
        
        with open(self.context_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 按条目分割（每个条目以 ## 开头）
        entries = content.split('## ')
        for entry in entries[1:]:  # 跳过第一个空条目
            if not entry.strip():
                continue
                
            # 提取时间戳
            try:
                timestamp_str = entry.split(' - Priority:')[0]
                entry_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                entry_timestamp = entry_time.timestamp()
                
                # 检查是否在3天内
                if current_time - entry_timestamp <= self.cleanup_threshold:
                    valid_contexts.append(entry)
                else:
                    print(f"🧹 清理过期上下文: {timestamp_str}")
                    
            except ValueError:
                # 如果时间戳格式错误，保留条目但标记
                valid_contexts.append(f"[INVALID TIMESTAMP] {entry}")
                
        return "## ".join(valid_contexts)
        
    def cleanup_expired(self):
        """清理过期的工作上下文"""
        valid_context = self.load_context()
        
        # 重写文件只保留有效内容
        with open(self.context_file, 'w', encoding='utf-8') as f:
            if valid_context:
                f.write("## " + valid_context)
                
        print(f"🧹 工作上下文清理完成")
        
    def get_context_summary(self):
        """获取工作上下文摘要"""
        context = self.load_context()
        if not context:
            return "无当前工作上下文"
            
        # 简单摘要：显示最近的几个条目
        entries = context.split('## ')[1:]
        recent_entries = entries[-3:]  # 最近3个条目
        
        summary = "### 最近工作上下文摘要:\n"
        for entry in recent_entries:
            lines = entry.strip().split('\n')
            if lines:
                timestamp_priority = lines[0]
                content_preview = '\n'.join(lines[1:3]) if len(lines) > 1 else "无内容"
                summary += f"- {timestamp_priority}\n  {content_preview[:100]}...\n"
                
        return summary

# 使用示例
if __name__ == "__main__":
    context_manager = WorkingContextManager()
    
    # 保存上下文示例
    context_manager.save_context("正在开发多记忆管理系统", priority="high")
    
    # 加载上下文
    current_context = context_manager.load_context()
    print("当前上下文:")
    print(current_context)
    
    # 获取摘要
    summary = context_manager.get_context_summary()
    print("\n上下文摘要:")
    print(summary)
    
    # 清理过期内容
    context_manager.cleanup_expired()