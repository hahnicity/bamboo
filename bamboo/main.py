"""
bamboo.main
~~~~~~~~~~
"""
from argparse import ArgumentParser
from os import environ

from bamboo.app import create_app
from bamboo.configure import configure_app
from bamboo.connection import make_engine
from bamboo.context import bamboo_context


def build_parser():
    """
    Parse all command line arguments
    """
    parser = ArgumentParser()
    add_app_arguments(parser)
    add_other_arguments(parser)
    return parser


def add_app_arguments(parser):
    """
    Add arguments for where the app will be run
    """
    hosts = parser.add_mutually_exclusive_group()
    hosts.add_argument("--local", help="Launch the app on 127.0.0.1", action="store_true")
    hosts.add_argument("--host", help="Launch the app on a specific host eg: 1.1.1.1")


def add_other_arguments(parser):
    """
    Add other arguments
    """
    others = parser.add_argument_group("Other Options")
    others.add_argument(
        "--debug",
        help="Enable exception logging and reload the app if the source changes",
        action="store_true",
    )
    others.add_argument(
        "--testing",
        help="Enable exception logging and usage of mocks for configuration functions",
        action="store_true",
    )


def main():
    """
    Console Entry point
    """
    args = build_parser().parse_args()
    app = create_app()
    with bamboo_context(engine=make_engine()):
        configure_app(app, args)
        app.run(host=app.config["HOST"], port=environ.get("PORT", 5000))
