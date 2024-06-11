import logging
from typing import Dict, Any, List

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GitHubEntity:

    def __init__(self, token: str):
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }


    def fetch_paginated_data(self, path: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch data from GitHub API with pagination and error handling."""
        results = []
        url = path
        while url:
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                results.extend(data)
                url = response.links.get("next", {}).get("url")
            except Exception as e:
                self.handle_request_exception(e, url)
                break
        return results

    def fetch_single_page_data(self, path: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fetch a single page of data from the GitHub API."""
        try:
            response = requests.get(path, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.handle_request_exception(e, path)
        return {}

    def handle_http_error(self, e: requests.HTTPError, url: str) -> None:
        """Handle specific HTTP errors with appropriate logging."""
        if e.response.status_code == 404:
            logging.error(f'Repository not found: {url}')
        elif e.response.status_code == 401:
            logging.error('Authentication failed: Invalid token')
        else:
            logging.error(f'HTTP error occurred: {e} - Status code: {e.response.status_code}')

    def handle_request_exception(self, e: Exception, url: str) -> None:
        """General exception handler for request-related exceptions."""
        if isinstance(e, requests.HTTPError):
            self.handle_http_error(e, url)
        else:
            logging.exception(f'Failed to make a request to {url}: {e}')

