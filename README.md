# GitHub Sentinel

GitHub 仓库更新监控工具，支持多仓库订阅、自动生成日报和 AI 摘要。

## 最近更新

### 2024-01 新增功能
- 添加了基于 Gradio 的 Web 界面，提供友好的图形化操作
- 支持时间范围查询，可生成指定时间段的更新报告
- 新增仓库订阅管理界面，支持可视化添加/删除订阅
- 优化了报告展示，支持查看历史报告列表
- 改进了 AI 摘要生成，支持多时间段的内容总结

## 功能特点

- 多仓库订阅管理
- GitHub 更新自动监控
- AI 驱动的更新内容摘要
- 美观的 Web 操作界面
- 灵活的时间范围查询
- Markdown 格式报告导出

## 使用方法

### Web 界面使用（推荐）

1. 启动 Web 服务：
```bash
python src/gradio_server.py
```

2. 访问界面：
- 打开浏览器访问 `http://localhost:7860`
- 默认端口为 7860，可在启动时通过参数修改

3. Report 功能：
   - 选择要查看的仓库
   - 设置查询时间：
     - Since Date：开始日期（必填）
     - Until Date：结束日期（可选，留空则只查看单天）
   - 点击 "Generate Report" 生成报告
   - 报告列表显示在左侧，可点击查看历史报告
   - 使用 "Refresh List" 刷新报告列表
   - "Reset" 按钮可重置所有输入

4. RepoLib 功能：
   - 添加仓库：
     - 在输入框中输入仓库地址（格式：owner/repo）
     - 点击 "Add Repository" 添加
   - 删除仓库：
     - 从下拉框选择要删除的仓库
     - 点击 "Remove Repository" 删除
   - 右侧可查看当前订阅的仓库列表

### 命令行使用

1. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Configure the application by editing `config.json`.

3. Run the application:
    ```sh
    python src/main.py
    ```

## Configuration
The configuration file `config.json` should contain the following settings:
```json
{
    "github_token": "your_github_token",
    "notification_settings": {
        "email": "your_email@example.com",
        "slack_webhook_url": "your_slack_webhook_url"
    },
    "subscriptions_file": "subscriptions.json",
    "update_interval": 86400
}
```

## 依赖安装

```bash
pip install -r requirements.txt
```

主要依赖：
- gradio：Web 界面框架
- openai：AI 摘要生成
- PyGithub：GitHub API 调用
- python-dotenv：环境变量管理
[其他依赖...]

## 注意事项

1. 首次使用需要配置：
   - GitHub Token
   - OpenAI API Key（用于 AI 摘要）
   - 订阅仓库列表

2. Web 界面特性：
   - 支持 emoji 和 markdown 链接的正确显示
   - 报告内容自动滚动
   - 响应式布局适配

3. 时间范围查询：
   - 单天查询：只填写 Since Date
   - 时间段查询：同时填写 Since Date 和 Until Date
   - 日期格式：YYYY-MM-DD

## 常见问题

1. 如何修改服务端口？
   - 修改 `gradio_server.py` 中的 `server_port` 参数

2. 如何允许外部访问？
   - 默认监听 0.0.0.0，允许外部访问
   - 确保防火墙允许对应端口访问

3. 报告未显示？
   - 检查日期格式是否正确
   - 确认选择的时间范围内是否有更新
   - 查看控制台是否有错误信息

## 贡献指南

[原有的贡献指南保持不变...]

## 许可证

[原有的许可证信息保持不变...]
