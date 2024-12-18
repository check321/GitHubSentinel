import json
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        # 加载.env文件
        load_dotenv()
        self.load_config()
    
    def load_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            # 从环境变量读取github token
            self.github_token = os.getenv('GITHUB_TOKEN')
            if not self.github_token:
                raise ValueError("GitHub token not found in environment variables")
            self.notification_settings = config.get('notification_settings')
            self.subscriptions_file = config.get('subscriptions_file')
            self.update_interval = config.get('update_interval', 24 * 60 * 60)  # Default to 24 hours
