#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多记忆管理器主模块
整合所有记忆管理组件，提供统一的接口
"""

import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.append(str(Path(__file__).parent))

from core_memory import CoreMemoryManager
from working_context import WorkingContextManager  
from logic_history import LogicHistoryManager
from operation_log import OperationLogManager
from task_recovery import TaskRecoveryManager

class MultiMemoryManager:
    def __init__(self, workspace_path="/home/kousoyu/.openclaw/workspace"):
        self.workspace_path = Path(workspace_path)
        self.core_memory = CoreMemoryManager(workspace_path)
        self.working_context = WorkingContextManager(workspace_path)
        self.logic_history = LogicHistoryManager(workspace_path)
        self.operation_log = OperationLogManager(workspace_path)
        self.task_recovery = TaskRecoveryManager(workspace_path)
        
    def initialize_memory_system(self):
        """初始化整个记忆系统"""
        print("🧠 初始化多记忆管理系统...")
        
        # 确保工作区目录存在
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        
        # 初始化各个组件
        self.core_memory.initialize_core_memory()
        print("✅ 核心记忆系统已初始化")
        
        # 记录初始化操作
        self.operation_log.log_operation(
            "system", 
            "多记忆管理系统初始化完成",
            importance="high"
        )
        
        print("🎉 多记忆管理系统初始化完成！")
        
    def save_core_instruction(self, instruction):
        """保存核心指令"""
        self.core_memory.save_core_instruction(instruction)
        self.operation_log.log_operation(
            "core_memory",
            f"保存核心指令: {instruction[:50]}...",
            importance="high"
        )
        
    def save_working_context(self, context, priority="normal"):
        """保存工作上下文"""
        self.working_context.save_context(context, priority)
        self.operation_log.log_operation(
            "working_context",
            f"保存工作上下文: {context[:50]}...",
            importance="normal"
        )
        
    def save_logic_history(self, topic, content, importance="medium"):
        """保存逻辑历史"""
        self.logic_history.save_logic_entry(topic, content, importance)
        self.operation_log.log_operation(
            "logic_history",
            f"保存逻辑历史 - {topic}: {content[:50]}...",
            importance="normal"
        )
        
    def log_operation(self, op_type, details, importance="normal", file_path=None):
        """记录操作日志"""
        self.operation_log.log_operation(op_type, details, importance, file_path)
        
    def save_task_state(self, description, data=None, priority="normal"):
        """保存任务状态"""
        task_id = self.task_recovery.save_task_state(description, data, priority)
        self.operation_log.log_operation(
            "task_recovery",
            f"保存任务状态: {description}",
            importance="high"
        )
        return task_id
        
    def complete_task(self, task_id):
        """完成任务"""
        self.task_recovery.complete_task(task_id)
        self.operation_log.log_operation(
            "task_recovery",
            f"完成任务: {task_id}",
            importance="high"
        )
        
    def cleanup_expired_memory(self):
        """清理过期的记忆"""
        print("🧹 清理过期记忆...")
        
        # 清理工作上下文（3天过期）
        self.working_context.cleanup_expired()
        
        # 清理操作日志（1天过期，保留重要日志）
        self.operation_log.cleanup_old_logs()
        
        # 优化逻辑历史（可选）
        # self.logic_history.optimize_history()
        
        print("✅ 过期记忆清理完成")
        
    def get_memory_summary(self):
        """获取所有记忆的摘要"""
        summary = "### 多记忆管理系统摘要\n\n"
        
        # 核心记忆摘要
        core_summary = self.core_memory.get_core_summary()
        summary += f"**核心记忆**:\n{core_summary}\n\n"
        
        # 工作上下文摘要  
        context_summary = self.working_context.get_context_summary()
        summary += f"**工作上下文**:\n{context_summary}\n\n"
        
        # 逻辑历史摘要
        logic_summary = self.logic_history.get_optimization_summary()
        summary += f"**逻辑历史**:\n{logic_summary}\n\n"
        
        # 操作日志统计
        log_stats = self.operation_log.get_log_statistics()
        summary += f"**操作日志**:\n{log_stats}\n\n"
        
        # 任务恢复摘要
        task_summary = self.task_recovery.get_recovery_summary()
        summary += f"**活动任务**:\n{task_summary}\n\n"
        
        return summary
        
    def load_startup_memory(self):
        """启动时加载关键记忆"""
        print("🚀 启动时加载关键记忆...")
        
        # 加载核心记忆（最高优先级）
        core_memory = self.core_memory.load_core_memory()
        print("✅ 核心记忆已加载")
        
        # 检查活动任务（最高优先级）
        active_tasks = self.task_recovery.load_active_tasks()
        if active_tasks:
            print(f"⚠️  发现 {len(active_tasks)} 个活动任务需要恢复")
            
        # 加载工作上下文（高优先级）
        working_context = self.working_context.load_context()
        print("✅ 工作上下文已加载")
        
        return {
            'core_memory': core_memory,
            'active_tasks': active_tasks,
            'working_context': working_context
        }

# 命令行接口
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='多记忆管理系统')
    parser.add_argument('command', choices=[
        'init', 'core', 'context', 'logic', 'log', 'task', 'cleanup', 'summary', 'startup'
    ], help='命令类型')
    parser.add_argument('--content', '-c', help='内容')
    parser.add_argument('--topic', '-t', help='主题（用于逻辑历史）')
    parser.add_argument('--importance', '-i', default='normal', 
                       choices=['critical', 'high', 'medium', 'low', 'normal'],
                       help='重要性级别')
    parser.add_argument('--priority', '-p', default='normal',
                       choices=['high', 'normal', 'low'],
                       help='优先级（用于上下文和任务）')
    parser.add_argument('--task-id', help='任务ID（用于完成任务）')
    parser.add_argument('--file-path', help='文件路径（用于操作日志）')
    
    args = parser.parse_args()
    
    manager = MultiMemoryManager()
    
    if args.command == 'init':
        manager.initialize_memory_system()
        
    elif args.command == 'core':
        if not args.content:
            print("错误: 需要提供 --content 参数")
            return
        manager.save_core_instruction(args.content)
        
    elif args.command == 'context':
        if not args.content:
            print("错误: 需要提供 --content 参数")
            return
        manager.save_working_context(args.content, args.priority)
        
    elif args.command == 'logic':
        if not args.content or not args.topic:
            print("错误: 需要提供 --content 和 --topic 参数")
            return
        manager.save_logic_history(args.topic, args.content, args.importance)
        
    elif args.command == 'log':
        if not args.content:
            print("错误: 需要提供 --content 参数")
            return
        manager.log_operation(args.importance, args.content, args.importance, args.file_path)
        
    elif args.command == 'task':
        if args.task_id:
            # 完成任务
            manager.complete_task(args.task_id)
        else:
            # 保存新任务
            if not args.content:
                print("错误: 需要提供 --content 参数或 --task-id 参数")
                return
            task_id = manager.save_task_state(args.content, priority=args.priority)
            print(f"任务ID: {task_id}")
            
    elif args.command == 'cleanup':
        manager.cleanup_expired_memory()
        
    elif args.command == 'summary':
        summary = manager.get_memory_summary()
        print(summary)
        
    elif args.command == 'startup':
        startup_data = manager.load_startup_memory()
        print("启动记忆加载完成")

if __name__ == "__main__":
    main()