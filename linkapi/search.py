# linkapi/search.py

import asyncio
from typing import Dict, List
from loguru import logger as log
from urllib.parse import urlencode, quote_plus
import httpx
from lxml import html
from .headers import get_headers

class Search:
    def __init__(self):
        pass

    async def fetch_page(self, url: str) -> str:
        """Fetch a single page content from the given URL."""
        headers = get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()  # Assurez-vous qu'aucune erreur HTTP ne s'est produite.
            return response.text

    def parse_job_search(self, content: str) -> List[Dict]:
        """Parse job data from job search pages using XPath."""
        tree = html.fromstring(content)
        total_results = tree.xpath("//span[contains(@class, 'job-count')]/text()")
        total_results = int(total_results[0].replace(",", "").replace("+", "")) if total_results else None

        data = []
        for element in tree.xpath("//section[contains(@class, 'results-list')]/ul/li"):
            data.append({
                "title": element.xpath(".//div/a/span/text()")[0].strip() if element.xpath(".//div/a/span/text()") else None,
                "company": element.xpath(".//div/div[contains(@class, 'info')]/h4/a/text()")[0].strip() if element.xpath(".//div/div[contains(@class, 'info')]/h4/a/text()") else None,
                "address": element.xpath(".//div/div[contains(@class, 'info')]/div/span/text()")[0].strip() if element.xpath(".//div/div[contains(@class, 'info')]/div/span/text()") else None,
                "timeAdded": element.xpath(".//div/div[contains(@class, 'info')]/div/time/@datetime")[0] if element.xpath(".//div/div[contains(@class, 'info')]/div/time/@datetime") else None,
                "jobUrl": element.xpath(".//div/a/@href")[0].split("?")[0] if element.xpath(".//div/a/@href") else None,
                "companyUrl": element.xpath(".//div/div[contains(@class, 'info')]/h4/a/@href")[0].split("?")[0] if element.xpath(".//div/div[contains(@class, 'info')]/h4/a/@href") else None,
                "salary": self.strip_text(element.xpath(".//span[contains(@class, 'salary')]/text()")[0]) if element.xpath(".//span[contains(@class, 'salary')]/text()") else None
            })
        
        return {"data": data, "total_results": total_results}

    def strip_text(self, text):
        """Remove extra spaces while handling None values."""
        return text.strip() if text is not None else text

    async def scrape_job_search(self, keyword: str, location: str, max_pages: int = None) -> List[Dict]:
        """Scrape LinkedIn job search pages and return job listings."""

        def form_urls_params(keyword, location):
            """Form the job search URL params."""
            params = {
                "keywords": quote_plus(keyword),
                "location": location,
            }
            return urlencode(params)

        first_page_url = "https://www.linkedin.com/jobs/search?" + form_urls_params(keyword, location)
        first_page_content = await self.fetch_page(first_page_url)
        first_page_data = self.parse_job_search(first_page_content)["data"]
        total_results = self.parse_job_search(first_page_content)["total_results"]

        # Si un nombre maximum de pages est défini, limiter le nombre total de résultats en conséquence
        if max_pages and max_pages * 25 < total_results:
            total_results = max_pages * 25
        
        log.info(f"Scraped the first job page, {total_results // 25 - 1} more pages to go")
        
        other_pages_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?"
        data = first_page_data
        
        for start_index in range(25, total_results + 25, 25):
            if max_pages and len(data) >= max_pages * 25:
                break
            paginated_url = f"{other_pages_url}{form_urls_params(keyword, location)}&start={start_index}"
            page_content = await self.fetch_page(paginated_url)
            page_data = self.parse_job_search(page_content)["data"]
            data.extend(page_data)

        log.success(f"Scraped {len(data)} jobs from LinkedIn job search")
        return data
        