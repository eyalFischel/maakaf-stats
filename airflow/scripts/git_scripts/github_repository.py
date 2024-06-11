from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List

from github_entity import GitHubEntity


class RepositoryFetcher(GitHubEntity):
    def __init__(self, repository, token):
        super().__init__(token)
        self.owner = repository.owner
        self.name = repository.name
        self.base_url = f"https://api.github.com/repos/{self.owner}/{self.name}"
        self.since = (datetime.now() - timedelta(days=7)).isoformat()
        self.until = datetime.now().isoformat()
        self.repo_info = self.fetch_single_page_data(f"{self.base_url}")
        self.views = self.fetch_single_page_data(f"{self.base_url}/traffic/views")

    def get_commits(self) -> List[Dict[str, Any]]:
        params = {'since': self.since, 'until': self.until}
        return self.fetch_paginated_data(f"{self.base_url}/commits", params)

    def get_pull_requests(self) -> List[Dict[str, Any]]:
        params = {'state': 'all', 'sort': 'created', 'direction': 'desc', 'per_page': 100}
        return self.fetch_paginated_data(f"{self.base_url}/pulls", params)

    def get_issues(self) -> List[Dict[str, Any]]:
        params = {'since': self.since}
        return self.fetch_paginated_data(f"{self.base_url}/issues", params)

    def get_comments(self) -> List[Dict[str, Any]]:
        params = {'since': self.since}
        return self.fetch_paginated_data(f"{self.base_url}/issues/comments", params)

    def get_stars(self) -> int:
        return self.repo_info.get('stargazers_count')

    def get_forks(self) -> int:
        return self.repo_info.get('forks_count')

    def get_watchers(self) -> int:
        return self.repo_info.get('subscribers_count')

    def update_commit(self,items, user_activity) -> None:
        for commit in items:
            author = commit['commit']['author']['name']
            user_activity[author]['commits'] += 1

    def update_activity(self, items, user_activity, key) -> None:
        for item in items:
            author = item['user']['login']
            user_activity[author][key] += 1

    def get_user_activity(self) -> Dict[str, Dict[str, int]]:

        user_activity = defaultdict(lambda: {'commits': 0, 'prs': 0, 'issues': 0})

        commits = self.get_commits()
        pull_requests = self.get_pull_requests()
        issues = self.get_issues()

        self.update_commit(commits, user_activity)
        self.update_activity(pull_requests, user_activity, 'prs')
        self.update_activity(issues, user_activity, 'issues')

        return user_activity

    def fetch_views(self) -> Dict[str, int]:
        views = {'views': self.views.get('count', 0), 'unique views': self.views.get('uniques', 0)}
        return views

    def fetch_repository_activity(self) -> Dict[str, int]:
        activity = {'commits': len(self.get_commits()), 'prs': len(self.get_pull_requests()),
                    'issues': len(self.get_issues()), 'comments': len(self.get_comments())}
        return activity

    def fetch_user_activity(self) -> Dict[str, Dict[str, int]]:
        activity = {}
        activity_dict = self.get_user_activity()
        for user, activities in activity_dict.items():
            activity[user] = {
                'Commits': activities['commits'],
                'PRs': activities['prs'],
                'Issues': activities['issues']
            }
        return activity

