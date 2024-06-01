
import requests
from collections import defaultdict
from datetime import datetime, timedelta


token = 'put_token_here'   # add your token

headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}

# Define the date range
since = (datetime.now() - timedelta(days=7)).isoformat()
until = datetime.now().isoformat()


def fetch_data(url, params=None):
    """Fetch data from GitHub API"""
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def get_commits(owner,repo):
    """Fetch number of commits"""
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {'since': since, 'until': until}
    return fetch_data(url, params)


def get_pull_requests(owner,repo):
    """Fetch the number of PR"""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    params = {'state': 'all', 'sort': 'created', 'direction': 'desc', 'since': since}
    return fetch_data(url, params)


def get_issues(owner,repo):
    """Fetch the number of issues"""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {'since': since}
    return fetch_data(url, params)


def aggregate_user_activity(commits, pull_requests, issues):
    """Aggregate and count the number of commits, pull requests, and issues created by each user."""
    user_activity = defaultdict(lambda: {'commits': 0, 'prs': 0, 'issues': 0})

    for commit in commits:
        author = commit['commit']['author']['name']
        user_activity[author]['commits'] += 1

    for pr in pull_requests:
        author = pr['user']['login']
        user_activity[author]['prs'] += 1

    for issue in issues:
        author = issue['user']['login']
        user_activity[author]['issues'] += 1

    return user_activity


def get_multiple_repos_data(repos):
    """ Retrieve and aggregate user activity across multiple repositories.
     This function compiles data on commits, pull requests,
      and issues for each user across all specified repositories."""
    overall_user_activity = defaultdict(lambda: {'commits': 0, 'prs': 0, 'issues': 0})

    for owner, repo in repos:
        commits = get_commits(owner, repo)
        pull_requests = get_pull_requests(owner, repo)
        issues = get_issues(owner, repo)
        user_activity = aggregate_user_activity(commits, pull_requests, issues)

        for user, activity in user_activity.items():
            overall_user_activity[user]['commits'] += activity['commits']
            overall_user_activity[user]['prs'] += activity['prs']
            overall_user_activity[user]['issues'] += activity['issues']

    return overall_user_activity


repo_list = [
    ('mario99logic', 'os-practice'),
    ('nirtal85', 'Playwright-Python-Example'),
    ('omrico', 'backbone'),
    ('eyalFischel', 'maakaf-stats')
]

overall_user_activity = get_multiple_repos_data(repo_list)

for user, activity in overall_user_activity.items():
    print(f"User: {user}, Commits: {activity['commits']}, PRs: {activity['prs']}, Issues: {activity['issues']}\n")


