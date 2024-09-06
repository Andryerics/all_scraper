import setuptools
from setuptools import setup, find_packages  # Ajout de l'import manquant

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="all_scraper",
    version="1.0.0",
    author="Andryerics",
    license="MIT",
    author_email="andryerics@gmail.com",
    description="Scraper all social network such as: LinkedIn, Tiktok, Instagram, Facebook...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Andryerics/all_scraper",
    
    keywords=[
        "facebook-scraper", 
        "facebook-parser", 
        "facebook-crawler",
        "facebook-scraper-without-apikey",
        "instagram-scraper", 
        "instagram-parser", 
        "instagram-crawler",
        "linkedin-scraper", 
        "linkedin-parser", 
        "linkedin-crawler",
        "tiktok-scraper", 
        "tiktok-parser", 
        "tiktok-crawler",
        "xvideos-scraper", 
        "xvideos-parser", 
        "xvideos-crawler"
    ],
    
    project_urls={
        "Bug Tracker": "https://github.com/Andryerics/all_scraper/issues",
        "homepage": "https://www.andryerics.com",
        "issues": "https://github.com/Andryerics/all_scraper/issues",
        "documentation": "https://github.com/Andryerics/all_scraper/blob/main/README.md",
        "repository": "https://github.com/Andryerics/all_scraper/"
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Indonesian",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only"
    ],

    packages=find_packages(),  # Assure-toi d'utiliser l'import correct
    python_requires=">=3.7"
)
