"""
bamboo.app
~~~~~~~~~~~~~~~~~
"""
from flask import Flask


def create_app():
    """
    Factory function for creating an app
    """
    return Flask(__name__)
