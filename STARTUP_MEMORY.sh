#!/bin/bash
# 启动时自动加载多记忆管理系统

echo "🚀 加载多记忆管理系统..."

# 检查技能是否存在
if [ -f "/home/kousoyu/.openclaw/workspace/skills/multi-memory-manager/memory-startup" ]; then
    # 加载启动记忆
    /home/kousoyu/.openclaw/workspace/skills/multi-memory-manager/memory-startup
    
    # 将技能目录添加到PATH（如果需要）
    export PATH="$PATH:/home/kousoyu/.openclaw/workspace/skills/multi-memory-manager"
    
    echo "✅ 多记忆管理系统已加载"
else
    echo "⚠️  多记忆管理系统未找到，跳过加载"
fi