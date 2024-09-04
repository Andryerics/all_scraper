import json
import httpx
import asyncio
from lxml import html
from loguru import logger as log
from typing import Dict
from bs4 import BeautifulSoup
from .headers import get_headers

class UserProfile:
    def __init__(self, url: str):
        self.url = url

    async def fetch_html(self) -> str:
        """Télécharger le contenu HTML d'une page web et le renvoyer sous forme de chaîne."""
        headers = get_headers()

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(self.url, headers=headers)
            if response.status_code == 403:
                log.error(f"Access forbidden (403) for URL: {self.url}")
                return ""
            response.raise_for_status()  # Raise an error for bad responses (e.g., 404)
            html_content = response.text

        # Utiliser BeautifulSoup pour structurer le HTML
        soup = BeautifulSoup(html_content, "html.parser")
        prettified_html = soup.prettify()

        return prettified_html

    def parse_profile(self, html_content: str) -> Dict:
        """Analyser les données du profil à partir du contenu HTML brut."""
        tree = html.fromstring(html_content)

        # Extraction des informations de profil
        first_name = tree.xpath("//meta[@property='profile:first_name']/@content")
        last_name = tree.xpath("//meta[@property='profile:last_name']/@content")
        cover_photo_url = tree.xpath("//div[contains(@class, 'cover-img__image-frame')]//img/@src")
        profile_photo_url = tree.xpath("//div[contains(@class, 'top-card__profile-image-container')]//img/@data-delayed-url")
        full_name = tree.xpath("//h1[contains(@class, 'top-card-layout__title')]/text()")
        bio_location = tree.xpath("//div[contains(@class, 'profile-info-subheader')]//span[1]/text()")
        followers = tree.xpath("//div[contains(@class, 'profile-info-subheader')]//span[contains(text(), 'followers')]/text()")
        connections = tree.xpath("//div[contains(@class, 'profile-info-subheader')]//span[contains(text(), 'connections')]/text()")

        # Nettoyage des valeurs
        first_name = first_name[0] if first_name else ''
        last_name = last_name[0] if last_name else ''
        cover_photo_url = cover_photo_url[0] if cover_photo_url else ''
        profile_photo_url = profile_photo_url[0] if profile_photo_url else ''
        full_name = full_name[0].strip() if full_name else ''
        bio_location = bio_location[0].strip() if bio_location else ''
        followers = followers[0].replace('followers', '').strip() if followers else ''
        connections = connections[0].replace('connections', '').strip() if connections else ''

        # Extraction des articles
        articles = []
        article_elements = tree.xpath("//section[@class='core-section-container core-section-container--with-border border-b-1 border-solid border-color-border-faint py-4 articles' and @data-section='articles']//ul/li")

        for element in article_elements:
            image_url = element.xpath(".//img/@data-delayed-url")[0] if element.xpath(".//img/@data-delayed-url") else ''
            title = element.xpath(".//h3[contains(@class, 'base-main-card__title')]/text()")[0].strip() if element.xpath(".//h3[contains(@class, 'base-main-card__title')]/text()") else ''
            author = element.xpath(".//h4[contains(@class, 'base-main-card__subtitle')]//a/text()")[0].strip() if element.xpath(".//h4[contains(@class, 'base-main-card__subtitle')]//a/text()") else ''
            date = element.xpath(".//div[contains(@class, 'base-main-card__metadata')]//span/text()")[0].strip() if element.xpath(".//div[contains(@class, 'base-main-card__metadata')]//span/text()") else ''

            articles.append({
                "image_url": image_url,
                "title": title,
                "author": author,
                "date": date
            })

        # Extraction des activités
        activities = []
        activity_elements = tree.xpath("//section[@class='core-section-container core-section-container--with-border border-b-1 border-solid border-color-border-faint py-4 activities' and @data-section='posts']//ul/li")

        for element in activity_elements:
            image_url = element.xpath(".//img/@data-delayed-url")[0] if element.xpath(".//img/@data-delayed-url") else ''
            title = element.xpath(".//h3[contains(@class, 'base-main-card__title')]/text()")[0].strip() if element.xpath(".//h3[contains(@class, 'base-main-card__title')]/text()") else ''
            shared_by = element.xpath(".//h4[contains(@class, 'base-main-card__subtitle')]//a/text()")[0].strip() if element.xpath(".//h4[contains(@class, 'base-main-card__subtitle')]//a/text()") else ''
            activity_url = element.xpath(".//a[contains(@class, 'base-card__full-link')]/@href")[0] if element.xpath(".//a[contains(@class, 'base-card__full-link')]/@href") else ''

            activities.append({
                "image_url": image_url,
                "title": title,
                "shared_by": shared_by,
                "activity_url": activity_url
            })

        # Extraction des "more activities"
        more_activities = []
        more_activity_elements = tree.xpath("//section[@class='core-section-container core-section-container--with-border border-b-1 border-solid border-color-border-faint py-4 activities' and @data-section='posts']//ul/li")

        for element in more_activity_elements:
            image_url = element.xpath(".//img/@data-delayed-url")[0] if element.xpath(".//img/@data-delayed-url") else ''
            title = element.xpath(".//h3[contains(@class, 'base-main-card__title')]/text()")[0].strip() if element.xpath(".//h3[contains(@class, 'base-main-card__title')]/text()") else ''
            shared_by = element.xpath(".//h4[contains(@class, 'base-main-card__subtitle')]//a/text()")[0].strip() if element.xpath(".//h4[contains(@class, 'base-main-card__subtitle')]//a/text()") else ''
            activity_url = element.xpath(".//a[contains(@class, 'base-card__full-link')]/@href")[0] if element.xpath(".//a[contains(@class, 'base-card__full-link')]/@href") else ''

            more_activities.append({
                "image_url": image_url,
                "title": title,
                "shared_by": shared_by,
                "activity_url": activity_url
            })

        # Extraction des données du JSON-LD (si nécessaire)
        json_ld = tree.xpath("//script[@type='application/ld+json']/text()")
        json_data = json.loads(json_ld[0]) if json_ld else {}

        # Inclure toutes les données extraites dans le résultat final
        profile_data = {
            "first_name": first_name,
            "last_name": last_name,
            "cover_photo_url": cover_photo_url,
            "profile_photo_url": profile_photo_url,
            "full_name": full_name,
            "bio_location": bio_location,
            "followers": followers,
            "connections": connections,
            "articles": articles,
            "activities": activities,
            "more_activities": more_activities,
            "json_ld_full": json_data
        }

        return profile_data
