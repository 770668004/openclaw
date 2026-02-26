#!/bin/bash

# Skill Evolution Manager - 初始化脚本
# 作者: Kousoyu
# 创建时间: 2026-02-26

set -e

echo "🚀 初始化技能进化管理系统..."

# 检查依赖
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 需要 Python 3"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "❌ 错误: 需要 Git"
    exit 1
fi

# 创建必要的目录
mkdir -p ~/.openclaw/skill-evolution/backup
mkdir -p ~/.openclaw/skill-evolution/logs
mkdir -p ~/.openclaw/skill-evolution/temp

# 设置权限
chmod +x /home/kousoyu/.openclaw/workspace/skills/skill-evolution-manager/evolution_manager.py

# 创建符号链接到全局命令（可选）
if [ ! -f ~/.local/bin/skill-evolve ]; then
    mkdir -p ~/.local/bin
    ln -sf /home/kousoyu/.openclaw/workspace/skills/skill-evolution-manager/evolution_manager.py ~/.local/bin/skill-evolve
    echo "✅ 已创建全局命令: skill-evolve"
fi

# 验证安装
echo "🔍 验证安装..."
python3 /home/kousoyu/.openclaw/workspace/skills/skill-evolution-manager/evolution_manager.py --version

echo "✅ 技能进化管理系统初始化完成！"
echo ""
echo "使用方法:"
echo "  skill-evolve --help                    # 查看帮助"
echo "  skill-evolve --audit                   # 审计所有技能"
echo "  skill-evolve --categorize              # 分类所有技能"
echo "  skill-evolve --evolve                  # 执行进化升级"
echo "  skill-evolve --schedule                # 设置24小时调度"
echo ""
echo "配置文件位置: ~/.openclaw/workspace/skills/skill-evolution-manager/config.json"