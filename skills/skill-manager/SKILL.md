# Skill Manager

方便查询和管理已安装的skills，按功能分类展示，提供简洁易懂的功能介绍。

## 使用方法

- `/skills` - 显示所有技能分类列表
- `/skills <category>` - 显示特定分类下的技能详情
- `/skills search <keyword>` - 按关键词搜索技能

## 技能分类

### 🔒 系统安全与审计
保护系统安全、数据备份和健康检查
- **healthcheck**: 主机安全加固和风险评估配置
- **backup**: 文件、目录和系统配置的完整备份恢复功能

### 💻 开发与代码管理  
GitHub集成、代码审查和开发工作流
- **github**: 通过gh CLI进行GitHub操作（issues、PRs、CI等）
- **gh-issues**: 自动获取GitHub issues并创建修复PR
- **coding-agent**: 高级编程代理，支持复杂编码任务
- **vercel-react-best-practices**: React/Next.js性能优化最佳实践

### 🎵 多媒体与娱乐
音频、视频和图像处理
- **sonoscli**: 控制Sonos音箱（发现/状态/播放/音量/分组）
- **spotify-player**: Spotify音乐播放控制
- **songsee**: 音乐识别和信息查询
- **video-frames**: 视频帧提取和处理
- **openai-image-gen**: OpenAI图像生成

### 💬 通信与消息
跨平台消息和通信工具
- **discord**: Discord消息和频道管理
- **slack**: Slack工作区集成
- **wacli**: WhatsApp命令行客户端
- **imsg**: iMessage消息发送
- **bluebubbles**: BlueBubbles服务器集成
- **voice-call**: 语音通话功能

### 📝 生产力工具
笔记、任务管理和密码管理
- **notion**: Notion页面和数据库操作
- **obsidian**: Obsidian笔记管理
- **bear-notes**: Bear笔记应用集成
- **apple-notes**: Apple Notes访问
- **apple-reminders**: Apple提醒事项管理
- **things-mac**: Things 3任务管理
- **trello**: Trello看板管理
- **1password**: 1Password密码管理

### 🤖 智能助手功能
实用工具和信息查询
- **weather**: 天气和预报查询（wttr.in/Open-Meteo）
- **gog**: GOG游戏库查询
- **goplaces**: Google Places地点搜索
- **oracle**: 决策建议和占卜
- **summarize**: 文本摘要生成
- **peekaboo**: 快速预览工具
- **gifgrep**: GIF搜索
- **xurl**: URL缩短和管理
- **blogwatcher**: 博客监控和更新通知

### 🏠 硬件与设备控制
智能家居和硬件设备管理
- **openhue**: Philips Hue灯光控制
- **eightctl**: Eight Sleep床垫控制
- **camsnap**: 摄像头快照和录制
- **camera**: 节点摄像头控制（通过nodes工具）

### 🧠 AI与模型工具
AI模型和语音处理
- **model-usage**: 模型使用统计和监控
- **openai-whisper**: 本地Whisper语音转文字
- **openai-whisper-api**: OpenAI Whisper API集成
- **sag**: ElevenLabs TTS语音合成
- **sherpa-onnx-tts**: 本地TTS语音合成
- **nano-banana-pro**: Nano Banana Pro模型集成

### 📁 文件与数据处理
文件管理和数据处理
- **file-maintenance**: 文件维护和清理
- **planning-with-files**: 基于文件的规划和组织
- **nano-pdf**: PDF文档处理
- **ordercli**: 订单管理工具

### 🛠️ 技能管理与发现
技能创建、发现和管理
- **skill-creator**: 创建和更新AgentSkills
- **find-skills**: 发现和安装新技能
- **clawhub**: ClawHub技能市场集成

### ⚙️ 系统工具
终端和系统管理
- **tmux**: Tmux会话管理
- **session-logs**: 会话日志管理
- **mcporter**: Minecraft服务器管理
- **himalaya**: Himalaya邮件客户端集成

## 快速查询示例

- 查看所有分类：`/skills`
- 查看多媒体技能：`/skills 多媒体`
- 搜索天气相关：`/skills search 天气`

每个技能都提供简明扼要的功能描述，帮助用户快速了解用途和适用场景。