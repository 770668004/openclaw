#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
逻辑历史管理模块
处理聊天逻辑摘要、重点优化记录，长期保存并定期优化整理
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
import re

class LogicHistoryManager:
    def __init__(self, workspace_path="/home/kousoyu/.openclaw/workspace"):
        self.workspace_path = Path(workspace_path)
        self.history_file = self.workspace_path / "LOGIC_HISTORY.md"
        self.optimization_interval = 7 * 24 * 3600  # 7天优化一次
        
    def save_logic_entry(self, topic, logic_content, importance="medium"):
        """
        保存逻辑历史条目
        Args:
            topic (str): 话题/主题
            logic_content (str): 逻辑内容
            importance (str): 重要性 (high/medium/low)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 提取关键点
        key_points = self._extract_key_points(logic_content)
        
        entry = f"""## {topic} - {timestamp}
**重要性**: {importance}
**关键点**: {key_points}

{logic_content}

---
"""
        
        # 追加到文件
        with open(self.history_file, 'a', encoding='utf-8') as f:
            f.write(entry)
            
        print(f"✅ 逻辑历史已保存到 {self.history_file}")
        
    def _extract_key_points(self, content):
        """从内容中提取关键点"""
        # 简单的关键点提取逻辑
        sentences = re.split(r'[。！？.!?]', content)
        key_sentences = []
        
        # 寻找包含关键词的句子
        keywords = ['记住', '重要', '必须', '应该', '不要', '需要', '偏好', '喜欢']
        for sentence in sentences[:5]:  # 只检查前5句
            if any(keyword in sentence for keyword in keywords):
                key_sentences.append(sentence.strip())
                
        if not key_sentences and sentences:
            # 如果没有找到关键词，取第一句
            key_sentences.append(sentences[0].strip())
            
        return "; ".join(key_sentences[:2])  # 最多返回2个关键点
        
    def load_logic_history(self, topic_filter=None):
        """
        加载逻辑历史
        Args:
            topic_filter (str): 可选的主题过滤器
        Returns:
            str: 逻辑历史内容
        """
        if not self.history_file.exists():
            return ""
            
        with open(self.history_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if not topic_filter:
            return content
            
        # 按条目分割
        entries = content.split('## ')
        filtered_entries = []
        
        for entry in entries[1:]:
            if topic_filter.lower() in entry.lower():
                filtered_entries.append(entry)
                
        if filtered_entries:
            return "## " + "## ".join(filtered_entries)
        else:
            return f"未找到与 '{topic_filter}' 相关的逻辑历史"
            
    def get_optimization_summary(self):
        """获取优化摘要"""
        if not self.history_file.exists():
            return "无逻辑历史记录"
            
        with open(self.history_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 统计条目数量
        entries = content.split('## ')[1:]
        total_entries = len(entries)
        
        # 统计重要性分布
        high_count = content.count('**重要性**: high')
        medium_count = content.count('**重要性**: medium')
        low_count = content.count('**重要性**: low')
        
        # 提取最近的重要条目
        recent_high_entries = []
        for entry in entries[-5:]:  # 最近5个条目
            if '**重要性**: high' in entry:
                lines = entry.strip().split('\n')
                if lines:
                    topic_timestamp = lines[0]
                    recent_high_entries.append(topic_timestamp)
                    
        summary = f"""### 逻辑历史统计:
- 总条目数: {total_entries}
- 高重要性: {high_count}
- 中重要性: {medium_count}  
- 低重要性: {low_count}

### 最近高重要性条目:
"""
        for entry in recent_high_entries[-3:]:
            summary += f"- {entry}\n"
            
        return summary
        
    def optimize_history(self):
        """优化历史记录，合并重复条目，清理冗余内容"""
        if not self.history_file.exists():
            return
            
        with open(self.history_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 这里可以实现更复杂的优化逻辑
        # 目前先做简单的去重和格式化
        
        entries = content.split('---\n')
        unique_entries = []
        seen_topics = set()
        
        for entry in entries:
            if not entry.strip():
                continue
                
            # 提取主题
            topic_match = re.search(r'## ([^-\n]+)', entry)
            if topic_match:
                topic = topic_match.group(1).strip()
                if topic not in seen_topics:
                    seen_topics.add(topic)
                    unique_entries.append(entry)
            else:
                unique_entries.append(entry)
                
        # 重写文件
        optimized_content = '---\n'.join(unique_entries)
        if optimized_content and not optimized_content.endswith('---\n'):
            optimized_content += '---\n'
            
        with open(self.history_file, 'w', encoding='utf-8') as f:
            f.write(optimized_content)
            
        print(f"✅ 逻辑历史优化完成，原始条目: {len(entries)}, 优化后: {len(unique_entries)}")

# 使用示例
if __name__ == "__main__":
    logic_manager = LogicHistoryManager()
    
    # 保存逻辑条目
    logic_manager.save_logic_entry(
        "记忆管理", 
        "用户要求将记忆分为多个文件类型，每个有特定用途和生命周期",
        importance="high"
    )
    
    # 加载历史
    history = logic_manager.load_logic_history("记忆管理")
    print("相关逻辑历史:")
    print(history)
    
    # 获取摘要
    summary = logic_manager.get_optimization_summary()
    print("\n优化摘要:")
    print(summary)
    
    # 执行优化
    logic_manager.optimize_history()