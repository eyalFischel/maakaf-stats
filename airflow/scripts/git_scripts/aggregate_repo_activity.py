
import requests
from collections import defaultdict
from datetime import datetime, timedelta

token = 'put_token_here'   # add your token
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}

since = (datetime.now() - timedelta(days=7)).isoformat()
until = datetime.now().isoformat()

def fetch_data(url, params=None):
    """Fetch data from GitHub API with pagination and error handling."""
    results = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.ok:
            data = response.json()
            results.extend(data)
            url = response.links.get('next', {}).get('url', None)  # More robust link handling
        else:
            print(f"Failed to fetch data: {response.status_code} - {response.text}")
            break
    return results


def get_commits(owner, repo):
    """Get commits for a specific repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {'since': since, 'until': until}
    return fetch_data(url, params)

def get_pull_requests(owner, repo):
    """Get pull requests for a specific repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    params = {'state': 'all', 'sort': 'created', 'direction': 'desc', 'per_page': 100}
    pull_requests = fetch_data(url, params)
    # Filter pull requests based on creation date
    filtered_prs = [pr for pr in pull_requests if pr['created_at'] >= since and pr['created_at'] <= until]
    return filtered_prs

def get_issues(owner, repo):
    """Get issues for a specific repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {'since': since}
    return fetch_data(url, params)

def get_comments(owner, repo):
    """Get issue comments for a specific repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/comments"
    params = {'since': since}
    return fetch_data(url, params)

def fetch_repository_activity(repositories):
    """Fetch and display activity for multiple repositories from multiple owners."""
    activity = defaultdict(lambda: {'commits': 0, 'prs': 0, 'issues': 0, 'comments': 0})
    for owner, repo in repositories:
        commits = get_commits(owner, repo)
        pull_requests = get_pull_requests(owner, repo)
        issues = get_issues(owner, repo)
        comments = get_comments(owner, repo)

        activity[repo]['commits'] = len(commits)
        activity[repo]['prs'] = len(pull_requests)
        activity[repo]['issues'] = len(issues)
        activity[repo]['comments'] = len(comments)

    return activity



repo_list = [
    ('achiyahb', 'ai-trainer-bff'),
    ('nirtal85', 'Playwright-Python-Example'),
    ('omrico', 'backbone'),
    ('eyalFischel', 'maakaf-stats')
]


repo_activities = fetch_repository_activity(repo_list)

for repo, stats in repo_activities.items():
    print(
        f"Repository: {repo}, Commits: {stats['commits']}, PRs: {stats['prs']}, Issues: {stats['issues']}, Comments: {stats['comments']}"
    )
