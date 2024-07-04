import os

from dotenv import load_dotenv

from database import SessionLocal
from github_repository import RepositoryFetcher
from repository import Repository
from sql_modules import RepositoryORM, GitHubUserORM


load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")


def collect_repository_data() -> None:
    """Gets the repositories from the DB and print their stats using the git api"""
    session = SessionLocal()

    # Fetch all repositories from the database
    repositories = session.query(RepositoryORM).all()

    for repo in repositories:
        user = (
            session.query(GitHubUserORM)
            .filter(GitHubUserORM.user_id == repo.userid)
            .first()
        )
        if user:
            # Initialize RepositoryFetcher with owner and repo name
            repository_info = {"owner": user.username, "name": repo.name}
            repository = Repository(
                owner=repository_info["owner"], name=repository_info["name"]
            )
            repo_fetcher = RepositoryFetcher(repository, github_token)

            # Fetch repository activity
            activity = repo_fetcher.fetch_repository_activity()
            print(
                f"Activity for {repository_info['owner']}/{repository_info['name']}: {activity}"
            )

    session.close()


def main():
    collect_repository_data()


main()
