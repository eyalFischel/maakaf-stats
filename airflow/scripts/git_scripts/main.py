from database import init_db
from repository_store_data import collect_repository_data, insert_repository_data


def main():
    # Initialize the database
    init_db()

    # Collect repository data
    repo_data = collect_repository_data()

    # Insert the collected data into the database
    insert_repository_data(repo_data)


main()
