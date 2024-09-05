import json
import asyncio
from typing import Dict, List
from loguru import logger as log
import httpx
from lxml import html
from .headers import get_headers

class JobsInfos:
    """Classe pour scraper les offres d'emploi des pages d'entreprise LinkedIn."""
    
    def __init__(self, url: str, max_pages: int = None):
        self.url = url
        self.max_pages = max_pages
        self.jobs_api_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/" + url.split("jobs/")[-1]

    @staticmethod
    def strip_text(text):
        """Supprime les espaces en trop tout en gérant les valeurs None."""
        return text.strip() if text is not None else text

    @staticmethod
    def parse_jobs(content: str) -> List[Dict]:
        """Parse les données d'emploi des pages d'entreprise LinkedIn en utilisant XPath."""
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
                "salary": JobsInfos.strip_text(element.xpath(".//span[contains(@class, 'salary')]/text()")[0]) if element.xpath(".//span[contains(@class, 'salary')]/text()") else None
            })
        
        return {"data": data, "total_results": total_results}

    async def fetch_page(self, url: str) -> str:
        """Récupère le contenu d'une page unique à partir de l'URL donnée."""
        headers = get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.text

    async def scrape_jobs(self) -> List[Dict]:
        """Scrape les pages d'entreprise LinkedIn et retourne les listes d'emploi."""
        first_page_content = await self.fetch_page(self.url)
        first_page_data = self.parse_jobs(first_page_content)["data"]
        total_results = self.parse_jobs(first_page_content)["total_results"]

        if self.max_pages and self.max_pages * 25 < total_results:
            total_results = self.max_pages * 25

        log.info(f"Scraped the first job page, {total_results // 25 - 1} more pages to go")

        data = first_page_data
        for start_index in range(25, total_results + 25, 25):
            if self.max_pages and len(data) >= self.max_pages * 25:
                break
            paginated_url = f"{self.jobs_api_url}&start={start_index}"
            page_content = await self.fetch_page(paginated_url)
            page_data = self.parse_jobs(page_content)["data"]
            data.extend(page_data)

        log.success(f"Scraped {len(data)} jobs from LinkedIn company job pages")
        return data

    async def save_to_json(self, filename: str):
        """Sauvegarde les résultats dans un fichier JSON."""
        job_search_data = await self.scrape_jobs()
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(job_search_data, file, indent=2, ensure_ascii=False)

    async def get_json(self) -> Dict:
        """Retourne les résultats sous forme d'objet Python."""
        job_search_data = await self.scrape_jobs()
        return job_search_data
        