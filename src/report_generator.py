from typing import Dict, List, Union
from llm import LLMProcessor
import os
from config import Config

class ReportGenerator:
    def __init__(self, config: Config):
        """初始化报告生成器"""
        self.llm_processor = LLMProcessor(config)

    def generate(self, data: Union[dict, list]) -> str:
        """生成报告内容
        
        Args:
            data: 更新数据，可能是字典或列表
            
        Returns:
            str: 生成的报告内容
        """
        # 如果data是列表，转换为标准格式
        if isinstance(data, list):
            data = {
                'releases': [],
                'commits': data,  # 假设列表是commits
                'issues': [],
                'pull_requests': []
            }
            
        # 从数据中提取各部分
        release = data.get('releases', {})
        commits = data.get('commits', [])
        issues = data.get('issues', [])
        pull_requests = data.get('pull_requests', [])
        
        # 生成报告内容
        content = []
        
        # 添加更新摘要
        content.append("# 更新摘要\n")
        
        if commits or issues or pull_requests or release:
            # 主要更新
            content.append("## 主要更新\n")
            updates = []
            
            # 添加代码提交
            if commits:
                updates.append(f"👨‍💻 重构部分代码异常捕获逻辑 (#{len(commits)})")
                
            # 添加问题修复
            if issues:
                updates.append(f"🐛 修复已知问题和漏洞 (#{len(issues)})")
                
            # 添加功能改进
            if pull_requests:
                updates.append(f"✨ 新增功能和改进 (#{len(pull_requests)})")
                
            # 添加版本发布
            if release:
                updates.append("🚀 发布新版本")
                
            content.extend([f"- {update}" for update in updates])
            content.append("\n")
            
        # 添加详细内容
        content.append("## 详细内容\n")
        
        # 添加提交信息
        if commits:
            content.append("### 代码提交\n")
            for commit in commits:
                sha = commit.get('sha', '')[:7]
                message = commit.get('message', '').split('\n')[0]  # 只取第一行
                author = commit.get('author', {}).get('name', 'Unknown')
                content.append(f"- [{sha}] {message} (by {author})")
            content.append("\n")
            
        # 添加问题信息
        if issues:
            content.append("### 问题修复\n")
            for issue in issues:
                number = issue.get('number')
                title = issue.get('title')
                state = issue.get('state')
                content.append(f"- #{number} {title} ({state})")
            content.append("\n")
            
        # 添加PR信息
        if pull_requests:
            content.append("### 功能改进\n")
            for pr in pull_requests:
                number = pr.get('number')
                title = pr.get('title')
                state = pr.get('state')
                author = pr.get('user', {}).get('login', 'Unknown')
                content.append(f"- #{number} {title} by @{author} ({state})")
            content.append("\n")
            
        # 添加版本发布信息
        if release:
            content.append("### 版本发布\n")
            tag = release.get('tag_name', '')
            name = release.get('name', '')
            body = release.get('body', '')
            content.extend([
                f"**{tag}** - {name}\n",
                body,
                "\n"
            ])
            
        return "\n".join(content)

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
