#!/bin/bash

# Skill Manager - List and categorize installed skills
# Usage: list-skills [category] | list-skills --all | list-skills --search <keyword>

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print usage
print_usage() {
    echo "技能管理器 - 查询和管理已安装的技能"
    echo ""
    echo "用法:"
    echo "  list-skills                    # 显示所有技能分类概览"
    echo "  list-skills <分类名>          # 显示特定分类的技能详情"
    echo "  list-skills --all             # 显示所有技能的完整列表"
    echo "  list-skills --search <关键词>  # 搜索包含关键词的技能"
    echo ""
    echo "可用分类:"
    echo "  系统安全与审计 | 开发与代码管理 | 多媒体与娱乐 | 通信与消息"
    echo "  生产力工具 | 智能助手功能 | 硬件与设备控制 | AI与模型工具"
    echo "  文件与数据处理 | 技能管理与发现 | 系统工具"
}

# Function to get skill description from SKILL.md
get_skill_description() {
    local skill_dir="$1"
    local skill_name=$(basename "$skill_dir")
    
    if [ -f "$skill_dir/SKILL.md" ]; then
        # Extract description from frontmatter or first paragraph
        if grep -q "^description:" "$skill_dir/SKILL.md"; then
            grep "^description:" "$skill_dir/SKILL.md" | cut -d':' -f2- | sed 's/^ *//;s/ *$//;s/^"//;s/"$//'
        elif grep -q "^[[:space:]]*\"description\":" "$skill_dir/SKILL.md"; then
            grep "\"description\":" "$skill_dir/SKILL.md" | cut -d':' -f2- | sed 's/^ *//;s/ *$//;s/^"//;s/"$//'
        else
            # Try to get first non-empty line after title
            awk '/^#/{flag=1;next} flag && NF{print; exit}' "$skill_dir/SKILL.md" 2>/dev/null || echo "描述不可用"
        fi
    else
        echo "描述文件缺失"
    fi
}

# Function to list all skills by category
list_all_categories() {
    echo -e "${GREEN}=== 技能分类概览 ===${NC}"
    echo ""
    
    # System Security & Audit
    echo -e "${YELLOW}🔒 系统安全与审计${NC}"
    echo "   • healthcheck - 主机安全加固和风险评估"
    echo "   • backup - 文件、目录和系统配置的备份恢复"
    echo ""
    
    # Development & Code Management
    echo -e "${YELLOW}💻 开发与代码管理${NC}"
    echo "   • github - GitHub操作（issues、PRs、CI等）"
    echo "   • gh-issues - 自动处理GitHub issues并创建PR"
    echo "   • coding-agent - 代码生成和编程助手"
    echo "   • vercel-react-best-practices - React/Next.js性能优化"
    echo ""
    
    # Multimedia & Entertainment
    echo -e "${YELLOW}🎵 多媒体与娱乐${NC}"
    echo "   • sonoscli - 控制Sonos音箱"
    echo "   • spotify-player - Spotify播放控制"
    echo "   • songsee - 音乐识别和管理"
    echo "   • video-frames - 视频帧提取和处理"
    echo "   • openai-image-gen - AI图像生成"
    echo ""
    
    # Communication & Messaging
    echo -e "${YELLOW}💬 通信与消息${NC}"
    echo "   • discord - Discord集成"
    echo "   • slack - Slack集成"
    echo "   • wacli - WhatsApp命令行"
    echo "   • imsg - iMessage集成"
    echo "   • bluebubbles - BlueBubbles集成"
    echo "   • voice-call - 语音通话功能"
    echo ""
    
    # Productivity Tools
    echo -e "${YELLOW}📊 生产力工具${NC}"
    echo "   • notion - Notion集成"
    echo "   • obsidian - Obsidian笔记管理"
    echo "   • bear-notes - Bear笔记应用"
    echo "   • apple-notes - Apple备忘录"
    echo "   • apple-reminders - Apple提醒事项"
    echo "   • things-mac - Things 3任务管理"
    echo "   • trello - Trello项目管理"
    echo "   • 1password - 1Password密码管理"
    echo ""
    
    # Smart Assistant Features
    echo -e "${YELLOW}🤖 智能助手功能${NC}"
    echo "   • weather - 天气查询和预报"
    echo "   • gog - Google搜索"
    echo "   • goplaces - 地点搜索"
    echo "   • oracle - 预测和建议"
    echo "   • summarize - 内容摘要"
    echo "   • peekaboo - 快速预览"
    echo "   • gifgrep - GIF搜索"
    echo "   • xurl - URL处理"
    echo "   • blogwatcher - 博客监控"
    echo ""
    
    # Hardware & Device Control
    echo -e "${YELLOW}🔌 硬件与设备控制${NC}"
    echo "   • openhue - Philips Hue灯光控制"
    echo "   • eightctl - Eight Sleep床垫控制"
    echo "   • camsnap - 摄像头快照"
    echo ""
    
    # AI & Model Tools
    echo -e "${YELLOW}🧠 AI与模型工具${NC}"
    echo "   • model-usage - 模型使用统计"
    echo "   • openai-whisper - 本地Whisper语音识别"
    echo "   • openai-whisper-api - OpenAI Whisper API"
    echo "   • sag - ElevenLabs语音合成"
    echo "   • sherpa-onnx-tts - 本地TTS引擎"
    echo "   • nano-banana-pro - Banana Pro模型"
    echo ""
    
    # File & Data Processing
    echo -e "${YELLOW}📁 文件与数据处理${NC}"
    echo "   • file-maintenance - 文件维护和清理"
    echo "   • planning-with-files - 基于文件的规划"
    echo "   • nano-pdf - PDF处理"
    echo "   • ordercli - 订单管理"
    echo ""
    
    # Skill Management & Discovery
    echo -e "${YELLOW}🔧 技能管理与发现${NC}"
    echo "   • skill-creator - 创建和更新技能"
    echo "   • find-skills - 发现和安装新技能"
    echo "   • clawhub - ClawHub集成"
    echo ""
    
    # System Tools
    echo -e "${YELLOW}⚙️ 系统工具${NC}"
    echo "   • tmux - Tmux会话管理"
    echo "   • session-logs - 会话日志管理"
    echo "   • mcporter - Minecraft服务器管理"
    echo "   • himalaya - Himalaya邮件客户端"
    echo ""
    
    echo -e "${CYAN}总计: 58个技能，涵盖11个主要类别${NC}"
}

# Function to show specific category details
show_category_details() {
    local category="$1"
    
    case "$category" in
        "系统安全与审计")
            echo -e "${YELLOW}🔒 系统安全与审计${NC}"
            echo "保护系统安全，进行风险评估和数据备份"
            echo ""
            echo -e "${GREEN}• healthcheck${NC} - 主机安全加固和风险容忍度配置"
            echo "  用于安全审计、防火墙/SSH/更新加固、风险评估等"
            echo ""
            echo -e "${GREEN}• backup${NC} - 全面的备份和恢复功能"
            echo "  支持增量备份、压缩、加密和多存储目的地"
            ;;
        "开发与代码管理")
            echo -e "${YELLOW}💻 开发与代码管理${NC}"
            echo "代码开发、版本控制和项目管理相关功能"
            echo ""
            echo -e "${GREEN}• github${NC} - GitHub操作"
            echo "  通过gh CLI管理issues、PRs、CI运行、代码审查等"
            echo ""
            echo -e "${GREEN}• gh-issues${NC} - GitHub Issues自动化"
            echo "  自动获取issues，生成修复方案并创建PR"
            echo ""
            echo -e "${GREEN}• coding-agent${NC} - 编程助手"
            echo "  代码生成、调试和优化"
            echo ""
            echo -e "${GREEN}• vercel-react-best-practices${NC} - React性能优化"
            echo "  Vercel工程团队的React/Next.js最佳实践指南"
            ;;
        "多媒体与娱乐")
            echo -e "${YELLOW}🎵 多媒体与娱乐${NC}"
            echo "音频、视频和娱乐内容控制"
            echo ""
            echo -e "${GREEN}• sonoscli${NC} - Sonos音箱控制"
            echo "  发现、状态查看、播放控制、音量调节、分组管理"
            echo ""
            echo -e "${GREEN}• spotify-player${NC} - Spotify控制"
            echo "  播放、暂停、跳过、音量控制等"
            echo ""
            echo -e "${GREEN}• songsee${NC} - 音乐识别"
            echo "  音乐发现和管理"
            echo ""
            echo -e "${GREEN}• video-frames${NC} - 视频处理"
            echo "  视频帧提取和分析"
            echo ""
            echo -e "${GREEN}• openai-image-gen${NC} - AI图像生成"
            echo "  使用OpenAI DALL-E生成图像"
            ;;
        "通信与消息")
            echo -e "${YELLOW}💬 通信与消息${NC}"
            echo "各种消息平台和通信工具集成"
            echo ""
            echo -e "${GREEN}• discord${NC} - Discord集成"
            echo "  消息发送、频道管理、机器人控制"
            echo ""
            echo -e "${GREEN}• slack${NC} - Slack集成"
            echo "  工作区消息和通知"
            echo ""
            echo -e "${GREEN}• wacli${NC} - WhatsApp命令行"
            echo "  WhatsApp消息发送和接收"
            echo ""
            echo -e "${GREEN}• imsg${NC} - iMessage集成"
            echo "  Apple iMessage消息处理"
            echo ""
            echo -e "${GREEN}• bluebubbles${NC} - BlueBubbles集成"
            echo "  Android消息在Apple设备上的同步"
            echo ""
            echo -e "${GREEN}• voice-call${NC} - 语音通话"
            echo "  语音通话功能支持"
            ;;
        "生产力工具")
            echo -e "${YELLOW}📊 生产力工具${NC}"
            echo "笔记、任务管理和个人信息组织"
            echo ""
            echo -e "${GREEN}• notion${NC} - Notion集成"
            echo "  Notion页面和数据库操作"
            echo ""
            echo -e "${GREEN}• obsidian${NC} - Obsidian笔记"
            echo "  本地Markdown笔记管理"
            echo ""
            echo -e "${GREEN}• bear-notes${NC} - Bear笔记"
            echo "  Bear应用笔记同步"
            echo ""
            echo -e "${GREEN}• apple-notes${NC} - Apple备忘录"
            echo "  Apple备忘录访问和管理"
            echo ""
            echo -e "${GREEN}• apple-reminders${NC} - Apple提醒事项"
            echo "  提醒事项创建和管理"
            echo ""
            echo -e "${GREEN}• things-mac${NC} - Things 3"
            echo "  Things 3任务管理应用集成"
            echo ""
            echo -e "${GREEN}• trello${NC} - Trello"
            echo "  Trello看板和卡片管理"
            echo ""
            echo -e "${GREEN}• 1password${NC} - 1Password"
            echo "  密码和安全信息管理"
            ;;
        "智能助手功能")
            echo -e "${YELLOW}🤖 智能助手功能${NC}"
            echo "日常助手功能和信息查询"
            echo ""
            echo -e "${GREEN}• weather${NC} - 天气查询"
            echo "  当前天气和预报（wttr.in或Open-Meteo）"
            echo ""
            echo -e "${GREEN}• gog${NC} - Google搜索"
            echo "  Google搜索集成"
            echo ""
            echo -e "${GREEN}• goplaces${NC} - 地点搜索"
            echo "  地点和商家搜索"
            echo ""
            echo -e "${GREEN}• oracle${NC} - 预测建议"
            echo "  基于数据的预测和建议"
            echo ""
            echo -e "${GREEN}• summarize${NC} - 内容摘要"
            echo "  文本和内容摘要生成"
            echo ""
            echo -e "${GREEN}• peekaboo${NC} - 快速预览"
            echo "  快速内容预览功能"
            echo ""
            echo -e "${GREEN}• gifgrep${NC} - GIF搜索"
            echo "  GIF动画搜索"
            echo ""
            echo -e "${GREEN}• xurl${NC} - URL处理"
            echo "  URL分析和处理"
            echo ""
            echo -e "${GREEN}• blogwatcher${NC} - 博客监控"
            echo "  博客更新监控"
            ;;
        "硬件与设备控制")
            echo -e "${YELLOW}🔌 硬件与设备控制${NC}"
            echo "智能家居和硬件设备控制"
            echo ""
            echo -e "${GREEN}• openhue${NC} - Philips Hue"
            echo "  Philips Hue智能灯光控制"
            echo ""
            echo -e "${GREEN}• eightctl${NC} - Eight Sleep"
            echo "  Eight Sleep智能床垫控制"
            echo ""
            echo -e "${GREEN}• camsnap${NC} - 摄像头快照"
            echo "  摄像头截图和录制"
            ;;
        "AI与模型工具")
            echo -e "${YELLOW}🧠 AI与模型工具${NC}"
            echo "AI模型和机器学习相关工具"
            echo ""
            echo -e "${GREEN}• model-usage${NC} - 模型使用统计"
            echo "  跟踪和分析模型使用情况"
            echo ""
            echo -e "${GREEN}• openai-whisper${NC} - 本地Whisper"
            echo "  本地运行的Whisper语音识别"
            echo ""
            echo -e "${GREEN}• openai-whisper-api${NC} - OpenAI Whisper API"
            echo "  OpenAI Whisper API集成"
            echo ""
            echo -e "${GREEN}• sag${NC} - ElevenLabs TTS"
            echo "  ElevenLabs语音合成"
            echo ""
            echo -e "${GREEN}• sherpa-onnx-tts${NC} - 本地TTS"
            echo "  本地ONNX TTS引擎"
            echo ""
            echo -e "${GREEN}• nano-banana-pro${NC} - Banana Pro"
            echo "  Banana Pro模型集成"
            ;;
        "文件与数据处理")
            echo -e "${YELLOW}📁 文件与数据处理${NC}"
            echo "文件管理和数据处理功能"
            echo ""
            echo -e "${GREEN}• file-maintenance${NC} - 文件维护"
            echo "  文件清理、整理和维护"
            echo ""
            echo -e "${GREEN}• planning-with-files${NC} - 基于文件的规划"
            echo "  使用文件进行任务规划"
            echo ""
            echo -e "${GREEN}• nano-pdf${NC} - PDF处理"
            echo "  PDF文档处理和转换"
            echo ""
            echo -e "${GREEN}• ordercli${NC} - 订单管理"
            echo "  订单处理和管理"
            ;;
        "技能管理与发现")
            echo -e "${YELLOW}🔧 技能管理与发现${NC}"
            echo "技能创建、发现和管理"
            echo ""
            echo -e "${GREEN}• skill-creator${NC} - 技能创建"
            echo "  创建和更新AgentSkills"
            echo ""
            echo -e "${GREEN}• find-skills${NC} - 技能发现"
            echo "  帮助用户发现和安装新技能"
            echo ""
            echo -e "${GREEN}• clawhub${NC} - ClawHub集成"
            echo "  ClawHub技能市场集成"
            ;;
        "系统工具")
            echo -e "${YELLOW}⚙️ 系统工具${NC}"
            echo "系统级工具和实用程序"
            echo ""
            echo -e "${GREEN}• tmux${NC} - Tmux会话管理"
            echo "  Tmux终端复用器集成"
            echo ""
            echo -e "${GREEN}• session-logs${NC} - 会话日志"
            echo "  会话日志记录和管理"
            echo ""
            echo -e "${GREEN}• mcporter${NC} - Minecraft服务器"
            echo "  Minecraft服务器管理"
            echo ""
            echo -e "${GREEN}• himalaya${NC} - Himalaya邮件"
            echo "  Himalaya邮件客户端集成"
            ;;
        *)
            echo -e "${RED}错误: 未知分类 '$category'${NC}"
            echo ""
            echo "可用分类:"
            echo "  系统安全与审计 | 开发与代码管理 | 多媒体与娱乐 | 通信与消息"
            echo "  生产力工具 | 智能助手功能 | 硬件与设备控制 | AI与模型工具"
            echo "  文件与数据处理 | 技能管理与发现 | 系统工具"
            exit 1
            ;;
    esac
}

# Function to list all skills
list_all_skills() {
    echo -e "${GREEN}=== 所有已安装技能 (58个) ===${NC}"
    echo ""
    
    # Get all skill directories
    local skill_dirs=()
    while IFS= read -r dir; do
        skill_dirs+=("$dir")
    done < <(find ~/.npm-global/lib/node_modules/openclaw/skills ~/.openclaw/workspace/skills ~/.agents/skills -name "SKILL.md" -exec dirname {} \; 2>/dev/null | sort)
    
    for dir in "${skill_dirs[@]}"; do
        local skill_name=$(basename "$dir")
        local description=$(get_skill_description "$dir")
        echo -e "${GREEN}• $skill_name${NC} - $description"
    done
}

# Function to search skills
search_skills() {
    local keyword="$1"
    echo -e "${GREEN}=== 搜索 '$keyword' ===${NC}"
    echo ""
    
    local found=false
    local skill_dirs=()
    while IFS= read -r dir; do
        skill_dirs+=("$dir")
    done < <(find ~/.npm-global/lib/node_modules/openclaw/skills ~/.openclaw/workspace/skills ~/.agents/skills -name "SKILL.md" -exec dirname {} \; 2>/dev/null | sort)
    
    for dir in "${skill_dirs[@]}"; do
        local skill_name=$(basename "$dir")
        local description=$(get_skill_description "$dir")
        
        # Check if keyword matches skill name or description
        if [[ "$skill_name" == *"$keyword"* ]] || [[ "$description" == *"$keyword"* ]]; then
            echo -e "${GREEN}• $skill_name${NC} - $description"
            found=true
        fi
    done
    
    if [ "$found" = false ]; then
        echo "未找到包含 '$keyword' 的技能"
    fi
}

# Main logic
if [ $# -eq 0 ]; then
    list_all_categories
elif [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    print_usage
elif [ "$1" = "--all" ]; then
    list_all_skills
elif [ "$1" = "--search" ]; then
    if [ $# -lt 2 ]; then
        echo "错误: --search 需要指定关键词"
        exit 1
    fi
    search_skills "$2"
else
    # Assume it's a category name
    show_category_details "$1"
fi