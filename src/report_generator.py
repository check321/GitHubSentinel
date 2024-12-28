from typing import Dict, List
from llm import LLMProcessor
import os
from config import Config

class ReportGenerator:
    def __init__(self, config: Config):
        """初始化报告生成器"""
        self.llm_processor = LLMProcessor(config)

    def generate(self, updates):
        """生成更新报告"""
        report = ""
        for repo, data in updates.items():
            report += f"\n## {repo}\n\n"
            
            # 处理releases信息
            release = data.get('releases', {})
            if release:
                report += "### Latest Release\n"
                report += f"- Version: {release.get('tag_name', 'N/A')}\n"
                report += f"- Title: {release.get('name', 'N/A')}\n"
                report += f"- Published at: {release.get('published_at', 'N/A')}\n"
                report += f"- URL: {release.get('html_url', 'N/A')}\n\n"
            else:
                report += "### No releases found\n\n"
            
            # 处理commits信息
            commits = data.get('commits', [])
            if commits:
                report += "### Recent Commits\n"
                for commit in commits:
                    sha = commit.get('sha', '')[:7]
                    message = commit.get('commit', {}).get('message', '').split('\n')[0]
                    author = commit.get('commit', {}).get('author', {}).get('name', 'Unknown')
                    report += f"- [`{sha}`] {message} (by {author})\n"
                report += "\n"
            
            # 处理issues信息
            issues = data.get('issues', [])
            if issues:
                report += "### Recent Issues\n"
                for issue in issues:
                    number = issue.get('number', 'N/A')
                    title = issue.get('title', 'N/A')
                    state = issue.get('state', 'unknown')
                    url = issue.get('html_url', '#')
                    report += f"- #{number} [{title}]({url}) ({state})\n"
                report += "\n"
            
            # 处理pull requests信息
            prs = data.get('pull_requests', [])
            if prs:
                report += "### Recent Pull Requests\n"
                for pr in prs:
                    number = pr.get('number', 'N/A')
                    title = pr.get('title', 'N/A')
                    state = pr.get('state', 'unknown')
                    url = pr.get('html_url', '#')
                    user = pr.get('user', {}).get('login', 'Unknown')
                    report += f"- #{number} [{title}]({url}) by @{user} ({state})\n"
                report += "\n"
            
        return report

    def generate_and_save(self, updates: Dict, filepath: str, with_summary: bool = True) -> str:
        """生成报告并保存到文件
        
        Args:
            updates: 更新数据
            filepath: 输出文件路径
            with_summary: 是否生成AI摘要
            
        Returns:
            str: 最终生成的文件路径
        """
        # 确保输出目录存在
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # 生成报告
        report = self.generate(updates)
        
        # 写入原始报告
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
            
        if with_summary:
            try:
                # 生成带摘要的报告
                summary_file = self.llm_processor.append_summary(filepath)
                if summary_file:
                    return summary_file
            except Exception as e:
                print(f"Failed to generate AI summary: {str(e)}")
                
        return filepath
