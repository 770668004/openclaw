#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能审计模块 - 严格的安全和逻辑审计
"""

import os
import json
import hashlib
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class SkillAuditor:
    """技能审计器 - 负责对技能进行安全性和逻辑性审计"""
    
    def __init__(self):
        self.security_rules = {
            'forbidden_patterns': [
                r'rm\s+-rf',  # 禁止危险的删除命令
                r'sudo\s+.*',  # 需要谨慎处理的sudo命令
                r'eval\s*\(.*\)',  # 禁止eval
                r'exec\s*\(.*\)',  # 禁止动态执行
                r'os\.system\s*\(.*\)',  # 禁止系统命令执行
            ],
            'required_patterns': [
                r'# Security:',  # 必须包含安全说明
                r'# When to Use',  # 必须包含使用场景
                r'# When NOT to Use',  # 必须包含禁止使用场景
            ],
            'sensitive_operations': [
                'file_write', 'network_request', 'system_command',
                'credential_access', 'data_modification'
            ]
        }
        
    def audit_skill_file(self, skill_path: str) -> Dict[str, any]:
        """
        审计单个技能文件
        
        Args:
            skill_path: 技能文件路径
            
        Returns:
            审计结果字典
        """
        audit_result = {
            'skill_name': os.path.basename(os.path.dirname(skill_path)),
            'file_path': skill_path,
            'security_score': 0,
            'logic_score': 0,
            'issues': [],
            'recommendations': [],
            'is_safe_to_upgrade': False,
            'audit_timestamp': datetime.now().isoformat()
        }
        
        try:
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 安全性审计
            security_issues = self._check_security_violations(content)
            audit_result['issues'].extend(security_issues)
            
            # 逻辑性审计
            logic_issues = self._check_logic_consistency(content)
            audit_result['issues'].extend(logic_issues)
            
            # 计算评分
            audit_result['security_score'] = max(0, 100 - len(security_issues) * 10)
            audit_result['logic_score'] = max(0, 100 - len(logic_issues) * 10)
            
            # 生成建议
            audit_result['recommendations'] = self._generate_recommendations(
                security_issues, logic_issues
            )
            
            # 判断是否安全升级
            audit_result['is_safe_to_upgrade'] = (
                audit_result['security_score'] >= 80 and 
                audit_result['logic_score'] >= 70 and
                not any('critical' in issue.get('severity', '') for issue in audit_result['issues'])
            )
            
        except Exception as e:
            audit_result['issues'].append({
                'type': 'file_error',
                'severity': 'critical',
                'message': f'无法读取技能文件: {str(e)}'
            })
            
        return audit_result
    
    def _check_security_violations(self, content: str) -> List[Dict[str, any]]:
        """检查安全违规"""
        issues = []
        
        # 检查禁止模式
        for pattern in self.security_rules['forbidden_patterns']:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                issues.append({
                    'type': 'forbidden_pattern',
                    'severity': 'critical' if 'rm -rf' in pattern else 'high',
                    'message': f'发现禁止的模式: {match.group()}',
                    'line_number': content[:match.start()].count('\n') + 1
                })
        
        # 检查必需模式
        for pattern in self.security_rules['required_patterns']:
            if not re.search(pattern, content, re.IGNORECASE):
                issues.append({
                    'type': 'missing_required_pattern',
                    'severity': 'medium',
                    'message': f'缺少必需的安全文档: {pattern}'
                })
        
        # 检查敏感操作
        sensitive_ops = self._detect_sensitive_operations(content)
        for op in sensitive_ops:
            issues.append({
                'type': 'sensitive_operation',
                'severity': 'medium',
                'message': f'检测到敏感操作: {op}',
                'requires_confirmation': True
            })
            
        return issues
    
    def _check_logic_consistency(self, content: str) -> List[Dict[str, any]]:
        """检查逻辑一致性"""
        issues = []
        
        # 检查描述完整性
        if 'description:' not in content:
            issues.append({
                'type': 'missing_description',
                'severity': 'high',
                'message': '技能缺少描述字段'
            })
        
        # 检查功能说明
        if '## When to Use' not in content or '## When NOT to Use' not in content:
            issues.append({
                'type': 'incomplete_usage_guide',
                'severity': 'medium',
                'message': '使用指南不完整，缺少使用场景或禁止场景说明'
            })
        
        # 检查代码示例
        if '```' not in content:
            issues.append({
                'type': 'missing_examples',
                'severity': 'low',
                'message': '缺少使用示例'
            })
        
        return issues
    
    def _detect_sensitive_operations(self, content: str) -> List[str]:
        """检测敏感操作"""
        detected_ops = []
        
        # 文件写入操作
        if re.search(r'(write|create|overwrite).*file', content, re.IGNORECASE):
            detected_ops.append('file_write')
            
        # 网络请求
        if re.search(r'(curl|wget|http|fetch|request)', content, re.IGNORECASE):
            detected_ops.append('network_request')
            
        # 系统命令
        if re.search(r'(bash|sh|command|exec)', content, re.IGNORECASE):
            detected_ops.append('system_command')
            
        # 凭据访问
        if re.search(r'(password|token|key|credential|auth)', content, re.IGNORECASE):
            detected_ops.append('credential_access')
            
        # 数据修改
        if re.search(r'(edit|modify|delete|remove|update)', content, re.IGNORECASE):
            detected_ops.append('data_modification')
            
        return detected_ops
    
    def _generate_recommendations(self, security_issues: List, logic_issues: List) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 安全建议
        critical_issues = [i for i in security_issues if i.get('severity') == 'critical']
        if critical_issues:
            recommendations.append("🚨 立即修复关键安全问题，特别是禁止的危险命令模式")
            
        high_issues = [i for i in security_issues if i.get('severity') == 'high']
        if high_issues:
            recommendations.append("⚠️ 修复高风险安全问题，确保用户数据安全")
            
        # 逻辑建议
        if any(i.get('severity') == 'high' for i in logic_issues):
            recommendations.append("📋 完善技能文档，确保使用场景描述清晰")
            
        # 通用建议
        if len(security_issues) + len(logic_issues) > 0:
            recommendations.append("🔍 建议进行全面代码审查，确保技能质量和安全性")
            
        return recommendations

def calculate_file_hash(file_path: str) -> str:
    """计算文件哈希值用于版本比较"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def compare_skill_versions(old_path: str, new_path: str) -> Dict[str, any]:
    """比较技能版本差异"""
    old_hash = calculate_file_hash(old_path)
    new_hash = calculate_file_hash(new_path)
    
    return {
        'hash_changed': old_hash != new_hash,
        'old_hash': old_hash,
        'new_hash': new_hash,
        'timestamp': datetime.now().isoformat()
    }