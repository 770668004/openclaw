#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
操作日志管理模块
记录代码修改、JSON配置变更等操作，重要记录永久保存，普通记录1天后删除
"""

import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import hashlib

class OperationLogManager:
    def __init__(self, workspace_path="/home/kousoyu/.openclaw/workspace"):
        self.workspace_path = Path(workspace_path)
        self.log_file = self.workspace_path / "OPERATION_LOG.md"
        self.cleanup_threshold = 24 * 3600  # 1天（秒）
        
    def log_operation(self, operation_type, details, importance="normal", file_path=None):
        """
        记录操作日志
        Args:
            operation_type (str): 操作类型 (create/modify/delete/config/code/json)
            details (str): 操作详情
            importance (str): 重要性 (critical/high/normal/low)
            file_path (str): 相关文件路径（可选）
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 生成操作摘要
        operation_summary = self._generate_operation_summary(operation_type, details, file_path)
        
        log_entry = f"""## {timestamp} - {operation_type.upper()}
**重要性**: {importance}
**文件**: {file_path or 'N/A'}
**摘要**: {operation_summary}

{details}

---
"""
        
        # 追加到日志文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        print(f"✅ 操作日志已记录到 {self.log_file}")
        
    def _generate_operation_summary(self, operation_type, details, file_path):
        """生成操作摘要"""
        if operation_type == "code":
            return f"代码修改: {file_path}"
        elif operation_type == "json":
            return f"JSON配置变更: {file_path}"
        elif operation_type == "create":
            return f"创建文件: {file_path}"
        elif operation_type == "modify":
            return f"修改文件: {file_path}"
        elif operation_type == "delete":
            return f"删除文件: {file_path}"
        elif operation_type == "config":
            return f"配置变更: {file_path}"
        else:
            # 截取详情的前50个字符作为摘要
            return details[:50] + "..." if len(details) > 50 else details
            
    def load_operation_log(self, days_back=7, importance_filter=None):
        """
        加载操作日志
        Args:
            days_back (int): 加载多少天内的日志
            importance_filter (str): 重要性过滤器 (critical/high/normal/low)
        Returns:
            str: 操作日志内容
        """
        if not self.log_file.exists():
            return "无操作日志记录"
            
        cutoff_time = datetime.now() - timedelta(days=days_back)
        relevant_logs = []
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 按条目分割
        entries = content.split('## ')
        for entry in entries[1:]:
            if not entry.strip():
                continue
                
            try:
                # 提取时间戳
                timestamp_str = entry.split(' - ')[0]
                entry_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                
                # 检查是否在时间范围内
                if entry_time >= cutoff_time:
                    # 检查重要性过滤
                    if importance_filter:
                        if f'**重要性**: {importance_filter}' in entry:
                            relevant_logs.append(entry)
                    else:
                        relevant_logs.append(entry)
                        
            except ValueError:
                # 时间戳格式错误，跳过
                continue
                
        if not relevant_logs:
            return f"最近{days_back}天内无相关操作日志"
            
        return "## " + "## ".join(relevant_logs)
        
    def cleanup_old_logs(self):
        """清理过期的操作日志（保留重要日志）"""
        if not self.log_file.exists():
            return
            
        current_time = time.time()
        kept_logs = []
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        entries = content.split('## ')
        for entry in entries[1:]:
            if not entry.strip():
                continue
                
            try:
                timestamp_str = entry.split(' - ')[0]
                entry_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                entry_timestamp = entry_time.timestamp()
                
                # 检查重要性
                is_important = ('**重要性**: critical' in entry or 
                              '**重要性**: high' in entry)
                
                # 保留重要日志或1天内的日志
                if is_important or (current_time - entry_timestamp <= self.cleanup_threshold):
                    kept_logs.append(entry)
                else:
                    print(f"🧹 清理过期操作日志: {timestamp_str}")
                    
            except ValueError:
                # 时间戳格式错误，保留以防万一
                kept_logs.append(entry)
                
        # 重写日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            if kept_logs:
                f.write("## " + "## ".join(kept_logs))
                
        print(f"✅ 操作日志清理完成，保留 {len(kept_logs)} 条记录")
        
    def get_log_statistics(self):
        """获取日志统计信息"""
        if not self.log_file.exists():
            return "无操作日志"
            
        with open(self.log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        entries = content.split('## ')[1:]
        total_logs = len(entries)
        
        # 统计各类型操作
        operation_types = {}
        importance_levels = {"critical": 0, "high": 0, "normal": 0, "low": 0}
        
        for entry in entries:
            # 统计操作类型
            lines = entry.strip().split('\n')
            if lines:
                first_line = lines[0]
                op_type = first_line.split(' - ')[1].lower() if ' - ' in first_line else 'unknown'
                operation_types[op_type] = operation_types.get(op_type, 0) + 1
                
            # 统计重要性
            for level in importance_levels.keys():
                if f'**重要性**: {level}' in entry:
                    importance_levels[level] += 1
                    break
                    
        stats = f"""### 操作日志统计:
- 总记录数: {total_logs}
- 操作类型分布: {operation_types}
- 重要性分布: {importance_levels}
"""
        return stats

# 使用示例
if __name__ == "__main__":
    log_manager = OperationLogManager()
    
    # 记录操作日志
    log_manager.log_operation(
        "create",
        "创建了multi-memory-manager技能目录和相关文件",
        importance="high",
        file_path="/home/kousoyu/.openclaw/workspace/skills/multi-memory-manager/"
    )
    
    log_manager.log_operation(
        "code",
        "实现了core_memory.py模块，处理核心记忆管理",
        importance="normal",
        file_path="/home/kousoyu/.openclaw/workspace/skills/multi-memory-manager/core_memory.py"
    )
    
    # 加载最近7天的日志
    recent_logs = log_manager.load_operation_log(days_back=7)
    print("最近操作日志:")
    print(recent_logs)
    
    # 获取统计信息
    stats = log_manager.get_log_statistics()
    print("\n日志统计:")
    print(stats)
    
    # 清理过期日志
    log_manager.cleanup_old_logs()