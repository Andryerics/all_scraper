import asyncio
import json
from typing import List, Dict
from httpx import AsyncClient, Response
from parsel import Selector
from loguru import logger as log
from .user_agent import get_random_user_agent

class User:
    def __init__(self):
        # initialize an async httpx client
        self.client = AsyncClient(
            http2=True,
            headers={
                "Accept-Language": "en-US,en;q=0.9",
                "User-Agent": get_random_user_agent(),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            },
        )

    def parse_profile(self, response: Response):
        """parse profile data from hidden scripts on the HTML"""
        assert response.status_code == 200, "request is blocked, use the ScrapFly codetabs"
        selector = Selector(response.text)
        data = selector.xpath("//script[@id='__UNIVERSAL_DATA_FOR_REHYDRATION__']/text()").get()
        profile_data = json.loads(data)["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
        return profile_data

    async def scrape_profiles(self, urls: List[str]) -> List[Dict]:
        """scrape tiktok profiles data from their URLs"""
        to_scrape = [self.client.get(url) for url in urls]
        data = []
        # scrape the URLs concurrently
        for response in asyncio.as_completed(to_scrape):
            response = await response
            profile_data = self.parse_profile(response)
            data.append(profile_data)
        log.success(f"scraped {len(data)} profiles from profile pages")
        return data
