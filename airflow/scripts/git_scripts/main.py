from database import init_db

from logging_config import logger
from repository_store_data import collect_repository_data, insert_repository_data

def main():
    try:
        logger.info("Initializing the database")
        init_db()

        logger.info("Collecting repository data")
        repo_data = collect_repository_data()

        logger.info("Inserting repository data into the database")
        insert_repository_data(repo_data)
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
