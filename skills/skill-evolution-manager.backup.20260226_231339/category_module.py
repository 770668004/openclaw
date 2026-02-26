#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能分类与整合模块
负责将62个现有技能按功能进行智能分类，并提供整合建议
"""

import os
import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class SkillInfo:
    """技能信息数据类"""
    name: str
    description: str
    path: str
    category: str = ""
    subcategory: str = ""
    complexity: str = "simple"  # simple, medium, complex
    security_level: str = "standard"  # standard, high, critical

class SkillCategorizer:
    """技能分类器"""
    
    def __init__(self):
        # 定义功能分类映射
        self.category_keywords = {
            "安全与审计": [
                "security", "audit", "hardening", "firewall", "ssh", 
                "encryption", "authentication", "authorization", "privacy",
                "compliance", "vulnerability", "penetration", "risk"
            ],
            "文件管理": [
                "file", "backup", "restore", "compress", "archive", 
                "sync", "transfer", "storage", "disk", "filesystem"
            ],
            "开发工具": [
                "coding", "code", "development", "programming", "build",
                "compile", "debug", "test", "lint", "refactor", "review"
            ],
            "系统管理": [
                "system", "os", "linux", "macos", "windows", "update",
                "package", "install", "configure", "monitor", "performance"
            ],
            "网络通信": [
                "network", "http", "api", "web", "browser", "fetch",
                "download", "upload", "websocket", "proxy", "dns"
            ],
            "数据处理": [
                "data", "json", "xml", "csv", "database", "query",
                "transform", "parse", "extract", "analyze", "process"
            ],
            "媒体处理": [
                "media", "image", "audio", "video", "canvas", "tts",
                "speech", "graphics", "render", "convert", "edit"
            ],
            "智能助手": [
                "agent", "skill", "memory", "workflow", "automation",
                "assistant", "chat", "conversation", "reasoning", "planning"
            ],
            "外部集成": [
                "github", "git", "discord", "telegram", "whatsapp",
                "slack", "email", "calendar", "weather", "sonos"
            ]
        }
        
        # 技能复杂度关键词
        self.complexity_keywords = {
            "complex": ["agent", "orchestration", "workflow", "automation", "ai"],
            "medium": ["api", "integration", "processing", "management"],
            "simple": ["read", "write", "fetch", "simple", "basic"]
        }
        
        # 安全级别关键词
        self.security_keywords = {
            "critical": ["security", "audit", "encryption", "authentication", "system"],
            "high": ["file", "network", "data", "external", "access"],
            "standard": ["media", "weather", "simple", "read", "display"]
        }
    
    def categorize_skill(self, skill_info: SkillInfo) -> Tuple[str, str]:
        """
        对技能进行分类
        
        Args:
            skill_info: 技能信息对象
            
        Returns:
            (主分类, 子分类) 元组
        """
        desc_lower = skill_info.description.lower()
        name_lower = skill_info.name.lower()
        combined_text = f"{name_lower} {desc_lower}"
        
        # 主分类匹配
        best_category = "智能助手"  # 默认分类
        best_score = 0
        
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in combined_text)
            if score > best_score:
                best_score = score
                best_category = category
        
        # 子分类（基于技能名称的细化）
        subcategory = self._get_subcategory(skill_info.name, best_category)
        
        return best_category, subcategory
    
    def _get_subcategory(self, skill_name: str, main_category: str) -> str:
        """获取子分类"""
        subcategories = {
            "安全与审计": ["系统安全", "网络安全", "数据安全", "合规审计"],
            "文件管理": ["备份恢复", "文件操作", "存储同步", "压缩归档"],
            "开发工具": ["代码生成", "代码审查", "测试工具", "构建部署"],
            "系统管理": ["系统监控", "配置管理", "更新维护", "性能优化"],
            "网络通信": ["HTTP客户端", "浏览器控制", "API集成", "网络工具"],
            "数据处理": ["数据解析", "数据转换", "数据库操作", "数据分析"],
            "媒体处理": ["图像处理", "音频处理", "视频处理", "文本转语音"],
            "智能助手": ["技能管理", "记忆系统", "工作流", "自动化"],
            "外部集成": ["GitHub集成", "消息平台", "IoT设备", "第三方API"]
        }
        
        if main_category in subcategories:
            # 简单的子分类逻辑（可以根据需要扩展）
            if "github" in skill_name.lower():
                return "GitHub集成"
            elif "backup" in skill_name.lower():
                return "备份恢复"
            elif "coding" in skill_name.lower():
                return "代码生成"
            elif "health" in skill_name.lower():
                return "系统安全"
            elif "weather" in skill_name.lower():
                return "第三方API"
            elif "sonos" in skill_name.lower():
                return "IoT设备"
            else:
                return subcategories[main_category][0]  # 返回第一个作为默认
        
        return "通用"
    
    def assess_complexity(self, skill_info: SkillInfo) -> str:
        """评估技能复杂度"""
        combined_text = f"{skill_info.name.lower()} {skill_info.description.lower()}"
        
        for complexity, keywords in self.complexity_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                return complexity
        
        return "simple"
    
    def assess_security_level(self, skill_info: SkillInfo) -> str:
        """评估安全级别"""
        combined_text = f"{skill_info.name.lower()} {skill_info.description.lower()}"
        
        for level, keywords in self.security_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                return level
        
        return "standard"

class SkillIntegrator:
    """技能整合器"""
    
    def __init__(self):
        self.categorizer = SkillCategorizer()
    
    def analyze_skills(self, skill_paths: List[str]) -> Dict[str, List[SkillInfo]]:
        """
        分析所有技能并进行分类
        
        Args:
            skill_paths: 技能目录路径列表
            
        Returns:
            按分类组织的技能字典
        """
        all_skills = []
        
        # 收集所有技能信息
        for skill_path in skill_paths:
            if os.path.exists(skill_path):
                skills = self._collect_skills_from_directory(skill_path)
                all_skills.extend(skills)
        
        # 分类和评估
        categorized_skills = {}
        for skill in all_skills:
            category, subcategory = self.categorizer.categorize_skill(skill)
            skill.category = category
            skill.subcategory = subcategory
            skill.complexity = self.categorizer.assess_complexity(skill)
            skill.security_level = self.categorizer.assess_security_level(skill)
            
            if category not in categorized_skills:
                categorized_skills[category] = []
            categorized_skills[category].append(skill)
        
        return categorized_skills
    
    def _collect_skills_from_directory(self, directory: str) -> List[SkillInfo]:
        """从目录收集技能信息"""
        skills = []
        
        if not os.path.exists(directory):
            return skills
        
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                skill_md_path = os.path.join(item_path, "SKILL.md")
                if os.path.exists(skill_md_path):
                    skill_info = self._parse_skill_md(skill_md_path)
                    if skill_info:
                        skills.append(skill_info)
        
        return skills
    
    def _parse_skill_md(self, file_path: str) -> Optional[SkillInfo]:
        """解析SKILL.md文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取YAML frontmatter
            if content.startswith('---'):
                end_marker = content.find('\n---', 3)
                if end_marker != -1:
                    yaml_content = content[3:end_marker]
                    lines = yaml_content.strip().split('\n')
                    
                    name = ""
                    description = ""
                    
                    for line in lines:
                        if line.startswith('name:'):
                            name = line[5:].strip().strip('"\'')
                        elif line.startswith('description:'):
                            description = line[12:].strip().strip('"\'')
                    
                    if name and description:
                        return SkillInfo(
                            name=name,
                            description=description,
                            path=file_path
                        )
            
            return None
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
    
    def generate_integration_recommendations(self, categorized_skills: Dict[str, List[SkillInfo]]) -> Dict[str, List[Dict]]:
        """
        生成技能整合建议
        
        Args:
            categorized_skills: 分类后的技能字典
            
        Returns:
            整合建议字典
        """
        recommendations = {}
        
        for category, skills in categorized_skills.items():
            # 按子分类分组
            subcategory_groups = {}
            for skill in skills:
                if skill.subcategory not in subcategory_groups:
                    subcategory_groups[skill.subcategory] = []
                subcategory_groups[skill.subcategory].append(skill)
            
            category_recommendations = []
            
            for subcategory, sub_skills in subcategory_groups.items():
                if len(sub_skills) > 1:
                    # 有多个相似技能，建议整合
                    recommendation = {
                        "type": "integration",
                        "subcategory": subcategory,
                        "skills": [s.name for s in sub_skills],
                        "description": f"建议将{subcategory}相关的{len(sub_skills)}个技能进行整合，减少重复代码，提高一致性",
                        "priority": self._calculate_integration_priority(sub_skills)
                    }
                    category_recommendations.append(recommendation)
                else:
                    # 单个技能，建议增强
                    skill = sub_skills[0]
                    recommendation = {
                        "type": "enhancement",
                        "subcategory": subcategory,
                        "skills": [skill.name],
                        "description": f"建议增强{skill.name}技能的功能，添加更多实用特性",
                        "priority": self._calculate_enhancement_priority(skill)
                    }
                    category_recommendations.append(recommendation)
            
            recommendations[category] = category_recommendations
        
        return recommendations
    
    def _calculate_integration_priority(self, skills: List[SkillInfo]) -> str:
        """计算整合优先级"""
        # 基于技能的安全级别和复杂度
        max_security = max(s.security_level for s in skills)
        max_complexity = max(s.complexity for s in skills)
        
        if max_security == "critical" or max_complexity == "complex":
            return "high"
        elif max_security == "high" or max_complexity == "medium":
            return "medium"
        else:
            return "low"
    
    def _calculate_enhancement_priority(self, skill: SkillInfo) -> str:
        """计算增强优先级"""
        if skill.security_level == "critical" or skill.complexity == "complex":
            return "high"
        elif skill.security_level == "high" or skill.complexity == "medium":
            return "medium"
        else:
            return "low"

def main():
    """主函数 - 用于测试"""
    integrator = SkillIntegrator()
    
    # 技能目录路径
    skill_directories = [
        "/home/kousoyu/.npm-global/lib/node_modules/openclaw/skills/",
        "/home/kousoyu/.openclaw/workspace/skills/",
        "/home/kousoyu/.agents/skills/"
    ]
    
    # 分析技能
    categorized_skills = integrator.analyze_skills(skill_directories)
    
    # 生成整合建议
    recommendations = integrator.generate_integration_recommendations(categorized_skills)
    
    # 输出结果
    print("=== 技能分类结果 ===")
    for category, skills in categorized_skills.items():
        print(f"\n{category} ({len(skills)}个技能):")
        for skill in skills:
            print(f"  - {skill.name} [{skill.subcategory}] - {skill.complexity}/{skill.security_level}")
    
    print("\n=== 整合建议 ===")
    for category, recs in recommendations.items():
        print(f"\n{category}:")
        for rec in recs:
            print(f"  - [{rec['priority']}] {rec['description']}")

if __name__ == "__main__":
    main()