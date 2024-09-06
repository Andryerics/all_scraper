from setuptools import setup, find_packages

setup(
    name="all_scraper",  # Le nom du package à installer via pip
    version="1.0.0",
    description="Scraper all social network such as : LinkedIn, Tiktok, Instagram, Facebook.....",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Andryerics",
    author_email="andryerics@gmail.com",
    url="https://github.com/Andryerics/all_scraper",  # Le lien vers ton repo GitHub
    packages=find_packages(),  # Trouve automatiquement tous les sous-modules (facebook_api, insta_api, etc.)
    install_requires=[
        "httpx",
        "loguru",
        "httpx[http2]",
        "parsel",
        "lxml"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
