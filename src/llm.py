from openai import OpenAI
from typing import Optional
from config import Config
import os

class LLMProcessor:
    def __init__(self, config: Config):
        """初始化OpenAI客户端
        
        Args:
            config: 配置对象
        """
        self.config = config
        try:
            self.client = OpenAI(
                api_key=config.openai_api_key,
                base_url=config.openai_base_url
            )
        except Exception as e:
            print(f"Warning: Failed to initialize OpenAI client: {str(e)}")
            self.client = None

    def generate_daily_report(self, markdown_content: str, repo: str, since: str, until: Optional[str] = None) -> str:
        """使用OpenAI生成每日报告摘要
        
        Args:
            markdown_content: 原始markdown内容
            repo: 仓库名称
            since: 开始日期
            until: 结束日期（可选）
        """
        if not self.client:
            return "AI摘要生成器未正确初始化，跳过摘要生成。"
        
        try:
            # 读取prompt模板
            prompt_path = os.path.join('prompt', 'generate_daily_report.txt')
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_template = f.read()
            
            # 生成标题
            if until:
                title = f"# {repo}-{since}-{until} 更新摘要\n\n"
            else:
                title = f"# {repo}-{since} 更新摘要\n\n"
            
            # 填充内容
            prompt = prompt_template.format(content=markdown_content)
            
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": self.config.openai_system_prompt,
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.config.openai_temperature,
                max_tokens=self.config.openai_max_tokens,
            )
            
            # 在摘要前添加标题
            return title + response.choices[0].message.content

        except FileNotFoundError:
            print(f"Error: Prompt template file not found at {prompt_path}")
            return "无法加载提示词模板。"
        except Exception as e:
            print(f"Error generating report with OpenAI: {str(e)}")
            return "AI摘要生成失败，请检查网络连接和API配置。"

    def append_summary(self, markdown_file: str, repo: str, since: str, until: Optional[str] = None) -> Optional[str]:
        """读取markdown文件并添加AI生成的摘要"""
        if not self.client:
            print("Warning: OpenAI client not initialized, skipping summary generation")
            return None

        try:
            # 读取原始文件内容
            with open(markdown_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 生成摘要
            summary = self.generate_daily_report(content, repo, since, until)

            # 创建新的文件名
            new_file = self.config.get_summary_filepath(markdown_file)

            # 写入新文件
            with open(new_file, "w", encoding="utf-8") as f:
                f.write(summary)
                f.write("\n\n---\n\n# 详细内容\n\n")
                f.write(content)

            return new_file

        except Exception as e:
            print(f"Error processing markdown file: {str(e)}")
            return None


if __name__ == "__main__":
    config = Config()
    llm = LLMProcessor(config)
