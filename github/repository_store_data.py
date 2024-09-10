from datetime import datetime
import json
import os

from dotenv import load_dotenv

from database import SessionLocal
from github_repository import RepositoryFetcher
from logging_config import logger
from repository import Repository
from sql_modules import RepositoryORM, GitHubUserORM

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")
json_file = "maakaf_repos.json"


def load_repositories_from_json(json_file: str) -> list:
    logger.info(f"Loading repositories from {json_file}")
    with open(json_file, "r") as file:
        repositories = json.load(file)
    logger.debug(f"Loaded repositories: {repositories}")
    return repositories


def collect_repository_data() -> list:

    logger.info("Starting to collect repository data.")
    repositories = load_repositories_from_json(json_file)
    repo_data = []

    for repo in repositories:
        try:
            # Initialize RepositoryFetcher with owner and repo name
            repository = Repository(owner=repo["owner"], name=repo["name"])
            repo_fetcher = RepositoryFetcher(repository, github_token)

            # Fetch repository activity
            activity = repo_fetcher.fetch_repository_activity()
            repo_data.append(
                {
                    "owner": repo["owner"],
                    "name": repo["name"],
                    "activity": activity,
                }
            )
            logger.info(f"Successfully fetched data for {repo['owner']}/{repo['name']}")
        except Exception as e:
            logger.error(
                f"Failed to fetch data for {repo['owner']}/{repo['name']}: {e}"
            )

    for data in repo_data:
        logger.info(f"Activity for {data['owner']}/{data['name']}: {data['activity']}")

    logger.info("Completed collecting repository data.")
    return repo_data


def insert_repository_data(repo_data: list) -> None:

    logger.info("Starting to insert repository data into the database.")
    session = SessionLocal()

    try:
        for data in repo_data:
            activity = data["activity"]
            get_user(session, data["owner"])
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
            logger.debug(f"Added repository {data['name']} to the session.")

        session.commit()
        logger.info("Successfully committed the repository data to the database.")
    except Exception as e:
        logger.error(f"Failed to insert repository data: {e}")
        session.rollback()
    finally:
        session.close()
        logger.info("Database session closed.")


def get_user(session, owner_name: str) -> None:

    user = session.query(GitHubUserORM).filter_by(username=owner_name).first()

    # If the user doesn't exist, create a new user
    if not user:
        user = GitHubUserORM(username=owner_name)
        session.add(user)
        session.commit()
        logger.debug(f"Created new user {owner_name} in the database.")
    else:
        logger.debug(f"User {owner_name} found in the database.")

    return user
