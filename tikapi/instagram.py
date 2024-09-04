# tikapi/instagram.py

import json
import httpx
from .user_agent import get_random_user_agent

class InstagramScraper:
    def __init__(self):
        self.client = httpx.Client(
            headers={
                "x-ig-app-id": "936619743392459",
                "User-Agent": get_random_user_agent(),
                "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept": "*/*",
            }
        )

    def scrape_user(self, username: str):
        """Scrape Instagram user's data"""
        result = self.client.get(
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}",
        )
        data = json.loads(result.content)
        return data["data"]["user"]
        