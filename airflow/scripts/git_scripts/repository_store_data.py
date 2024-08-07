import os
from datetime import datetime
from typing import Generator

from dotenv import load_dotenv

from database import SessionLocal
from github_repository import RepositoryFetcher
from repository import Repository
from sql_modules import RepositoryORM, GitHubUserORM
from sqlalchemy.exc import SQLAlchemyError


load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")


def get_repositories(session: any) -> Generator:
    try:
        yield (
            session.query(RepositoryORM.userid, RepositoryORM.name)
            .distinct(RepositoryORM.userid, RepositoryORM.name)
            .all()
        )
    except SQLAlchemyError as error:
        print(f"An error occurred: {error}")
        session.close()
    finally:
        session.close()


def collect_repository_data() -> list:
    """Gets the repositories from the DB and return their stats using the git api"""
    session = SessionLocal()
    repositories = get_repositories(session)

    if not repositories:
        return []
      
    repo_data = []

    for repo in repositories:
        user = (
            session.query(GitHubUserORM)
            .filter(GitHubUserORM.username == repo.owner)
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
            repo_data.append(
                {
                    "owner": repository_info["owner"],
                    "name": repository_info["name"],
                    "activity": activity,
                }
            )

    for data in repo_data:
        print(f"Activity for {data['owner']}/{data['name']}: {data['activity']}")

    return repo_data


def insert_repository_data(repo_data: list) -> None:
    """Inserts the repository data into the database"""
    session = SessionLocal()

    for data in repo_data:
        activity = data["activity"]
        new_repo = RepositoryORM(
            name=data["name"],
            forks=activity.get("forks", 0),
            stars=activity.get("stars", 0),
            commits=activity.get("commits", 0),
            pull_requests=activity.get("prs", 0),
            issues=activity.get("issues", 0),
            comments=activity.get("comments", 0),
            watchers=activity.get("watchers", 0),
            views=activity.get("views", 0),
            active_users=activity.get("activeusers", 0),
            owner=data["owner"],
            fetched_at=datetime.now(),
        )
        session.add(new_repo)

    session.commit()
    session.close()
