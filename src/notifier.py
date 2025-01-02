import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import markdown2
import os
from typing import List, Optional
from config import Config
import ssl

class EmailNotifier:
    """邮件通知类"""
    
    def __init__(self, config: Config):
        """初始化邮件通知器
        
        Args:
            config: 配置对象
        """
        self.config = config
        self.email_config = config.notification_settings.get('email', {})
        
        # 验证必要的配置
        if not self.email_config.get('enabled'):
            raise ValueError("Email notification is not enabled in config")
        
        required_fields = ['smtp_server', 'smtp_port', 'sender_email', 'sender_password']
        for field in required_fields:
            if not self.email_config.get(field):
                raise ValueError(f"Missing required email config: {field}")

    def convert_md_to_html(self, markdown_content: str) -> str:
        """将Markdown内容转换为HTML
        
        Args:
            markdown_content: Markdown格式的内容
            
        Returns:
            str: HTML格式的内容
        """
        # 使用markdown2转换，启用额外特性
        extras = [
            "tables",           # 表格支持
            "code-friendly",    # 代码块友好
            "cuddled-lists",    # 列表处理优化
            "fenced-code-blocks", # 围栏式代码块
            "header-ids",       # 标题ID
            "html-classes",     # HTML类支持
            "markdown-in-html", # HTML中的Markdown
            "numbering",        # 编号支持
            "strike",          # 删除线
            "task_list",       # 任务列表
            "toc"              # 目录
        ]
        
        return markdown2.markdown(markdown_content, extras=extras)

    def send_report(self, repo: str, report_content: str, recipients: Optional[List[str]] = None) -> bool:
        """发送报告邮件
        
        Args:
            repo: 仓库名称
            report_content: 报告内容（Markdown格式）
            recipients: 可选的收件人列表，如果不提供则使用配置中的收件人
            
        Returns:
            bool: 发送是否成功
        """
        try:
            # 使用配置的收件人列表或传入的收件人列表
            if recipients is not None:
                to_emails = recipients
            else:
                to_emails = self.email_config['recipients']
                
            if not to_emails:
                raise ValueError("No recipients specified")
            
            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_config['sender_email']
            msg['To'] = ', '.join(to_emails)
            
            # 设置邮件主题
            current_date = datetime.now().strftime('%Y-%m-%d')
            subject_template = self.email_config.get('subject_template', 'GitHub Updates: {repo} - {date}')
            msg['Subject'] = subject_template.format(repo=repo, date=current_date)
            
            # 转换内容为HTML
            html_content = self.convert_md_to_html(report_content)
            
            # 添加HTML内容
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # 打印连接信息
            print(f"Connecting to SMTP server: {self.email_config['smtp_server']}:{self.email_config['smtp_port']}")
            
            # 使用SSL连接
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                self.email_config['smtp_server'],
                self.email_config['smtp_port'],
                context=context
            ) as server:
                # 登录
                print(f"Logging in as {self.email_config['sender_email']}")
                server.login(
                    self.email_config['sender_email'],
                    self.email_config['sender_password']
                )
                print("Login successful")
                
                # 发送邮件
                server.send_message(msg)
                print("Message sent successfully")
                
                print(f"Successfully sent email report for {repo} to {', '.join(to_emails)}")
                return True
                
        except Exception as e:
            print(f"Failed to send email report: {str(e)}")
            return False

class Notifier:
    """通知管理类"""
    
    def __init__(self, notification_settings: dict):
        """初始化通知管理器
        
        Args:
            notification_settings: 通知配置
        """
        self.settings = notification_settings or {}
        self.email_notifier = None
        
        # 如果启用了邮件通知，初始化邮件通知器
        email_settings = self.settings.get('email', {})
        if isinstance(email_settings, dict) and email_settings.get('enabled'):
            try:
                self.email_notifier = EmailNotifier(Config())
            except Exception as e:
                print(f"Failed to initialize email notifier: {str(e)}")

    def send_report(self, repo: str, report_content: str, recipients: Optional[List[str]] = None) -> bool:
        """发送报告
        
        Args:
            repo: 仓库名称
            report_content: 报告内容
            recipients: 可选的收件人列表
            
        Returns:
            bool: 是否成功发送
        """
        success = True
        
        # 发送邮件通知
        if self.email_notifier:
            success &= self.email_notifier.send_report(repo, report_content, recipients)
            
        return success

if __name__ == "__main__":
    # 测试代码
    config = Config()
    notifier = Notifier(config.notification_settings)
    
    test_content = """
    # Test Report
    
    ## Updates
    - Update 1111
    - Update 2222
    
    ### Details
    Some detailed information here.
    """
    
    notifier.send_report("test/repo", test_content)
