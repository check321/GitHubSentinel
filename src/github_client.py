import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import time
from config import Config

class GitHubClient:
    """GitHub API客户端"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, config: Config):
        """初始化GitHub客户端
        
        Args:
            config: Config对象，包含所有配置信息
        """
        self.config = config
        self.token = config.github_token  # 直接使用config对象中的token
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.rate_limit_remaining = None
        self.rate_limit_reset = None

    def _make_request(self, url: str, params: Optional[Dict] = None) -> Dict:
        """发送API请求并处理常见错误"""
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            # 更新速率限制信息
            self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
            self.rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', 0))
            
            # 处理速率限制
            if response.status_code == 403 and self.rate_limit_remaining == 0:
                reset_time = datetime.fromtimestamp(self.rate_limit_reset)
                wait_time = (reset_time - datetime.now()).total_seconds()
                if wait_time > 0:
                    print(f"Rate limit exceeded. Waiting {wait_time:.0f} seconds...")
                    time.sleep(wait_time)
                    return self._make_request(url, params)  # 重试请求
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {str(e)}")
            return {}

    def fetch_updates(self, subscriptions: List[str], since: Optional[datetime] = None, 
                     until: Optional[datetime] = None) -> Dict[str, Any]:
        """获取仓库的所有更新信息
        
        Args:
            subscriptions: 仓库列表
            since: 可选，开始时间
            until: 可选，结束时间
        """
        updates = {}
        for repo in subscriptions:
            repo_updates = {
                'releases': {},
                'commits': [],
                'issues': [],
                'pull_requests': []
            }
            
            # 获取最新发布
            releases = self.fetch_releases(repo, since, until)
            if releases:
                repo_updates['releases'] = releases[0]  # 只取最新的一个
            
            # 获取提交历史
            repo_updates['commits'] = self.fetch_commits(repo, since, until)
            
            # 获取议题
            repo_updates['issues'] = self.fetch_issues(repo, since, until)
            
            # 获取拉取请求
            repo_updates['pull_requests'] = self.fetch_pull_requests(repo, since, until)
            
            updates[repo] = repo_updates
            
        return updates

    def fetch_releases(self, repo: str, since: Optional[datetime] = None,
                      until: Optional[datetime] = None) -> List[Dict]:
        """获取仓库的发布记录"""
        url = f"{self.config.github_config['api_base_url']}/repos/{repo}/releases"
        params = {'per_page': self.config.github_config['items_per_page']}
        
        releases = self._make_request(url, params) or []
        
        # 过滤时间范围
        if since or until:
            filtered = []
            for release in releases:
                published_at = datetime.strptime(release['published_at'], '%Y-%m-%dT%H:%M:%SZ')
                if since and published_at < since:
                    continue
                if until and published_at > until:
                    continue
                filtered.append(release)
            return filtered
            
        return releases

    def fetch_commits(self, repo: str, since: Optional[datetime] = None,
                     until: Optional[datetime] = None) -> List[Dict]:
        """获取仓库的提交历史"""
        url = f"{self.config.github_config['api_base_url']}/repos/{repo}/commits"
        params = {'per_page': self.config.github_config['items_per_page']}
        
        if since:
            params['since'] = since.isoformat()
        if until:
            params['until'] = until.isoformat()
            
        return self._make_request(url, params) or []

    def fetch_issues(self, repo: str, since: Optional[datetime] = None,
                    until: Optional[datetime] = None, state: str = 'all') -> List[Dict]:
        """获取仓库的议题"""
        url = f"{self.config.github_config['api_base_url']}/repos/{repo}/issues"
        params = {
            'state': state,
            'per_page': self.config.github_config['items_per_page']
        }
        
        if since:
            params['since'] = since.isoformat()
            
        issues = self._make_request(url, params) or []
        
        # GitHub API的issues接口只支持since参数，所以需要手动过滤until
        if until:
            filtered = []
            for issue in issues:
                updated_at = datetime.strptime(issue['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
                if updated_at <= until:
                    filtered.append(issue)
            return filtered
            
        return issues

    def fetch_pull_requests(self, repo: str, since: Optional[datetime] = None,
                          until: Optional[datetime] = None, state: str = 'all') -> List[Dict]:
        """获取仓库的拉取请求"""
        url = f"{self.config.github_config['api_base_url']}/repos/{repo}/pulls"
        params = {
            'state': state,
            'per_page': self.config.github_config['items_per_page']
        }
        
        prs = self._make_request(url, params) or []
        
        # 手动过滤时间范围，因为PR接口不支持since和until参数
        if since or until:
            filtered = []
            for pr in prs:
                updated_at = datetime.strptime(pr['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
                if since and updated_at < since:
                    continue
                if until and updated_at > until:
                    continue
                filtered.append(pr)
            return filtered
            
        return prs

    def get_rate_limit_info(self) -> Dict[str, Any]:
        """获取API速率限制信息"""
        url = f"{self.BASE_URL}/rate_limit"
        return self._make_request(url)

    def check_repository_exists(self, repo: str) -> bool:
        """检查仓库是否存在
        
        Args:
            repo: 仓库名称 (格式: owner/repo)
        """
        url = f"{self.BASE_URL}/repos/{repo}"
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
