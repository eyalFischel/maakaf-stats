import logging
from typing import Any, Dict, List

import requests

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GitHubEntity:
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        self.timeout = 10

    def fetch_paginated_data(
        self, path: str, params: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Fetch data from GitHub API with pagination and error handling."""
        results = []
        url = path
        while url:
            try:
                response = requests.get(
                    url, headers=self.headers, params=params, timeout=self.timeout
                )
                response.raise_for_status()
                data = response.json()
                results.extend(data)
                url = response.links.get("next", {}).get("url")
            except requests.exceptions.HTTPError as http_err:
                logging.error(
                    f"HTTP error occurred: {http_err} - Status Code: {response.status_code}"
                )
                break
            except requests.exceptions.ConnectionError as conn_err:
                logging.error(f"Connection error occurred: {conn_err}")
                break
            except requests.exceptions.Timeout as timeout_err:
                logging.error(f"Timeout error occurred: {timeout_err}")
                break
            except requests.exceptions.RequestException as req_err:
                logging.error(f"An error occurred: {req_err}")
                break
        return results

    def fetch_single_page_data(
        self, path: str, params: Dict[str, Any] = None
    ) -> Dict[str, Any]:

        try:
            response = requests.get(
                path, headers=self.headers, params=params, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            logging.error(
                f"HTTP error occurred: {http_err} - Status Code: {response.status_code}"
            )
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"An error occurred: {req_err}")
        return {}
