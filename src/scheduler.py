import time
from datetime import datetime
import traceback

class Scheduler:
    def __init__(self, github_client, notifier, report_generator, subscription_manager, interval=86400):
        self.github_client = github_client
        self.notifier = notifier
        self.report_generator = report_generator
        self.subscription_manager = subscription_manager
        self.interval = interval
        self.running = False

    def start(self):
        """启动调度器"""
        self.running = True
        self.run()

    def stop(self):
        """停止调度器"""
        self.running = False

    def run(self):
        """运行调度循环"""
        while self.running:
            try:
                # 获取订阅列表
                subscriptions = self.subscription_manager.get_subscriptions()
                
                # 获取更新
                updates = self.github_client.fetch_updates(subscriptions)
                
                # 生成报告
                if updates:
                    for repo, repo_updates in updates.items():
                        # 生成报告内容
                        report_content = self.report_generator.generate(repo_updates)
                        
                        # 发送通知
                        if report_content:
                            self.notifier.send_report(repo=repo, report_content=report_content)
                
                # 等待下一次执行
                time.sleep(self.interval)
                
            except Exception as e:
                # print error stack trace
                print(f"Error in scheduler: {e}")
                traceback.print_exc()
                time.sleep(60)  # 发生错误时等待1分钟后重试
