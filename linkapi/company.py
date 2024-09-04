import httpx
import uuid
import os
import asyncio
from lxml import html
from bs4 import BeautifulSoup
from loguru import logger as log
from .headers import get_headers

class CompanyScraper:
    def __init__(self, url, cookies=None):
        self.url = url
        self.cookies = cookies if cookies else {}

    async def fetch_and_save_html(self) -> dict:
        """Télécharger le contenu HTML d'une page web et extraire les informations pertinentes."""
        headers = get_headers()
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response = await client.get(self.url, headers=headers, cookies=self.cookies)
                if response.status_code == 403:
                    log.error(f"Access forbidden (403) for URL: {self.url}")
                    return {}
                response.raise_for_status()  # Raise an error for bad responses (e.g., 404)
                html_content = response.text
            except httpx.RequestError as exc:
                log.error(f"An error occurred while requesting {exc.request.url!r}.")
                return {}

        # Extraire les informations
        extracted_info = self.extract_information(html_content)
        return extracted_info

    def extract_information(self, html_content: str) -> dict:
        """Extrait les informations pertinentes de la page HTML."""
        tree = html.fromstring(html_content)

        # Extraction des informations principales
        cover_photo = tree.xpath("//figure[@class='cover-img']//img[@class='cover-img__image']/@src")
        profile_photo = tree.xpath("//img[contains(@class, 'top-card-layout__entity-image')]/@data-delayed-url")
        company_name = tree.xpath("//h1[contains(@class, 'top-card-layout__title')]/text()")
        category = tree.xpath("//h2[contains(@class, 'top-card-layout__headline')]/text()")
        location = tree.xpath("//h3[contains(@class, 'top-card-layout__first-subline')]/text()[1]")
        followers = tree.xpath("//h3[contains(@class, 'top-card-layout__first-subline')]/span/following-sibling::text()")
        about = tree.xpath("//p[@data-test-id='about-us__description']/text()")
        website = tree.xpath("//div[@data-test-id='about-us__website']//a/@href")
        industry = tree.xpath("//div[@data-test-id='about-us__industry']//dd/text()")
        company_size = tree.xpath("//div[@data-test-id='about-us__size']//dd/text()")
        headquarters = tree.xpath("//div[@data-test-id='about-us__headquarters']//dd/text()")
        organization_type = tree.xpath("//div[@data-test-id='about-us__organizationType']//dd/text()")
        specialties = tree.xpath("//div[@data-test-id='about-us__specialties']//dd/text()")

        # Nettoyage des données
        location = location[0].strip() if location else None
        followers = followers[0].strip() if followers else None
        about = about[0].strip() if about else None
        website = website[0].strip() if website else None
        industry = industry[0].strip() if industry else None
        company_size = company_size[0].strip() if company_size else None
        headquarters = headquarters[0].strip() if headquarters else None
        organization_type = organization_type[0].strip() if organization_type else None
        specialties = specialties[0].strip() if specialties else None

        # Extraction des employés
        employees = self.extract_employees(html_content, tree)

        return {
            "cover_photo": cover_photo[0] if cover_photo else None,
            "profile_photo": profile_photo[0] if profile_photo else None,
            "company_name": company_name[0].strip() if company_name else None,
            "category": category[0].strip() if category else None,
            "location": location,
            "followers": followers,
            "about": about,
            "website": website,
            "industry": industry,
            "company_size": company_size,
            "headquarters": headquarters,
            "organization_type": organization_type,
            "specialties": specialties,
            "employees": employees  # Ajout de la liste des employés
        }

    def extract_employees(self, html_content: str, tree) -> list:
        """Extrait la liste des employés de la page HTML."""
        employees = []
        employee_elements = tree.xpath("//section[@data-test-id='employees-at']//li")
        soup = BeautifulSoup(html_content, 'html.parser')

        for i, employee in enumerate(employee_elements):
            # Extraire et nettoyer le nom de l'employé avec bs4
            name_tag = soup.select("section[data-test-id='employees-at'] li")[i].select_one("h3.base-main-card__title")
            name = name_tag.get_text(strip=True) if name_tag else "N/A"

            # Extraire et nettoyer le titre du poste de l'employé avec bs4
            title_tag = soup.select("section[data-test-id='employees-at'] li")[i].select_one("h4.base-main-card__subtitle")
            title = title_tag.get_text(strip=True) if title_tag else "N/A"

            # Extraire le lien vers le profil LinkedIn avec XPath
            profile_link_elements = employee.xpath(".//a/@href")
            profile_link = profile_link_elements[0].strip() if profile_link_elements else "N/A"

            # Extraire l'URL de l'image de l'employé avec XPath
            image_url_elements = employee.xpath(".//img/@data-delayed-url")
            image_url = image_url_elements[0].strip() if image_url_elements else "N/A"

            # Ajouter l'employé à la liste
            employees.append({
                "name": name,
                "title": title,
                "profile_link": profile_link,
                "image_url": image_url
            })

        return employees
        