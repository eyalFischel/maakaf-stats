import os

from dotenv import load_dotenv

from github_repository import RepositoryFetcher
from repository import Repository


load_dotenv()
github_token = os.getenv('GITHUB_TOKEN')

def main():
    repository1 = Repository(owner='eyalFischel', name='maakaf-stats')
    repo1 = RepositoryFetcher(repository1, github_token)
    print(repo1.fetch_repository_activity())


main()
