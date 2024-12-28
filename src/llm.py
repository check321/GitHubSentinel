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

    def generate_daily_report(self, markdown_content: str) -> str:
        """使用OpenAI生成每日报告摘要"""
        if not self.client:
            return "AI摘要生成器未正确初始化，跳过摘要生成。"

        prompt = f"""
请分析以下GitHub仓库的更新内容，生成一个简洁的中文摘要报告。重点关注：
1. 主要更新内容
2. 重要的问题修复
3. 新功能添加
4. 值得注意的PR

原始内容：
{markdown_content}

请以下面的格式输出：
# 更新摘要
[总体概述]

## 主要更新
- [更新点1]
- [更新点2]

## 重要修复
- [修复1]
- [修复2]

## 新增功能
- [功能1]
- [功能2]

## 其他说明
[其他需要注意的事项]
"""

        try:
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
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error generating report with OpenAI: {str(e)}")
            return "AI摘要生成失败，请检查网络连接和API配置。"

    def append_summary(self, markdown_file: str) -> Optional[str]:
        """读取markdown文件并添加AI生成的摘要"""
        if not self.client:
            print("Warning: OpenAI client not initialized, skipping summary generation")
            return None

        try:
            # 读取原始文件内容
            with open(markdown_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 生成摘要
            summary = self.generate_daily_report(content)

            # 创建新的文件名
            new_file = self.config.get_summary_filepath(markdown_file)

            # 写入新文件
            with open(new_file, "w", encoding="utf-8") as f:
                f.write("# AI 生成的更新摘要\n\n")
                f.write(summary)
                f.write("\n\n---\n\n# 原始更新内容\n\n")
                f.write(content)

            return new_file

        except Exception as e:
            print(f"Error processing markdown file: {str(e)}")
            return None


if __name__ == "__main__":
    config = Config()
    llm = LLMProcessor(config)
