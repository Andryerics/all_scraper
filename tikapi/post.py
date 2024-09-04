# tikapi/post.py

import jmespath
import asyncio
import json
from typing import List, Dict
from httpx import AsyncClient, Response
from parsel import Selector
from loguru import logger as log
from .user_agent import get_random_user_agent

class Post:
    def __init__(self):
        self.client = AsyncClient(
            http2=True,
            headers={
                "Accept-Language": "en-US,en;q=0.9",
                "User-Agent": get_random_user_agent(),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            },
        )

    def parse_post(self, response: Response) -> Dict:
        """parse hidden post data from HTML"""
        assert response.status_code == 200, "request is blocked, use the ScrapFly codetabs"
        selector = Selector(response.text)
        data = selector.xpath("//script[@id='__UNIVERSAL_DATA_FOR_REHYDRATION__']/text()").get()
        post_data = json.loads(data)["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]
        parsed_post_data = jmespath.search(
            """{
            id: id,
            desc: desc,
            createTime: createTime,
            video: video.{duration: duration, ratio: ratio, cover: cover, playAddr: playAddr, downloadAddr: downloadAddr, bitrate: bitrate},
            author: author.{id: id, uniqueId: uniqueId, nickname: nickname, avatarLarger: avatarLarger, signature: signature, verified: verified},
            stats: stats,
            locationCreated: locationCreated,
            diversificationLabels: diversificationLabels,
            suggestedWords: suggestedWords,
            contents: contents[].{textExtra: textExtra[].{hashtagName: hashtagName}}
            }""",
            post_data
        )
        return parsed_post_data

    async def scrape_posts(self, urls: list[str]) -> list[dict]:
        """scrape tiktok posts data from their URLs"""
        to_scrape = [self.client.get(url) for url in urls]
        data = []
        for response in asyncio.as_completed(to_scrape):
            response = await response
            post_data = self.parse_post(response)
            data.append(post_data)
        log.success(f"scraped {len(data)} posts from post pages")
        return data
