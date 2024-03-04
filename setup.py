from setuptools import setup, find_packages

setup(
    name='APWikipedia',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-restful",
        "nltk",
        "flask_cors"
    ],
    entry_points={
        'console_scripts': [
        ],
    },
)
