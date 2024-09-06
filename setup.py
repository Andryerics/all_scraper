import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name = "all_scraper",
  version = "1.0.0",
  author = "Andryerics",
  author_email = "andryerics@gmail.com",
  description = "Scraper all social network such as : LinkedIn, Tiktok, Instagram, Facebook.....",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  url = "https://github.com/Andryerics/all_scraper",
  project_urls = {
    "Bug Tracker": "package issues URL",
    "homepage": "https://www.andryerics.com",
    "issues": "https://github.com/Andryerics/all_scraper/issues",
    "documentation": "https://github.com/Andryerics/all_scraper/blob/main/README.md",
    "repository" = "https://github.com/Andryerics/all_scraper/",
      
  },
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  package_dir = {"": "src"},
  packages = setuptools.find_packages(where="src"),
  python_requires = ">=3.6"
)
