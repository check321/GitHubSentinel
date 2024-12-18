import requests

class GitHubClient:
    def __init__(self, token):
        self.token = token
    
    def fetch_updates(self, subscriptions):
        # headers = {
        #     'Authorization': f'Bearer {self.token}'
        # }
        updates = {}
        for repo in subscriptions:
            response = requests.get(f'https://api.github.com/repos/{repo}/releases/latest')
            if response.status_code == 200:
                updates[repo] = response.json()
            # print response message if the response is not 200
            else:
                print(f"Error fetching updates for {repo}: {response.text}")
        return updates
