from flask import Flask, jsonify, request
import asyncio
import json
from tikapi import User, Post, Comments, InstagramScraper

app = Flask(__name__)

# Route /user pour scraper les profils TikTok
@app.route('/user', methods=['POST'])
def scrape_user():
    urls = request.form.getlist("urls")  # Récupérer les URLs comme liste depuis le formulaire

    async def scrape_profiles(urls):
        user = User()
        result = await user.scrape_profiles(urls=urls)
        return result

    result = asyncio.run(scrape_profiles(urls))
    return jsonify(result)

# Route /post pour scraper les posts TikTok
@app.route('/post', methods=['POST'])
def scrape_post():
    urls = request.form.getlist("urls")  # Récupérer les URLs comme liste depuis le formulaire

    async def scrape_posts(urls):
        post = Post()
        result = await post.scrape_posts(urls=urls)
        return result

    result = asyncio.run(scrape_posts(urls))
    return jsonify(result)

# Route /comments pour scraper les commentaires TikTok
@app.route('/comments', methods=['POST'])
def scrape_comments():
    post_id = request.form.get("post_id")  # Récupérer l'ID du post depuis le formulaire
    max_comments = int(request.form.get("max_comments", 100))  # Valeur par défaut : 100
    comments_count = int(request.form.get("comments_count", 20))  # Valeur par défaut : 20

    async def scrape_comments(post_id, max_comments, comments_count):
        comments_scraper = Comments()
        result = await comments_scraper.scrape_comments(
            post_id=post_id,
            max_comments=max_comments,
            comments_count=comments_count
        )
        return result

    result = asyncio.run(scrape_comments(post_id, max_comments, comments_count))
    return jsonify(result)

# Route /insta pour scraper les données d'utilisateur Instagram
@app.route('/insta', methods=['POST'])
def scrape_insta():
    username = request.form.get("username")  # Récupérer le nom d'utilisateur depuis le formulaire

    def scrape_instagram_user(username):
        scraper = InstagramScraper()
        result = scraper.scrape_user(username)
        return result

    result = scrape_instagram_user(username)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8900)
