import setuptools
from pinscrape._version import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as req:
    reqs = req.read().split("\n")

setuptools.setup(
    name="all_scraper",
    version=__version__,
    author="Andryerics",
    author_email="andryerics@gmail.com",
    description="Scraper all social network such as : LinkedIn, Tiktok, Instagram, Facebook.....",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Andryerics/all_scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=reqs,
)
