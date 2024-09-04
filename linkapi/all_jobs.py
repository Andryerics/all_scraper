import json
import asyncio
from typing import Dict, List
from loguru import logger as log
import httpx
from lxml import html
from .headers import get_headers

class AllJobs:
    """Classe pour la recherche et l'extraction de données de LinkedIn."""

    @staticmethod
    async def fetch_page(url: str) -> str:
        """Récupère le contenu d'une page à partir de l'URL donnée."""
        headers = get_headers()
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()  # Vérifie qu'aucune erreur HTTP ne s'est produite.
            return response.text

    @staticmethod
    def parse_job_page(content: str) -> Dict:
        """Analyse les données de chaque page de poste LinkedIn."""
        tree = html.fromstring(content)

        # Extraire les données JSON dans le script tag
        script_data = json.loads(tree.xpath("//script[@type='application/ld+json']/text()")[0])

        # Extraire et nettoyer la description du job
        description = []
        for element in tree.xpath("//div[contains(@class, 'show-more')]/ul/li/text()"):
            text = element.replace("\n", "").strip()
            if text:
                description.append(text)

        # Ajouter la description propre dans les données
        script_data["jobDescription"] = description
        script_data.pop("description")  # Supprimer la clé avec le HTML encodé

        return script_data

    @staticmethod
    async def scrape_jobs(urls: List[str]) -> List[Dict]:
        """Scrape LinkedIn job pages asynchronously."""
        tasks = [AllJobs.fetch_page(url) for url in urls]

        data = []
        for task in asyncio.as_completed(tasks):
            content = await task
            data.append(AllJobs.parse_job_page(content))

        log.success(f"Scraped {len(data)} jobs from LinkedIn")
        return data

    @staticmethod
    async def run(urls: List[str]) -> List[Dict]:
        """Exécute le scraping et retourne les résultats."""
        job_data = await AllJobs.scrape_jobs(urls)
        return job_data
        