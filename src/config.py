import json
import os
from dotenv import load_dotenv
from datetime import datetime

class Config:
    def __init__(self):
        # 加载.env文件
        load_dotenv(override=True)
        self.load_config()
    
    def load_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            
            # GitHub配置
            self.github_token = os.getenv('GITHUB_TOKEN')
            if not self.github_token:
                raise ValueError("GitHub token not found in environment variables")
            self.github_config = config.get('github', {})
            
            # OpenAI配置
            self.openai_api_key = os.getenv('OPENAI_API_KEY')
            if not self.openai_api_key:
                raise ValueError("OpenAI API key not found in environment variables")
            self.openai_base_url = os.getenv('OPENAI_BASE_URL')
            
            openai_config = config.get('openai', {})
            self.openai_model = openai_config.get('model', 'gpt-4o-mini')
            self.openai_max_tokens = openai_config.get('max_tokens', 5000)
            self.openai_temperature = openai_config.get('temperature', 0.7)
            self.openai_system_prompt = openai_config.get('system_prompt', '')
            self.prompt_dir = openai_config.get('prompt_dir', 'prompt')
            
            # 确保prompt目录存在
            os.makedirs(self.prompt_dir, exist_ok=True)
            
            # 导出配置
            self.exports_config = config.get('exports', {})
            self.exports_dir = self.exports_config.get('directory', 'exports')
            
            # 确保导出目录存在
            os.makedirs(self.exports_dir, exist_ok=True)
            
            # 通知配置
            self._notification_settings = {}
            
            # 从环境变量加载邮件配置
            email_config = {
                'enabled': True,  # 默认启用
                'smtp_server': os.getenv('EMAIL_SMTP_SERVER'),
                'smtp_port': int(os.getenv('EMAIL_SMTP_PORT', 465)),
                'sender_email': os.getenv('EMAIL_SENDER'),
                'sender_password': os.getenv('EMAIL_PASSWORD'),
                'recipients': [email.strip() for email in os.getenv('EMAIL_RECIPIENTS', '').split(',') if email.strip()],
                'subject_template': 'GitHub Updates: {repo} - {date}'
            }
            
            # 验证必要的邮件配置
            required_email_fields = ['smtp_server', 'sender_email', 'sender_password', 'recipients']
            missing_fields = [field for field in required_email_fields if not email_config.get(field)]
            
            if missing_fields:
                print(f"Warning: Missing email configuration fields: {', '.join(missing_fields)}")
                email_config['enabled'] = False
            
            self._notification_settings['email'] = email_config
            
            # 其他配置
            self.subscriptions_file = config.get('subscriptions_file', 'subscriptions.json')
            self.update_interval = config.get('update_interval', 24 * 60 * 60)

    def get_export_filepath(self, repo: str = None, since: datetime = None, until: datetime = None) -> str:
        """生成导出文件路径
        
        Args:
            repo: 可选，仓库名称
            since: 可选，开始时间
            until: 可选，结束时间
        """
        # 确保导出目录存在
        os.makedirs(self.exports_dir, exist_ok=True)
        
        # 生成基础文件名
        if repo:
            base_name = repo.replace('/', '_')
        else:
            base_name = "github_updates"
        
        # 添加时间信息
        if since:
            if until:
                # 如果有时间范围，使用范围格式
                date_str = f"{since.strftime('%Y%m%d')}-{until.strftime('%Y%m%d')}"
            else:
                # 如果只有开始时间，只使用单个日期
                date_str = since.strftime('%Y%m%d')
        else:
            # 如果没有时间信息，使用当前时间戳
            date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        filename = f"{base_name}_{date_str}.md"
        return os.path.join(self.exports_dir, filename)

    def get_summary_filepath(self, original_path: str) -> str:
        """生成带摘要的文件路径"""
        file_path, ext = os.path.splitext(original_path)
        summary_suffix = self.exports_config.get('summary_suffix', '-with-summary')
        return f"{file_path}{summary_suffix}{ext}"

    @property
    def notification_settings(self) -> dict:
        """获取通知设置"""
        return self._notification_settings
