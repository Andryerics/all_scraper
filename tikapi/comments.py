import asyncio
import json
from typing import List, Dict
from urllib.parse import urlencode
from httpx import AsyncClient, Response
from loguru import logger as log
import jmespath
from .user_agent import get_random_user_agent

class Comments:
    def __init__(self):
        # initialize an async httpx client
        self.client = AsyncClient(
            http2=True,
            headers={
                "Accept-Language": "en-US,en;q=0.9",
                "User-Agent": get_random_user_agent(),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "content-type": "application/json"
            },
        )

    def parse_comments(self, response: Response) -> List[Dict]:
        """parse comments data from the API response"""
        data = json.loads(response.text)
        comments_data = data["comments"]
        total_comments = data["total"]
        parsed_comments = []
        # refine the comments with JMESPath
        for comment in comments_data:
            result = jmespath.search(
                """{
                text: text,
                comment_language: comment_language,
                digg_count: digg_count,
                reply_comment_total: reply_comment_total,
                author_pin: author_pin,
                create_time: create_time,
                cid: cid,
                nickname: user.nickname,
                unique_id: user.unique_id,
                aweme_id: aweme_id
                }""",
                comment
            )
            parsed_comments.append(result)
        return {"comments": parsed_comments, "total_comments": total_comments}

    async def scrape_comments(self, post_id: int, comments_count: int = 20, max_comments: int = None) -> List[Dict]:
        """scrape comments from tiktok posts using hidden APIs"""

        def form_api_url(cursor: int):
            """form the reviews API URL and its pagination values"""
            base_url = "https://www.tiktok.com/api/comment/list/?"
            params = {
                "aweme_id": post_id,
                'count': comments_count,
                'cursor': cursor # the index to start from      
            }
            return base_url + urlencode(params)

        log.info("scraping the first comments batch")
        first_page = await self.client.get(form_api_url(0))
        data = self.parse_comments(first_page)
        comments_data = data["comments"]
        total_comments = data["total_comments"]

        # get the maximum number of comments to scrape
        if max_comments and max_comments < total_comments:
            total_comments = max_comments

        # scrape the remaining comments concurrently
        log.info(f"scraping comments pagination, remaining {total_comments // comments_count - 1} more pages")
        _other_pages = [
            self.client.get(form_api_url(cursor=cursor))
            for cursor in range(comments_count, total_comments + comments_count, comments_count)
        ]
        for response in asyncio.as_completed(_other_pages):
            response = await response
            data = self.parse_comments(response)["comments"]
            comments_data.extend(data)

        log.success(f"scraped {len(comments_data)} from the comments API from the post with the ID {post_id}")
        return comments_data
        