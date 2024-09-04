import asyncio
import json
import random
import time
from flask import Flask, request, jsonify
from linkapi import UserProfile, CompanyScraper, JobsInfos, Search, AllJobs
from loguru import logger as log

app = Flask(__name__)

# Helper function to run async functions in Flask
def run_async(func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(func)

@app.route('/user', methods=['POST'])
def user_profile():
    """Endpoint to scrape user profile."""
    url = request.form.get('url')
    if not url:
        return "URL is required", 400

    async def scrape_user_profile():
        user_profile = UserProfile(url)
        html_content = await user_profile.fetch_html()
        if not html_content:
            return {"error": "Failed to retrieve HTML content"}, 500

        profile_data = user_profile.parse_profile(html_content)
        return profile_data

    data = run_async(scrape_user_profile())
    return jsonify(data)

@app.route('/company', methods=['POST'])
def company_info():
    """Endpoint to scrape company information."""
    url = request.form.get('url')
    if not url:
        return "URL is required", 400

    async def scrape_company_info():
        scraper = CompanyScraper(url)
        extracted_info = await scraper.fetch_and_save_html()
        return extracted_info if extracted_info else {}

    data = run_async(scrape_company_info())
    return jsonify(data)

@app.route('/jobs', methods=['POST'])
def jobs_info():
    """Endpoint to scrape jobs information."""
    url = request.form.get('url')
    max_pages = int(request.form.get('max_pages', 1))

    async def scrape_jobs_info():
        scraper = JobsInfos(url=url, max_pages=max_pages)
        json_output = await scraper.get_json()  # Renvoie maintenant un objet Python
        return json_output

    data = run_async(scrape_jobs_info())
    return jsonify(data)  # jsonify traite l'objet Python directement

@app.route('/search', methods=['POST'])
def job_search():
    """Endpoint to perform a job search."""
    keyword = request.form.get('keyword')
    location = request.form.get('location')
    max_pages = int(request.form.get('max_pages', 1))

    async def scrape_job_search():
        search = Search()
        job_search_data = await search.scrape_job_search(
            keyword=keyword,
            location=location,
            max_pages=max_pages
        )
        return job_search_data

    data = run_async(scrape_job_search())
    return jsonify(data)

@app.route('/all_jobs', methods=['POST'])
def all_jobs():
    """Endpoint to scrape detailed job information."""
    urls = request.form.getlist('urls')

    async def scrape_all_jobs():
        job_data = await AllJobs.run(urls)
        return job_data

    data = run_async(scrape_all_jobs())
    return jsonify(data)

if __name__ == "__main__":
    # Log message for startup delay
    delay = random.uniform(2, 5)
    log.info(f"Waiting for {delay} seconds before starting...")
    time.sleep(delay)

    # Run the Flask app on host 0.0.0.0 and port 8900
    app.run(host='0.0.0.0', port=8900)
