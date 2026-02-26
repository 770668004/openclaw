#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能进化管理器 - 调度模块
负责24小时执行周期的管理和任务优先级控制
"""

import os
import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EvolutionTask:
    """进化任务数据结构"""
    task_id: str
    skill_name: str
    category: str
    priority: int  # 0-10, 10为最高优先级
    status: str  # pending, running, completed, failed
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    execution_cycle: str  # 执行周期标识
    current_task_priority: int = 0  # 当前正在执行的任务优先级

class EvolutionScheduler:
    """技能进化调度器"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.scheduler_file = self.workspace_path / "evolution_scheduler.json"
        self.tasks: List[EvolutionTask] = []
        self.current_execution_cycle = ""
        self.load_scheduler_state()
        
    def load_scheduler_state(self):
        """加载调度器状态"""
        try:
            if self.scheduler_file.exists():
                with open(self.scheduler_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [EvolutionTask(**task) for task in data.get('tasks', [])]
                    self.current_execution_cycle = data.get('current_execution_cycle', '')
            else:
                self.initialize_scheduler()
        except Exception as e:
            logger.error(f"加载调度器状态失败: {e}")
            self.initialize_scheduler()
            
    def initialize_scheduler(self):
        """初始化调度器"""
        self.current_execution_cycle = self.get_current_cycle()
        self.tasks = []
        self.save_scheduler_state()
        
    def get_current_cycle(self) -> str:
        """获取当前执行周期（24小时为一个周期）"""
        now = datetime.now()
        cycle_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return cycle_start.strftime("%Y-%m-%d")
        
    def should_start_new_cycle(self) -> bool:
        """检查是否应该开始新的执行周期"""
        current_cycle = self.get_current_cycle()
        return current_cycle != self.current_execution_cycle
        
    def start_new_cycle(self):
        """开始新的执行周期"""
        if self.should_start_new_cycle():
            logger.info(f"开始新的执行周期: {self.get_current_cycle()}")
            self.current_execution_cycle = self.get_current_cycle()
            # 清理已完成的任务
            self.cleanup_completed_tasks()
            self.save_scheduler_state()
            
    def cleanup_completed_tasks(self):
        """清理已完成的任务"""
        self.tasks = [task for task in self.tasks if task.status not in ['completed', 'failed']]
        
    def create_evolution_task(self, skill_name: str, category: str, priority: int = 5) -> EvolutionTask:
        """创建进化任务"""
        task_id = f"evol_{int(time.time())}_{skill_name}"
        task = EvolutionTask(
            task_id=task_id,
            skill_name=skill_name,
            category=category,
            priority=priority,
            status='pending',
            created_at=datetime.now().isoformat(),
            execution_cycle=self.current_execution_cycle
        )
        self.tasks.append(task)
        self.save_scheduler_state()
        return task
        
    def can_execute_task(self, task_priority: int, current_task_priority: int = 0) -> bool:
        """
        检查是否可以执行任务
        执行期的优先级小于当时正在执行的任务
        """
        return task_priority <= current_task_priority
        
    def get_pending_tasks(self) -> List[EvolutionTask]:
        """获取待处理的任务"""
        return [task for task in self.tasks if task.status == 'pending']
        
    def get_running_tasks(self) -> List[EvolutionTask]:
        """获取正在运行的任务"""
        return [task for task in self.tasks if task.status == 'running']
        
    def update_task_status(self, task_id: str, status: str):
        """更新任务状态"""
        for task in self.tasks:
            if task.task_id == task_id:
                task.status = status
                if status == 'running':
                    task.started_at = datetime.now().isoformat()
                elif status in ['completed', 'failed']:
                    task.completed_at = datetime.now().isoformat()
                self.save_scheduler_state()
                break
                
    def save_scheduler_state(self):
        """保存调度器状态"""
        try:
            data = {
                'current_execution_cycle': self.current_execution_cycle,
                'tasks': [asdict(task) for task in self.tasks]
            }
            with open(self.scheduler_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存调度器状态失败: {e}")
            
    def get_execution_stats(self) -> Dict[str, Any]:
        """获取执行统计信息"""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t.status == 'completed'])
        failed_tasks = len([t for t in self.tasks if t.status == 'failed'])
        pending_tasks = len([t for t in self.tasks if t.status == 'pending'])
        running_tasks = len([t for t in self.tasks if t.status == 'running'])
        
        return {
            'current_cycle': self.current_execution_cycle,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'failed_tasks': failed_tasks,
            'pending_tasks': pending_tasks,
            'running_tasks': running_tasks,
            'success_rate': (completed_tasks / max(total_tasks, 1)) * 100
        }
        
    def pause_all_tasks(self):
        """暂停所有任务（用于紧急情况）"""
        for task in self.tasks:
            if task.status == 'running':
                task.status = 'paused'
        self.save_scheduler_state()
        logger.info("所有任务已暂停")
        
    def resume_all_tasks(self):
        """恢复所有任务"""
        for task in self.tasks:
            if task.status == 'paused':
                task.status = 'pending'
        self.save_scheduler_state()
        logger.info("所有任务已恢复")

# 全局调度器实例
_scheduler_instance = None

def get_scheduler(workspace_path: str = None) -> EvolutionScheduler:
    """获取全局调度器实例"""
    global _scheduler_instance
    if _scheduler_instance is None:
        if workspace_path is None:
            workspace_path = os.path.expanduser("~/.openclaw/workspace")
        _scheduler_instance = EvolutionScheduler(workspace_path)
    return _scheduler_instance

def main():
    """主函数 - 用于测试"""
    scheduler = get_scheduler()
    print("调度器状态:")
    print(json.dumps(scheduler.get_execution_stats(), indent=2, ensure_ascii=False))
    
if __name__ == "__main__":
    main()