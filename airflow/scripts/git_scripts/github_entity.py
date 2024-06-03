from typing import Dict, Any, List

import requests


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
            response = requests.get(url, headers=self.headers, params=params)
            if response.ok:
                data = response.json()
                results.extend(data)
                # Check if there's a 'next' page link and update the url, otherwise break the loop
                links = response.links
                if "next" in links:
                    url = links["next"]["url"]
                else:
                    break
            else:
                print(f"Failed to fetch data: {response.status_code} - {response.text}")
                break
        return results

    def fetch_single_page_data(self, path, params: Dict[str, Any] = None) -> Dict[str, Any]:
        response = requests.get(path, headers=self.headers, params=params)
        return response.json()
