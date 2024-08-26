import os
from datetime import datetime
import json

from dotenv import load_dotenv

from database import SessionLocal
from github_repository import RepositoryFetcher
from logging_config import logger
from repository import Repository
from sql_modules import RepositoryORM

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")


def load_repositories_from_json(json_file: str) -> list:
    logger.info(f"Loading repositories from {json_file}")
    with open(json_file, 'r') as file:
        repositories = json.load(file)
    logger.debug(f"Loaded repositories: {repositories}")
    return repositories


def collect_repository_data() -> list:
    """Gets the repositories from the DB and return their stats using the git api"""
    logger.info("Starting to collect repository data.")
    repositories = load_repositories_from_json('maakaf_repos.json')
    repo_data = []

    for repo in repositories:
        try:
            # Initialize RepositoryFetcher with owner and repo name
            repository = Repository(
                owner=repo["owner"], name=repo["name"]
            )
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
            logger.error(f"Failed to fetch data for {repo['owner']}/{repo['name']}: {e}")

    for data in repo_data:
        logger.info(f"Activity for {data['owner']}/{data['name']}: {data['activity']}")

    logger.info("Completed collecting repository data.")
    return repo_data


def insert_repository_data(repo_data: list) -> None:
    """Inserts the repository data into the database"""
    logger.info("Starting to insert repository data into the database.")
    session = SessionLocal()

    try:
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
            logger.debug(f"Added repository {data['name']} to the session.")

        session.commit()
        logger.info("Successfully committed the repository data to the database.")
    except Exception as e:
        logger.error(f"Failed to insert repository data: {e}")
        session.rollback()
    finally:
        session.close()
        logger.info("Database session closed.")
