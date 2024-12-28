import gradio as gr
from datetime import datetime, timedelta
from config import Config
from github_client import GitHubClient
from report_generator import ReportGenerator
from subscription_manager import SubscriptionManager
from llm import LLMProcessor
import os

class GradioUI:
    def __init__(self):
        """初始化Gradio UI"""
        self.config = Config()
        self.github_client = GitHubClient(self.config)
        self.report_generator = ReportGenerator(self.config)
        self.subscription_manager = SubscriptionManager(self.config.subscriptions_file)
        self.llm_processor = LLMProcessor(self.config)

    def load_subscriptions(self) -> list:
        """加载订阅列表"""
        return self.subscription_manager.get_subscriptions()

    def generate_report(self, repo: str, date: str, until_date: str = None) -> tuple[str, list]:
        """生成报告
        
        Returns:
            tuple[str, list]: (报告内容, 更新后的文件列表)
        """
        try:
            # 验证开始日期格式
            report_date = datetime.strptime(date, '%Y-%m-%d')
            since = report_date.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # 处理结束日期
            if until_date and until_date.strip():
                until = datetime.strptime(until_date, '%Y-%m-%d')
                until = until.replace(hour=23, minute=59, second=59, microsecond=999999)
            else:
                until = since + timedelta(days=1)
            
            # 验证日期范围
            if until <= since:
                return "结束日期必须大于开始日期。", self.load_summary_files()
            
            # 获取GitHub更新
            updates = self.github_client.fetch_updates([repo], since=since, until=until)
            if not updates:
                return "该时间段内没有更新。", self.load_summary_files()
            
            # 生成报告文件
            report_file = self.config.get_export_filepath(repo=repo, since=since)
            self.report_generator.generate_and_save(updates, report_file)
            
            # 生成AI摘要
            summary_file = self.llm_processor.append_summary(
                report_file,
                repo=repo,
                since=date,
                until=until_date if until_date and until_date.strip() else None
            )
            
            # 读取内容并返回更新后的文件列表
            content = ""
            if summary_file and os.path.exists(summary_file):
                with open(summary_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif os.path.exists(report_file):
                with open(report_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                content = "生成报告失败：无法找到生成的文件。"
            
            return content, self.load_summary_files()
                    
        except ValueError:
            return "日期格式错误，请使用YYYY-MM-DD格式。", self.load_summary_files()
        except Exception as e:
            return f"生成报告时发生错误: {str(e)}", self.load_summary_files()

    def add_subscription(self, repo: str) -> tuple[list, str]:
        """添加订阅仓库"""
        try:
            if not repo:
                return self.load_subscriptions(), "请输入仓库名称"
            self.subscription_manager.add_subscription(repo)
            return self.load_subscriptions(), f"成功添加仓库: {repo}"
        except Exception as e:
            return self.load_subscriptions(), f"添加仓库失败: {str(e)}"

    def remove_subscription(self, repo: str) -> tuple[list, str]:
        """删除订阅仓库"""
        try:
            if not repo:
                return self.load_subscriptions(), "请选择要删除的仓库"
            self.subscription_manager.remove_subscription(repo)
            return self.load_subscriptions(), f"成功删除仓库: {repo}"
        except Exception as e:
            return self.load_subscriptions(), f"删除仓库失败: {str(e)}"

    def load_summary_files(self) -> list:
        """加载已生成的摘要文件列表"""
        try:
            # 获取导出目录下的所有摘要文件
            export_dir = self.config.exports_dir
            summary_files = []
            if os.path.exists(export_dir):
                for filename in os.listdir(export_dir):
                    # print filename
                    if filename.endswith('-summary.md'):
                        # 从文件名中提取信息
                        file_path = os.path.join(export_dir, filename)
                        # 获取文件修改时间
                        mtime = os.path.getmtime(file_path)
                        mtime_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                        summary_files.append([filename, mtime_str, file_path])
            
            # 按修改时间倒序排序
            summary_files.sort(key=lambda x: x[1], reverse=True)
            return summary_files
        except Exception as e:
            print(f"Error loading summary files: {str(e)}")
            return []

    def load_summary_content(self, filename: str) -> str:
        """加载摘要文件内容"""
        try:
            file_path = os.path.join(self.config.exports_dir, filename)
            if not file_path or not os.path.exists(file_path):
                return "文件不存在或已被删除。"
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"读取文件失败: {str(e)}"

    def create_ui(self):
        """创建Gradio界面"""
        # 获取默认日期（昨天）
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # 获取订阅列表并设置默认值
        subscriptions = self.load_subscriptions()
        default_repo = subscriptions[0] if subscriptions else None
        
        # 创建界面
        with gr.Blocks(title="GitHub Sentinel", theme=gr.themes.Soft()) as interface:
            gr.Markdown("# GitHub Sentinel")
            
            with gr.Tabs() as tabs:
                # Report标签页
                with gr.Tab("Report"):
                    with gr.Row(equal_height=True):
                        # 左侧控制面板
                        with gr.Column(scale=1):
                            # 仓库选择下拉框
                            repo_dropdown = gr.Dropdown(
                                choices=subscriptions,
                                value=default_repo,
                                label="Select Repository",
                                info="Choose a repository to generate report"
                            )
                            
                            # 日期选择器
                            date_picker = gr.Textbox(
                                label="Since Date",
                                value=yesterday,
                                info="Format: YYYY-MM-DD"
                            )
                            
                            # 结束日期选择器（可选）
                            until_picker = gr.Textbox(
                                label="Until Date (Optional)",
                                value="",
                                info="Format: YYYY-MM-DD, leave empty for single day report"
                            )
                            
                            with gr.Row():
                                # 提交按钮
                                submit_btn = gr.Button("Generate Report", variant="primary")
                                # 重置按钮
                                reset_btn = gr.Button("Reset")
                            
                            # 摘要文件列表
                            gr.Markdown("### Generated Reports")
                            summary_list = gr.Dataframe(
                                headers=["File Name", "Generated Time", "Path"],
                                value=self.load_summary_files(),
                                interactive=False,
                                elem_classes="summary-list"
                            )
                            refresh_btn = gr.Button("Refresh List", size="sm")
                        
                        # 右侧输出面板
                        with gr.Column(scale=2):
                            # Markdown输出框，设置固定高度和滚动
                            output = gr.Markdown(
                                label="Report Output",
                                value="Report will be displayed here...",
                                show_label=True,
                                elem_classes="output-markdown"
                            )
                
                # RepoLib标签页
                with gr.Tab("RepoLib"):
                    with gr.Row():
                        with gr.Column(scale=1):
                            # 添加仓库
                            new_repo_input = gr.Textbox(
                                label="Add New Repository",
                                placeholder="owner/repo",
                                info="Format: owner/repo (e.g. microsoft/vscode)"
                            )
                            add_btn = gr.Button("Add Repository", variant="primary")
                            
                            # 删除仓库
                            remove_dropdown = gr.Dropdown(
                                choices=subscriptions,
                                label="Remove Repository",
                                info="Select a repository to remove"
                            )
                            remove_btn = gr.Button("Remove Repository", variant="stop")
                            
                        with gr.Column(scale=1):
                            # 订阅列表
                            repo_list = gr.Dataframe(
                                headers=["Subscribed Repositories"],
                                value=[[repo] for repo in subscriptions],
                                interactive=False
                            )
                            
                            # 操作结果提示
                            result_info = gr.Markdown("Repository management results will be shown here...")
            
            # 添加自定义CSS
            gr.HTML("""
                <style>
                .output-markdown {
                    height: calc(100vh - 200px) !important;
                    padding: 1rem !important;
                    border: 1px solid #e0e0e0 !important;
                    border-radius: 8px !important;
                    background-color: #ffffff !important;
                }
                
                /* 移除内部markdown容器的滚动条 */
                .output-markdown > div {
                    height: 100% !important;
                    overflow: hidden !important;
                }
                
                /* 确保链接样式正确 */
                .output-markdown a {
                    color: #2563eb !important;
                    text-decoration: underline !important;
                }
                
                .output-markdown a:hover {
                    color: #1d4ed8 !important;
                }
                
                /* 美化滚动条 */
                .output-markdown {
                    overflow-y: auto !important;
                }
                
                /* 确保emoji和其他特殊字符正确显示 */
                .output-markdown p {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
                }
                
                /* 摘要列表样式 */
                .summary-list {
                    max-height: 300px !important;
                    overflow-y: auto !important;
                }
                
                .summary-list table {
                    width: 100% !important;
                }
                
                .summary-list tr {
                    cursor: pointer !important;
                }
                
                .summary-list tr:hover {
                    background-color: #f5f5f5 !important;
                }
                
                .output-markdown::-webkit-scrollbar {
                    width: 8px;
                }
                .output-markdown::-webkit-scrollbar-track {
                    background: #f1f1f1;
                    border-radius: 4px;
                }
                .output-markdown::-webkit-scrollbar-thumb {
                    background: #888;
                    border-radius: 4px;
                }
                .output-markdown::-webkit-scrollbar-thumb:hover {
                    background: #555;
                }
                </style>
            """)
            
            # 绑定Report标签页事件
            submit_btn.click(
                fn=self.generate_report,
                inputs=[repo_dropdown, date_picker, until_picker],
                outputs=[output, summary_list]  # 更新输出和文件列表
            )
            
            def reset():
                return [
                    {"value": default_repo, "__type__": "update"},
                    {"value": yesterday, "__type__": "update"},
                    {"value": "", "__type__": "update"},  # 清空until日期
                    {"value": "Report will be displayed here...", "__type__": "update"}
                ]
            
            reset_btn.click(
                fn=reset,
                inputs=[],
                outputs=[repo_dropdown, date_picker, until_picker, output]
            )
            
            # 绑定摘要列表事件
            def refresh_summary_list():
                return self.load_summary_files()
            
            refresh_btn.click(
                fn=refresh_summary_list,
                inputs=[],
                outputs=summary_list
            )
            
            # 点击摘要列表加载内容
            def load_selected_summary(evt: gr.SelectData) -> str:
                try:
                    file_name = evt.value  # 使用第三列的完整路径
                    return self.load_summary_content(file_name)
                except Exception as e:
                    return f"加载文件失败: {str(e)}"
            
            summary_list.select(
                fn=load_selected_summary,
                inputs=[],
                outputs=output
            )
            
            # 绑定RepoLib标签页事件
            def update_repo_components(repos):
                return [
                    {"choices": repos, "__type__": "update"},  # 更新Report页面的下拉框
                    {"choices": repos, "__type__": "update"},  # 更新RepoLib页面的下拉框
                    {"value": [[repo] for repo in repos], "__type__": "update"}  # 更新数据表格
                ]
            
            def add_repo(repo):
                repos, message = self.add_subscription(repo)
                components = update_repo_components(repos)
                components.append(message)  # 添加结果消息
                components.append({"value": "", "__type__": "update"})  # 清空输入框
                return components
            
            add_btn.click(
                fn=add_repo,
                inputs=[new_repo_input],
                outputs=[repo_dropdown, remove_dropdown, repo_list, result_info, new_repo_input]
            )
            
            def remove_repo(repo):
                repos, message = self.remove_subscription(repo)
                components = update_repo_components(repos)
                components.append(message)
                return components
            
            remove_btn.click(
                fn=remove_repo,
                inputs=[remove_dropdown],
                outputs=[repo_dropdown, remove_dropdown, repo_list, result_info]
            )
            
        return interface

def main():
    """启动Gradio服务器"""
    ui = GradioUI()
    interface = ui.create_ui()
    interface.launch(
        server_name="0.0.0.0",  # 允许外部访问
        server_port=7860,       # 默认端口
        share=False             # 创建公共链接
    )

if __name__ == "__main__":
    main() 