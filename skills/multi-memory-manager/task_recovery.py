#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务恢复管理模块
处理正在执行的任务状态，用于网络中断恢复，任务完成后自动删除
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
import uuid

class TaskRecoveryManager:
    def __init__(self, workspace_path="/home/kousoyu/.openclaw/workspace"):
        self.workspace_path = Path(workspace_path)
        self.recovery_file = self.workspace_path / "TASK_RECOVERY.md"
        
    def save_task_state(self, task_description, task_data=None, priority="normal"):
        """
        保存任务状态
        Args:
            task_description (str): 任务描述
            task_data (dict): 任务相关数据（可选）
            priority (str): 任务优先级 (high/normal/low)
        Returns:
            str: 任务ID
        """
        task_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        task_entry = f"""## TASK_ID: {task_id}
**描述**: {task_description}
**优先级**: {priority}
**开始时间**: {timestamp}
**状态**: running

"""
        if task_data:
            task_entry += f"**数据**:\n```json\n{json.dumps(task_data, indent=2, ensure_ascii=False)}\n```\n\n"
            
        # 追加到恢复文件
        with open(self.recovery_file, 'a', encoding='utf-8') as f:
            f.write(task_entry)
            
        print(f"✅ 任务状态已保存 (ID: {task_id})")
        return task_id
        
    def load_active_tasks(self):
        """
        加载所有活动任务
        Returns:
            list: 活动任务列表
        """
        if not self.recovery_file.exists():
            return []
            
        with open(self.recovery_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if not content.strip():
            return []
            
        # 按任务分割
        task_entries = content.split('## TASK_ID: ')
        active_tasks = []
        
        for entry in task_entries[1:]:
            if not entry.strip():
                continue
                
            try:
                lines = entry.strip().split('\n')
                task_id = lines[0].strip()
                
                # 提取任务信息
                task_info = {
                    'task_id': task_id,
                    'description': '',
                    'priority': 'normal',
                    'start_time': '',
                    'status': 'running',
                    'data': None
                }
                
                for line in lines[1:]:
                    if line.startswith('**描述**: '):
                        task_info['description'] = line.replace('**描述**: ', '').strip()
                    elif line.startswith('**优先级**: '):
                        task_info['priority'] = line.replace('**优先级**: ', '').strip()
                    elif line.startswith('**开始时间**: '):
                        task_info['start_time'] = line.replace('**开始时间**: ', '').strip()
                    elif line.startswith('**状态**: '):
                        task_info['status'] = line.replace('**状态**: ', '').strip()
                    elif line.startswith('```json'):
                        # 提取JSON数据
                        json_start = entry.find('```json')
                        json_end = entry.find('```', json_start + 7)
                        if json_start != -1 and json_end != -1:
                            json_str = entry[json_start + 7:json_end]
                            try:
                                task_info['data'] = json.loads(json_str)
                            except json.JSONDecodeError:
                                task_info['data'] = None
                        break
                        
                if task_info['status'] == 'running':
                    active_tasks.append(task_info)
                    
            except Exception as e:
                print(f"⚠️ 解析任务条目时出错: {e}")
                continue
                
        return active_tasks
        
    def complete_task(self, task_id):
        """
        标记任务为完成并从恢复文件中移除
        Args:
            task_id (str): 任务ID
        """
        if not self.recovery_file.exists():
            return
            
        with open(self.recovery_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 查找并移除指定任务
        task_marker = f"## TASK_ID: {task_id}"
        if task_marker not in content:
            print(f"⚠️ 未找到任务ID: {task_id}")
            return
            
        # 分割内容
        parts = content.split(task_marker)
        if len(parts) < 2:
            return
            
        # 找到任务的完整内容（直到下一个任务或文件结束）
        remaining_content = parts[1]
        next_task_marker = "## TASK_ID: "
        if next_task_marker in remaining_content:
            task_content = remaining_content.split(next_task_marker)[0]
            new_content = parts[0] + remaining_content[len(task_content):]
        else:
            # 这是最后一个任务
            new_content = parts[0]
            
        # 写回文件
        with open(self.recovery_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"✅ 任务 {task_id} 已完成并从恢复文件中移除")
        
    def get_recovery_summary(self):
        """获取任务恢复摘要"""
        active_tasks = self.load_active_tasks()
        
        if not active_tasks:
            return "无活动任务"
            
        summary = f"### 活动任务摘要 ({len(active_tasks)} 个任务):\n"
        
        for task in active_tasks[:5]:  # 显示最多5个任务
            summary += f"- **{task['description']}**\n"
            summary += f"  ID: {task['task_id'][:8]}...\n"
            summary += f"  优先级: {task['priority']}, 开始时间: {task['start_time']}\n\n"
            
        if len(active_tasks) > 5:
            summary += f"... 还有 {len(active_tasks) - 5} 个任务\n"
            
        return summary
        
    def clear_all_tasks(self):
        """清除所有任务（谨慎使用）"""
        if self.recovery_file.exists():
            self.recovery_file.unlink()
            print("🧹 所有任务已清除")

# 使用示例
if __name__ == "__main__":
    recovery_manager = TaskRecoveryManager()
    
    # 保存任务状态
    task_id = recovery_manager.save_task_state(
        "创建多记忆管理系统技能",
        task_data={
            "skill_name": "multi-memory-manager",
            "components": ["core_memory", "working_context", "logic_history", "operation_log", "task_recovery"],
            "status": "in_progress"
        },
        priority="high"
    )
    
    # 加载活动任务
    active_tasks = recovery_manager.load_active_tasks()
    print("活动任务:")
    for task in active_tasks:
        print(f"- {task['description']} (ID: {task['task_id']})")
        
    # 获取摘要
    summary = recovery_manager.get_recovery_summary()
    print("\n任务摘要:")
    print(summary)
    
    # 完成任务
    recovery_manager.complete_task(task_id)