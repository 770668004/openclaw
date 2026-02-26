#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能进化管理系统 - Skill Evolution Manager

功能：
1. 自动分类现有技能到功能类别
2. 严格审计技能代码和逻辑
3. 智能升级和优化技能
4. 24小时周期性自我进化
5. 优先级管理（当前任务 > 进化任务）
"""

import os
import json
import yaml
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkillEvolutionManager:
    """技能进化管理器主类"""
    
    def __init__(self):
        self.skill_directories = [
            "~/.npm-global/lib/node_modules/openclaw/skills/",
            "~/.openclaw/workspace/skills/",
            "~/.agents/skills/"
        ]
        self.categories = {
            "安全与审计": ["healthcheck", "security", "audit", "firewall", "hardening"],
            "文件管理": ["backup", "file", "storage", "sync", "compress"],
            "开发工具": ["coding-agent", "github", "git", "code", "review", "testing"],
            "通信协作": ["message", "chat", "email", "notification", "voice-call"],
            "系统监控": ["status", "monitor", "performance", "resource", "health"],
            "数据处理": ["weather", "api", "fetch", "process", "transform"],
            "智能助手": ["find-skills", "skill-creator", "concise-output", "context-restore"],
            "设备控制": ["sonoscli", "camsnap", "blucli", "bluebubbles", "things-mac"]
        }
        self.audit_log = []
        self.evolution_history = []
        
    def discover_skills(self) -> Dict[str, Dict]:
        """发现所有已安装的技能"""
        skills = {}
        
        for skill_dir in self.skill_directories:
            expanded_dir = os.path.expanduser(skill_dir)
            if os.path.exists(expanded_dir):
                for item in os.listdir(expanded_dir):
                    skill_path = os.path.join(expanded_dir, item)
                    if os.path.isdir(skill_path):
                        skill_md_path = os.path.join(skill_path, "SKILL.md")
                        if os.path.exists(skill_md_path):
                            skill_info = self.parse_skill_md(skill_md_path)
                            if skill_info:
                                skills[skill_info['name']] = {
                                    'path': skill_path,
                                    'info': skill_info,
                                    'category': self.categorize_skill(skill_info['name'], skill_info.get('description', ''))
                                }
        
        return skills
    
    def parse_skill_md(self, skill_md_path: str) -> Optional[Dict]:
        """解析SKILL.md文件"""
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1]
                    try:
                        metadata = yaml.safe_load(yaml_content)
                        if isinstance(metadata, dict):
                            return metadata
                    except yaml.YAMLError:
                        pass
            
            # 如果没有YAML frontmatter，尝试从内容中提取
            lines = content.split('\n')
            name = None
            description = None
            
            for line in lines:
                if line.startswith('name:'):
                    name = line.replace('name:', '').strip().strip('"\'')
                elif line.startswith('description:'):
                    description = line.replace('description:', '').strip().strip('"\'')
            
            if name:
                return {'name': name, 'description': description or ''}
                
        except Exception as e:
            logger.error(f"解析技能文件失败 {skill_md_path}: {e}")
        
        return None
    
    def categorize_skill(self, skill_name: str, description: str) -> str:
        """将技能分类到功能类别"""
        skill_text = f"{skill_name} {description}".lower()
        
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in skill_text:
                    return category
        
        # 默认分类
        return "其他工具"
    
    def audit_skill(self, skill_name: str, skill_path: str) -> Dict:
        """严格审计技能代码和逻辑"""
        audit_result = {
            'skill_name': skill_name,
            'timestamp': datetime.now().isoformat(),
            'security_issues': [],
            'logic_issues': [],
            'performance_issues': [],
            'recommendations': [],
            'hash_before': None
        }
        
        try:
            # 计算技能目录的哈希值
            audit_result['hash_before'] = self.calculate_directory_hash(skill_path)
            
            # 安全审计
            security_issues = self.security_audit(skill_path)
            audit_result['security_issues'] = security_issues
            
            # 逻辑审计
            logic_issues = self.logic_audit(skill_path)
            audit_result['logic_issues'] = logic_issues
            
            # 性能审计
            performance_issues = self.performance_audit(skill_path)
            audit_result['performance_issues'] = performance_issues
            
            # 生成优化建议
            recommendations = self.generate_recommendations(
                security_issues, logic_issues, performance_issues
            )
            audit_result['recommendations'] = recommendations
            
        except Exception as e:
            logger.error(f"审计技能失败 {skill_name}: {e}")
            audit_result['error'] = str(e)
        
        return audit_result
    
    def calculate_directory_hash(self, directory: str) -> str:
        """计算目录的哈希值"""
        hash_md5 = hashlib.md5()
        for root, dirs, files in os.walk(directory):
            for file in sorted(files):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'rb') as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            hash_md5.update(chunk)
                except Exception:
                    continue
        return hash_md5.hexdigest()
    
    def security_audit(self, skill_path: str) -> List[str]:
        """安全审计"""
        issues = []
        
        # 检查敏感操作
        dangerous_patterns = [
            'rm -rf',
            'sudo',
            'chmod 777',
            'eval(',
            'exec(',
            'os.system('
        ]
        
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                if file.endswith(('.py', '.js', '.sh', '.md')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            for pattern in dangerous_patterns:
                                if pattern in content:
                                    issues.append(f"发现危险模式 '{pattern}' 在文件 {filepath}")
                    except Exception:
                        continue
        
        return issues
    
    def logic_audit(self, skill_path: str) -> List[str]:
        """逻辑审计"""
        issues = []
        
        # 检查SKILL.md是否存在
        skill_md_path = os.path.join(skill_path, "SKILL.md")
        if not os.path.exists(skill_md_path):
            issues.append("缺少SKILL.md文件")
        
        # 检查是否有实现文件
        has_implementation = False
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                if file.endswith(('.py', '.js', '.sh')) and file != "SKILL.md":
                    has_implementation = True
                    break
            if has_implementation:
                break
        
        if not has_implementation:
            issues.append("缺少实现文件")
        
        return issues
    
    def performance_audit(self, skill_path: str) -> List[str]:
        """性能审计"""
        issues = []
        
        # 检查文件大小
        total_size = 0
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    total_size += os.path.getsize(filepath)
                except Exception:
                    continue
        
        if total_size > 10 * 1024 * 1024:  # 10MB
            issues.append(f"技能目录过大 ({total_size / 1024 / 1024:.2f} MB)")
        
        return issues
    
    def generate_recommendations(self, security_issues: List[str], 
                               logic_issues: List[str], 
                               performance_issues: List[str]) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        if security_issues:
            recommendations.append("需要修复安全问题，避免使用危险操作")
        
        if logic_issues:
            recommendations.append("完善技能结构，确保包含必要的元数据和实现")
        
        if performance_issues:
            recommendations.append("优化技能大小，移除不必要的文件")
        
        if not (security_issues or logic_issues or performance_issues):
            recommendations.append("技能质量良好，可以考虑功能增强")
        
        return recommendations
    
    def evolve_skill(self, skill_name: str, skill_path: str, audit_result: Dict) -> bool:
        """进化升级技能"""
        try:
            # 创建备份
            backup_path = f"{skill_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            import shutil
            shutil.copytree(skill_path, backup_path)
            
            # 应用优化建议
            success = self.apply_optimizations(skill_path, audit_result['recommendations'])
            
            if success:
                # 验证升级后的技能
                new_hash = self.calculate_directory_hash(skill_path)
                if new_hash != audit_result['hash_before']:
                    self.evolution_history.append({
                        'skill_name': skill_name,
                        'timestamp': datetime.now().isoformat(),
                        'old_hash': audit_result['hash_before'],
                        'new_hash': new_hash,
                        'changes': audit_result['recommendations']
                    })
                    logger.info(f"技能 {skill_name} 升级成功")
                    return True
                else:
                    logger.warning(f"技能 {skill_name} 升级后无变化")
                    return False
            else:
                # 恢复备份
                shutil.rmtree(skill_path)
                shutil.move(backup_path, skill_path)
                logger.error(f"技能 {skill_name} 升级失败，已恢复备份")
                return False
                
        except Exception as e:
            logger.error(f"升级技能失败 {skill_name}: {e}")
            return False
    
    def apply_optimizations(self, skill_path: str, recommendations: List[str]) -> bool:
        """应用优化建议"""
        # 这里需要具体的优化逻辑，根据推荐内容进行修改
        # 目前先返回True作为占位符
        return True
    
    def run_evolution_cycle(self):
        """运行24小时进化周期"""
        logger.info("开始技能进化周期")
        
        # 发现所有技能
        skills = self.discover_skills()
        logger.info(f"发现 {len(skills)} 个技能")
        
        # 对每个技能进行审计和可能的升级
        for skill_name, skill_data in skills.items():
            logger.info(f"审计技能: {skill_name}")
            
            # 严格审计
            audit_result = self.audit_skill(skill_name, skill_data['path'])
            self.audit_log.append(audit_result)
            
            # 如果有严重问题或优化建议，考虑升级
            if (audit_result['security_issues'] or 
                audit_result['logic_issues'] or 
                len(audit_result['recommendations']) > 0):
                
                # 检查是否应该升级（基于时间、优先级等）
                if self.should_upgrade_skill(skill_name, audit_result):
                    logger.info(f"开始升级技能: {skill_name}")
                    success = self.evolve_skill(skill_name, skill_data['path'], audit_result)
                    if success:
                        logger.info(f"技能 {skill_name} 升级完成")
                    else:
                        logger.error(f"技能 {skill_name} 升级失败")
        
        logger.info("技能进化周期完成")
    
    def should_upgrade_skill(self, skill_name: str, audit_result: Dict) -> bool:
        """判断是否应该升级技能"""
        # 严重的安全问题必须立即修复
        if audit_result['security_issues']:
            return True
        
        # 逻辑问题也需要修复
        if audit_result['logic_issues']:
            return True
        
        # 其他情况根据配置决定
        # 这里可以添加更多智能判断逻辑
        return False
    
    def get_categorized_skills(self) -> Dict[str, List[Dict]]:
        """获取分类后的技能列表"""
        skills = self.discover_skills()
        categorized = {}
        
        for category in self.categories.keys():
            categorized[category] = []
        
        categorized["其他工具"] = []
        
        for skill_name, skill_data in skills.items():
            category = skill_data['category']
            if category not in categorized:
                categorized[category] = []
            
            categorized[category].append({
                'name': skill_name,
                'description': skill_data['info'].get('description', ''),
                'path': skill_data['path']
            })
        
        return categorized

def main():
    """主函数"""
    manager = SkillEvolutionManager()
    
    # 运行一次进化周期
    manager.run_evolution_cycle()
    
    # 输出分类结果
    categorized_skills = manager.get_categorized_skills()
    for category, skills in categorized_skills.items():
        if skills:
            print(f"\n{category} ({len(skills)} 个技能):")
            for skill in skills:
                print(f"  - {skill['name']}: {skill['description']}")

if __name__ == "__main__":
    main()