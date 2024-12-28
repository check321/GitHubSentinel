import argparse
import shlex
from datetime import datetime, timedelta
import os
import json
from typing import Dict, Callable, List
from llm import LLMProcessor
from config import Config

class CLI:
    def __init__(self, github_client, subscription_manager, report_generator, config: Config):
        """初始化CLI
        
        Args:
            github_client: GitHub客户端
            subscription_manager: 订阅管理器
            report_generator: 报告生成器
            config: 配置对象
        """
        self.github_client = github_client
        self.subscription_manager = subscription_manager
        self.report_generator = report_generator
        self.config = config
        self.llm_processor = LLMProcessor(config)
        self.commands: Dict[str, dict] = self._register_commands()
        self.parser = self._create_parser()

    def _register_commands(self) -> Dict[str, dict]:
        """注册所有可用的命令及其配置"""
        return {
            'add': {
                'help': 'Add a subscription',
                'args': [
                    {
                        'name': 'repo',
                        'help': 'The repository to subscribe to (e.g., owner/repo)',
                        'type': str
                    }
                ],
                'handler': self.add_subscription
            },
            'remove': {
                'help': 'Remove a subscription',
                'args': [
                    {
                        'name': 'repo',
                        'help': 'The repository to unsubscribe from (e.g., owner/repo)',
                        'type': str
                    }
                ],
                'handler': self.remove_subscription
            },
            'list': {
                'help': 'List all subscriptions',
                'handler': self.list_subscriptions
            },
            'fetch': {
                'help': 'Fetch updates immediately',
                'handler': self.fetch_updates
            },
            'export': {
                'help': 'Export updates to markdown file',
                'args': [
                    {
                        'name': '--since',
                        'dest': 'since',
                        'help': 'Start date (YYYY-MM-DD), defaults to none',
                        'type': str,
                        'required': False,
                        'default': None,
                    },
                    {
                        'name': '--until',
                        'dest': 'until',
                        'help': 'End date (YYYY-MM-DD), defaults to none',
                        'type': str,
                        'required': False,
                        'default': None,
                    }
                ],
                'handler': self.export_updates
            },
            'help': {
                'help': 'Show this help message',
                'handler': self.print_help
            },
            'daily': {
                'help': 'Export daily progress report for repositories',
                'args': [
                    {
                        'name': '--date',
                        'dest': 'date',
                        'help': 'Report date (YYYY-MM-DD), defaults to today',
                        'type': str,
                        'required': False,
                        'default': None,
                    }
                ],
                'handler': self.export_daily_progress
            }
        }

    def _create_parser(self):
        """创建命令行解析器"""
        parser = argparse.ArgumentParser(
            description='GitHub Sentinel Command Line Interface',
            formatter_class=argparse.RawTextHelpFormatter
        )
        subparsers = parser.add_subparsers(title='Commands', dest='command')

        # 根据注册的命令创建子解析器
        for cmd_name, cmd_config in self.commands.items():
            subparser = subparsers.add_parser(
                cmd_name,
                help=cmd_config['help'],
                formatter_class=argparse.RawTextHelpFormatter
            )
            
            # 添加命令参数（如果有）
            if 'args' in cmd_config:
                for arg in cmd_config['args']:
                    name = arg['name']
                    kwargs = {
                        'help': arg['help'],
                        'type': arg['type']
                    }
                    
                    # 区分可选参数和位置参数
                    if name.startswith('--'):
                        # 可选参数的额外配置
                        if 'required' in arg:
                            kwargs['required'] = arg['required']
                        if 'default' in arg:
                            kwargs['default'] = arg['default']
                        if 'nargs' in arg:
                            kwargs['nargs'] = arg['nargs']
                        if 'dest' in arg:
                            kwargs['dest'] = arg['dest']
                        subparser.add_argument(name, **kwargs)
                    else:
                        # 位置参数
                        subparser.add_argument(name, **kwargs)

        return parser

    def add_subscription(self, args):
        self.subscription_manager.add_subscription(args.repo)
        print(f"Added subscription: {args.repo}")

    def remove_subscription(self, args):
        self.subscription_manager.remove_subscription(args.repo)
        print(f"Removed subscription: {args.repo}")

    def list_subscriptions(self, _):
        subscriptions = self.subscription_manager.get_subscriptions()
        print("Current subscriptions:")
        for sub in subscriptions:
            print(f"- {sub}")

    def fetch_updates(self, _):
        updates = self.github_client.fetch_updates(self.subscription_manager.get_subscriptions())
        print(f"Updates fetched: {json.dumps(updates, indent=4)}")
        report = self.report_generator.generate(updates)
        print("Updates fetched:")
        print(report)

    def export_updates(self, args):
        """导出更新到markdown文件"""
        try:
            since = None
            until = None
            
            if args.since:
                since = datetime.strptime(args.since, '%Y-%m-%d')
            if args.until:
                until = datetime.strptime(args.until, '%Y-%m-%d')
                until = until.replace(hour=23, minute=59, second=59)
                
            updates = self.github_client.fetch_updates(
                self.subscription_manager.get_subscriptions(), 
                since=since,
                until=until
            )
            
            # 使用新的文件命名规则
            filepath = self.config.get_export_filepath(since=since, until=until)
            
            # 生成并保存报告
            final_path = self.report_generator.generate_and_save(updates, filepath, with_summary=True)
            if final_path.endswith('-with-summary.md'):
                print(f"Report with AI summary exported to: {final_path}")
            else:
                print(f"Report exported to: {final_path} (without AI summary)")
            
        except Exception as e:
            print(f"Error exporting updates: {str(e)}")

    def print_help(self, _):
        help_text = ["GitHub Sentinel Command Line Interface\n"]
        help_text.append("Available commands:")
        
        # 动态生成帮助信息
        for cmd_name, cmd_config in self.commands.items():
            help_text.append(f"  {cmd_name:<14} {cmd_config['help']}")
        
        help_text.extend([
            "  exit            Exit the tool",
            "  quit            Exit the tool"
        ])
        
        print("\n".join(help_text))

    def handle_command(self, command: str) -> bool:
        """处理命令输入"""
        if command in ["exit", "quit"]:
            return False
            
        try:
            args = self.parser.parse_args(shlex.split(command))
            if args.command and args.command in self.commands:
                self.commands[args.command]['handler'](args)
            else:
                self.parser.print_help()
        except Exception as e:
            print(f"Error: {e}")
        
        return True

    def run(self):
        """运行CLI交互循环"""
        self.print_help(None)
        while True:
            try:
                command = input("GitHub Sentinel> ")
                if not self.handle_command(command):
                    print("Exiting GitHub Sentinel...")
                    break
            except KeyboardInterrupt:
                print("\nExiting GitHub Sentinel...")
                break 

    def export_daily_progress(self, args):
        """导出每日进度报告"""
        try:
            if args.date:
                report_date = datetime.strptime(args.date, '%Y-%m-%d')
            else:
                report_date = datetime.now()
            
            since = report_date.replace(hour=0, minute=0, second=0, microsecond=0)
            until = since + timedelta(days=1)
            
            subscriptions = self.subscription_manager.get_subscriptions()
            for repo in subscriptions:
                self._generate_daily_report(repo, since, until, report_date)
            
        except ValueError as e:
            print(f"Error: Invalid date format. Please use YYYY-MM-DD. ({str(e)})")
        except Exception as e:
            print(f"Error generating daily report: {str(e)}")

    def _generate_daily_report(self, repo: str, since: datetime, until: datetime, report_date: datetime):
        """为单个仓库生成每日报告"""
        # 获取当日更新
        updates = self.github_client.fetch_updates([repo], since=since)
        
        # 使用新的文件命名规则
        filepath = self.config.get_export_filepath(repo=repo, since=since)
        
        # 生成并保存报告
        try:
            final_path = self.report_generator.generate_and_save(updates, filepath, with_summary=True)
            if final_path.endswith('-with-summary.md'):
                print(f"Daily report with AI summary exported to: {final_path}")
            else:
                print(f"Daily report exported to: {final_path} (without AI summary)")
        except Exception as e:
            print(f"Error generating report: {str(e)}")

    def _format_commits(self, commits: List[Dict]) -> str:
        """格式化提交信息"""
        if not commits:
            return "No commits found today.\n"
        
        lines = []
        for commit in commits:
            sha = commit.get('sha', '')[:7]
            message = commit.get('commit', {}).get('message', '').split('\n')[0]
            author = commit.get('commit', {}).get('author', {}).get('name', 'Unknown')
            lines.append(f"- [`{sha}`] {message} (by {author})")
        
        return '\n'.join(lines) + '\n'

    def _format_issues(self, issues: List[Dict]) -> str:
        """格式化议题信息"""
        if not issues:
            return "No issues updated today.\n"
        
        lines = []
        for issue in issues:
            number = issue.get('number')
            title = issue.get('title')
            state = issue.get('state')
            url = issue.get('html_url')
            lines.append(f"- #{number} [{title}]({url}) ({state})")
        
        return '\n'.join(lines) + '\n'

    def _format_pull_requests(self, prs: List[Dict]) -> str:
        """格式化拉取请求信息"""
        if not prs:
            return "No pull requests updated today.\n"
        
        lines = []
        for pr in prs:
            number = pr.get('number')
            title = pr.get('title')
            state = pr.get('state')
            url = pr.get('html_url')
            user = pr.get('user', {}).get('login', 'Unknown')
            lines.append(f"- #{number} [{title}]({url}) by @{user} ({state})")
        
        return '\n'.join(lines) + '\n' 