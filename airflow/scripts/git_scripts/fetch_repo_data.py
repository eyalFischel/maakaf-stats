import requests


token = 'put_token_here'   # add your token


def get_repo_data(owner, repo, token):

    """ Fetch the data of the repository including stars, forks, watchers,
     views and unique views(how many different users). views only work on repos you own"""

    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}

    # Get repository information
    repo_url = f"https://api.github.com/repos/{owner}/{repo}"
    repo_response = requests.get(repo_url, headers=headers)
    repo_data = repo_response.json()

    stars = repo_data.get('stargazers_count', 0)
    forks = repo_data.get('forks_count', 0)
    watchers = repo_data.get('subscribers_count', 0)

    # Get repository views
    views_url = f"https://api.github.com/repos/{owner}/{repo}/traffic/views"
    views_response = requests.get(views_url, headers=headers)
    views_data = views_response.json()

    views_count = views_data.get('count', 0)
    unique_views = views_data.get('uniques', 0)

    return {
        'stars': stars,
        'forks': forks,
        'watchers': watchers,
        'views_count': views_count,
        'unique_views': unique_views
    }

def fetch_multiple_repos(repo_list, token):
    """Fetch data for multiple repositories."""
    results = []
    for username, repo_name in repo_list:
        repo_data = get_repo_data(username, repo_name, token)
        results.append(repo_data)
    return results


repo_list = [
    ('achiyahb', 'ai-trainer-bff'),
    ('nirtal85', 'Playwright-Python-Example'),
    ('omrico', 'backbone'),
    ('eyalFischel', 'maakaf-stats')
]

results = fetch_multiple_repos(repo_list, token)

for repo_data in results:
    print(repo_data)
