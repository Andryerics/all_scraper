import requests
from .base_url import BASE_URL_TIKTOK, BASE_URL_BETABOTZ, BASE_URL_BILIBILI, BASE_URL_DOUYIN, HEADERS
from .exception import APITimeoutException, APIHTTPErrorException, GeneralAPIException

class Scraper:
    def api_request(self, base_url, endpoint, params=None, headers=None, timeout=10):
        """
        Fonction générique pour effectuer des requêtes API, gérer les exceptions et les logs.

        Args:
        - base_url: L'URL de base (par exemple, TikTok, Douyin, Bilibili ou Betabotz).
        - endpoint: Le chemin de l'API à appeler (ajouté à base_url).
        - params: Les paramètres de la requête.
        - headers: Les en-têtes HTTP, optionnels.
        - timeout: Temps d'attente maximal pour la requête.

        Returns:
        - Le contenu JSON de la réponse en cas de succès, ou un message d'erreur détaillé.
        """
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            raise APITimeoutException("La requête a expiré.")
        
        except requests.exceptions.HTTPError as http_err:
            raise APIHTTPErrorException(f"Erreur HTTP {response.status_code} : {response.text}")
        
        except requests.exceptions.RequestException as err:
            raise GeneralAPIException(f"Erreur : {err}")

    # Fonctions spécifiques aux API TikTok
    def fetch_post_comment(self, aweme_id, cursor=100, count=20):
        """
        Récupère les commentaires d'un post TikTok.
        """
        params = {'aweme_id': aweme_id, 'cursor': cursor, 'count': count}
        return self.api_request(BASE_URL_TIKTOK, "fetch_post_comment", params=params, headers=HEADERS)

    def fetch_user_profile(self, unique_id):
        """
        Récupère le profil utilisateur TikTok en fonction de l'identifiant unique.
        """
        params = {'uniqueId': unique_id}
        return self.api_request(BASE_URL_TIKTOK, "fetch_user_profile", params=params, headers=HEADERS)

    def fetch_post_comment_reply(self, item_id, comment_id, cursor=0, count=20):
        """
        Récupère les réponses à un commentaire sur un post TikTok.
        """
        params = {'item_id': item_id, 'comment_id': comment_id, 'cursor': cursor, 'count': count}
        return self.api_request(BASE_URL_TIKTOK, "fetch_post_comment_reply", params=params, headers=HEADERS)

    def get_sec_user_id(self, url_encoded):
        """
        Récupère le sec_user_id depuis une URL TikTok encodée.
        """
        params = {'url': url_encoded}
        return self.api_request(BASE_URL_TIKTOK, "get_sec_user_id", params=params, headers=HEADERS)

    def get_aweme_id(self, url_encoded):
        """
        Récupère l'aweme_id (ID de la vidéo) depuis une URL TikTok encodée.
        """
        params = {'url': url_encoded}
        return self.api_request(BASE_URL_TIKTOK, "get_aweme_id", params=params, headers=HEADERS)

    def get_unique_id(self, url_encoded):
        """
        Récupère l'unique_id (ID de l'utilisateur) depuis une URL TikTok encodée.
        """
        params = {'url': url_encoded}
        return self.api_request(BASE_URL_TIKTOK, "get_unique_id", params=params, headers=HEADERS)

    def fetch_user_follow(self, sec_uid, count=10, max_cursor=0, min_cursor=0):
        """
        Récupère la liste des followers d'un utilisateur TikTok.
        """
        params = {
            'secUid': sec_uid,
            'count': count,
            'maxCursor': max_cursor,
            'minCursor': min_cursor
        }
        return self.api_request(BASE_URL_TIKTOK, "fetch_user_follow", params=params, headers=HEADERS)

    # Fonctions spécifiques pour les API Betabotz (TikTok Downloader, Instagram Stalker, Xvideos Downloader et Recherche)
    def download_tiktok_video(self, url):
        """
        Télécharge une vidéo TikTok via l'URL fournie.
        """
        params = {'url': url}
        return self.api_request(BASE_URL_BETABOTZ, "tiktokdl", params=params)

    def stalk_instagram_profile(self, username):
        """
        Scrape un profil Instagram via le nom d'utilisateur fourni.
        """
        params = {'q': username}
        return self.api_request(BASE_URL_BETABOTZ, "stalk-ig", params=params)

    def download_xvideos_video(self, url):
        """
        Télécharge une vidéo Xvideos via l'URL fournie.
        """
        params = {'url': url}
        return self.api_request(BASE_URL_BETABOTZ, "xvideosdl", params=params)

    def search_xvideos(self, query):
        """
        Recherche des vidéos sur Xvideos via une requête texte.
        """
        params = {'q': query}
        return self.api_request(BASE_URL_BETABOTZ, "xvideosearch", params=params)

    # Fonctions spécifiques aux API Bilibili
    def fetch_bilibili_video_comments(self, bv_id, pn=1):
        """
        Récupère les commentaires d'une vidéo Bilibili via bv_id et numéro de page (pn).
        """
        params = {'bv_id': bv_id, 'pn': pn}
        return self.api_request(BASE_URL_BILIBILI, "fetch_video_comments", params=params)

    def fetch_bilibili_comment_reply(self, bv_id, pn=1, rpid=None):
        """
        Récupère les réponses à un commentaire sur une vidéo Bilibili via bv_id, numéro de page (pn) et l'ID du commentaire (rpid).
        """
        params = {'bv_id': bv_id, 'pn': pn, 'rpid': rpid}
        return self.api_request(BASE_URL_BILIBILI, "fetch_comment_reply", params=params)

    # Fonctions spécifiques à l'API Douyin
    def fetch_user_profile_douyin(self, sec_user_id):
        """
        Récupère le profil utilisateur Douyin en fonction du sec_user_id.
        """
        params = {'sec_user_id': sec_user_id}
        return self.api_request(BASE_URL_DOUYIN, "fetch_user_profile", params=params, headers=HEADERS)

    def fetch_user_post_videos(self, sec_user_id):
        """
        Récupère les vidéos postées par un utilisateur Douyin.
        """
        params = {'sec_user_id': sec_user_id}
        return self.api_request(BASE_URL_DOUYIN, "fetch_user_post_videos", params=params, headers=HEADERS)

    def fetch_video_comments(self, aweme_id, cursor=0, count=20):
        """
        Récupère les commentaires sur une vidéo Douyin.
        """
        params = {'aweme_id': aweme_id, 'cursor': cursor, 'count': count}
        return self.api_request(BASE_URL_DOUYIN, "fetch_video_comments", params=params, headers=HEADERS)

    def fetch_video_comment_replies(self, item_id, comment_id, cursor=0, count=20):
        """
        Récupère les réponses aux commentaires sur une vidéo Douyin.
        """
        params = {'item_id': item_id, 'comment_id': comment_id, 'cursor': cursor, 'count': count}
        return self.api_request(BASE_URL_DOUYIN, "fetch_video_comment_replies", params=params, headers=HEADERS)

    def get_aweme_id_douyin(self, url_encoded):
        """
        Récupère l'aweme_id (ID de la vidéo) depuis une URL Douyin encodée.
        """
        params = {'url': url_encoded}
        return self.api_request(BASE_URL_DOUYIN, "get_aweme_id", params=params, headers=HEADERS)
        