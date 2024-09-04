# setup.py


from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='all_scraper',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    include_package_data=True,
    description='A simple Python wrapper for the Deezer API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Andryerics/deezer_api',
    author='Andry RL',
    author_email='andryerics@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
