from typing import List, Dict, Tuple
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from llm import LLMProcessor
from config import Config

# 配置日志记录
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class HackerNewsClient:
    """HackerNews客户端，用于抓取Hacker News的新闻列表"""
    
    BASE_URL = "https://news.ycombinator.com/"
    
    def __init__(self, config: Config = None):
        """初始化HackerNews客户端"""
        self.session = requests.Session()
        # 设置用户代理，避免被封禁
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        })
        self.config = config
        self.llm_processor = LLMProcessor(config) if config else None
        logger.info("HackerNewsClient initialized with headers: %s", self.session.headers)

    def chat_completion(self, prompt: str) -> str:
        """使用OpenAI生成回复
        
        Args:
            prompt: 提示词
            
        Returns:
            str: 生成的回复
        """
        if not self.llm_processor or not self.llm_processor.client:
            logger.error("LLMProcessor not initialized properly")
            return ""
            
        try:
            response = self.llm_processor.client.chat.completions.create(
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
            logger.error("Failed to generate chat completion: %s", str(e))
            return ""

    def generate_report(self, news_list: List[Dict]) -> Tuple[str, str]:
        """使用ChatGPT生成新闻报告
        
        Args:
            news_list: 新闻列表
            
        Returns:
            Tuple[str, str]: (英文报告, 中文报告)
        """
        if not self.llm_processor:
            logger.error("LLMProcessor not initialized, cannot generate report")
            return "", ""
            
        try:
            # 构建新闻摘要文本
            news_text = []
            for i, news in enumerate(news_list, 1):
                news_text.append(f"{i}. {news['title']}")
                news_text.append(f"   Score: {news['score']}, Comments: {news['comments_count']}")
                news_text.append(f"   URL: {news['url']}")
                news_text.append("")
            
            news_content = "\n".join(news_text)
            
            # 生成英文报告的提示词
            en_prompt = f"""Please analyze the following Hacker News top stories and generate a comprehensive report. 
Focus on identifying key trends, notable discussions, and significant developments in technology.

News List:
{news_content}

Please structure your report with:
1. Overview of top trending topics
2. Notable technical discussions or announcements
3. Key community interests
4. Emerging trends or patterns

Keep the tone professional but engaging."""

            # 生成中文报告的提示词
            zh_prompt = f"""请分析以下Hacker News热门新闻，并生成一份详细的中文报告。
重点关注技术趋势、值得注意的讨论以及重要的技术发展。

新闻列表：
{news_content}

请按以下结构组织报告：
1. 热门话题概述
2. 值得关注的技术讨论或公告
3. 社区关注重点
4. 新兴趋势或模式

使用专业但易于理解的语言，确保对中文读者友好。"""

            # 使用LLM生成报告
            en_report = self.chat_completion(en_prompt)
            zh_report = self.chat_completion(zh_prompt)
            
            logger.info("Successfully generated news reports")
            return en_report, zh_report
            
        except Exception as e:
            logger.error("Failed to generate news report: %s", str(e), exc_info=True)
            return "", ""

    def translate_titles(self, news_list: List[Dict]) -> List[Dict]:
        """使用ChatGPT翻译新闻标题
        
        Args:
            news_list: 新闻列表
            
        Returns:
            List[Dict]: 带有中文标题的新闻列表
        """
        if not self.llm_processor:
            logger.warning("LLMProcessor not initialized, skipping title translation")
            return news_list
            
        try:
            # 构建翻译提示词
            titles = [f"{i+1}. {news['title']}" for i, news in enumerate(news_list)]
            titles_text = "\n".join(titles)
            
            prompt = f"""请将以下Hacker News新闻标题翻译成中文，保持专业性和准确性。
只需要翻译，不要添加任何额外的内容。按照原有的编号顺序输出。

{titles_text}

翻译规则：
1. 保留原文中的专有名词（如项目名、公司名）
2. 技术术语使用通用的中文翻译
3. 每行以序号开始，保持原有格式
4. 只输出翻译结果，不要有任何其他内容"""

            # 获取翻译结果
            translations = self.chat_completion(prompt)
            
            # 解析翻译结果
            translation_lines = [line.strip() for line in translations.split('\n') if line.strip()]
            
            # 创建翻译后的新闻列表
            translated_news = []
            for i, news in enumerate(news_list):
                if i < len(translation_lines):
                    # 提取翻译后的标题（去除序号和点）
                    translated_title = translation_lines[i]
                    if '. ' in translated_title:
                        translated_title = translated_title.split('. ', 1)[1]
                    
                    # 创建新的新闻字典，包含原标题和翻译
                    news_item = dict(news)
                    news_item['title_zh'] = translated_title
                    translated_news.append(news_item)
                else:
                    # 如果没有对应的翻译，使用原标题
                    news_item = dict(news)
                    news_item['title_zh'] = news['title']
                    translated_news.append(news_item)
            
            logger.info("Successfully translated %d news titles", len(translated_news))
            return translated_news
            
        except Exception as e:
            logger.error("Failed to translate news titles: %s", str(e), exc_info=True)
            return news_list

    def get_news_list(self, limit: int = 30, generate_report: bool = False) -> Dict:
        """获取HackerNews新闻列表
        
        Args:
            limit: 获取的新闻数量，默认30条
            generate_report: 是否生成报告，默认False
            
        Returns:
            Dict: 包含新闻列表和可选的报告
        """
        try:
            logger.info("Fetching news from HackerNews with limit: %d", limit)
            response = self.session.get(self.BASE_URL)
            response.raise_for_status()
            
            logger.debug("Response status code: %d", response.status_code)
            
            # 保存响应内容到文件以供调试
            with open('hn_response.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            logger.debug("Saved response content to hn_response.html")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找所有新闻条目（直接查找，不依赖表格结构）
            items = soup.find_all('tr', class_='athing')
            logger.info("Found %d news items in total", len(items))
            
            if not items:
                logger.error("No news items found")
                return {"news": [], "reports": {}}
            
            news_list = []
            for i, item in enumerate(items[:limit], 1):
                try:
                    logger.debug("Processing news item %d/%d (id: %s)", i, limit, item.get('id', 'unknown'))
                    
                    # 获取标题和链接
                    title_link = item.select_one('td.title a')  # 使用CSS选择器
                    if not title_link:
                        logger.warning("No title link found for item %d", i)
                        continue
                    
                    # 获取分数和评论信息（在下一个tr中）
                    subtext = item.find_next_sibling('tr')
                    if not subtext:
                        logger.warning("No subtext found for item %d", i)
                        continue
                    
                    # 获取分数
                    score = 0
                    score_span = subtext.find('span', class_='score')
                    if score_span:
                        try:
                            score_text = score_span.text.strip()
                            score = int(score_text.split()[0])
                            logger.debug("Found score %d for item %d", score, i)
                        except (ValueError, IndexError) as e:
                            logger.warning("Failed to parse score for item %d: %s", i, str(e))
                    
                    # 获取评论数
                    comments_count = 0
                    comments_link = subtext.select_one('a:contains("comment")')
                    if comments_link:
                        try:
                            comments_text = comments_link.text.split()[0]
                            if comments_text.isdigit():
                                comments_count = int(comments_text)
                                logger.debug("Found %d comments for item %d", comments_count, i)
                        except (ValueError, IndexError) as e:
                            logger.warning("Failed to parse comments count for item %d: %s", i, str(e))
                    
                    news = {
                        'id': item.get('id'),
                        'title': title_link.text.strip(),
                        'url': title_link.get('href'),
                        'score': score,
                        'comments_count': comments_count,
                        'comments_url': f"{self.BASE_URL}item?id={item.get('id')}",
                        'timestamp': datetime.now().isoformat()
                    }
                    logger.debug("Successfully processed news item: %s", news)
                    news_list.append(news)
                    
                except Exception as e:
                    logger.error("Error processing news item %d: %s", i, str(e), exc_info=True)
                    continue
                
            logger.info("Successfully fetched %d news items", len(news_list))
            
            # 如果需要生成报告，先翻译标题
            if generate_report and self.config:
                news_list = self.translate_titles(news_list)
            
            result = {"news": news_list, "reports": {}}
            
            # 如果需要生成报告
            if generate_report and news_list:
                en_report, zh_report = self.generate_report(news_list)
                result["reports"] = {
                    "en": en_report,
                    "zh": zh_report
                }
            
            return result
            
        except requests.RequestException as e:
            logger.error("Failed to fetch news from Hacker News: %s", str(e), exc_info=True)
            return {"news": [], "reports": {}}
        except Exception as e:
            logger.error("Error parsing Hacker News content: %s", str(e), exc_info=True)
            return {"news": [], "reports": {}} 