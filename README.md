# GitHubSentinel

GitHub 仓库更新监控和报告生成工具

## 最近更新

### 2024年1月
- 📧 新增邮件推送功能
  - 支持 HTML 邮件，自动渲染 Markdown 内容
  - SSL 加密连接确保安全性
  - 支持配置多个收件人
  - 可自定义邮件模板
- ⏰ 新增自动报告生成
  - 支持后台周期性自动拉取更新
  - 可配置更新检查间隔
  - 自动生成并发送报告
  - 错误重试机制确保稳定性

## 功能特性

- 📊 自动监控 GitHub 仓库更新
- 📝 生成结构化的更新报告
- 🤖 使用 GPT 生成更新摘要
- 📧 邮件通知功能
  - SSL 加密连接
  - Markdown 转 HTML 渲染
  - 支持多收件人配置
  - 自定义邮件模板
- ⚡ 自动化功能
  - 周期性检查更新
  - 自动生成报告
  - 自动发送邮件通知
  - 错误自动重试
- 🌐 Web 界面管理
- 🔒 安全的配置管理

## 快速开始

1. 克隆仓库并安装依赖：
```bash
git clone <repo-url>
cd GitHubSentinel
pip install -r requirements.txt
```

2. 配置环境变量（复制 `.env.example` 为 `.env` 并填写）：
```env
# GitHub配置
GITHUB_TOKEN=your_github_token

# OpenAI配置
OPENAI_API_KEY=your_openai_key
OPENAI_BASE_URL=your_openai_base_url

# 邮件配置
EMAIL_SMTP_SERVER=smtp.example.com
EMAIL_SMTP_PORT=465
EMAIL_SENDER=your_email@example.com
EMAIL_PASSWORD=your_email_password
# 多个收件人用逗号分隔
EMAIL_RECIPIENTS=recipient1@example.com,recipient2@example.com
```

3. 配置订阅（编辑 `subscriptions.json`）：
```json
[
    "owner/repo1",
    "owner/repo2"
]
```

4. 启动服务：
```bash
# 启动后台监控服务（自动拉取更新并发送邮件）
python src/main.py

# 或启动 Web 界面
python src/gradio_server.py
```

## 配置说明

### 基础配置
- `config.json`: 基本配置文件
  - `update_interval`: 更新检查间隔（秒）
  - `exports_config`: 导出配置
  - `notification_settings`: 通知设置
- `.env`: 环境变量配置
- `subscriptions.json`: 仓库订阅列表

### 邮件通知配置
- `EMAIL_SMTP_SERVER`: SMTP服务器地址
- `EMAIL_SMTP_PORT`: SMTP端口（默认465，SSL）
- `EMAIL_SENDER`: 发件人邮箱
- `EMAIL_PASSWORD`: 发件人密码
- `EMAIL_RECIPIENTS`: 收件人列表（逗号分隔）

### 自动化配置
- `update_interval`: 更新检查间隔（默认24小时）
- 错误重试：发生错误时自动等待1分钟后重试
- 支持后台运行：使用 nohup 或系统服务

## 使用说明

### 自动报告生成
- 程序会按配置的时间间隔自动检查更新
- 发现更新时自动生成报告
- 生成的报告会自动发送到配置的邮箱
- 同时保存在 exports 目录下

### 邮件通知
- 支持 HTML 格式，自动渲染 Markdown
- 包含仓库名称和时间信息
- 支持表情符号和链接
- 可通过环境变量配置多个收件人

## 注意事项

1. 确保 GitHub Token 具有足够的权限
2. OpenAI API 需要稳定的网络连接
3. 邮件服务器需要正确的 SSL 配置
4. 建议使用系统服务或 supervisor 确保程序持续运行
5. 定期检查日志文件了解运行状态

## 常见问题

1. 邮件发送失败？
   - 检查 SMTP 配置是否正确
   - 确认端口是否支持 SSL
   - 验证密码是否正确
   - 检查防火墙设置

2. 自动更新没有运行？
   - 检查程序是否在后台运行
   - 确认配置的时间间隔是否正确
   - 查看日志文件是否有错误信息

3. 如何修改更新频率？
   - 在 `config.json` 中修改 `update_interval` 值
   - 单位为秒，默认86400（24小时）
