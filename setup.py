#!/usr/bin/env python
from setuptools import setup, find_packages

__version__ = "0.1"


setup(
    name="bamboo",
    author="Gregory Rehm",
    author_email="grehm87@gmail.com",
    version=__version__,
    description="A Flask+SQLAlchemy backend for PandaPayments",
    packages=find_packages(),
    package_data={"*": ["*.html"]},
    entry_points={
        "console_scripts": [
            "bamboo=bamboo.main:main",
        ],
    },
    install_requires=[
        "flask",
        "flask-heroku",
        "flask-sqlalchemy",
        "ProxyTypes>=0.9,<1.0",
        "psycopg2",
        "requests",
        "sqlalchemy",
        "ujson",
    ],
)
