"""
bamboo.configure
~~~~~~~~~~~~~~~
"""
import os

from flask.ext.heroku import Heroku

from bamboo.controllers import create_routes


def configure_app(app, args):
    """
    Configure the application's behavior
    """
    app.debug = args.debug
    app.testing = args.testing
    app.config["HOST"] = get_host(args)

    # Configure DB for Heroku/Testing
    configure_database(app)

    # Create all application controllers
    create_routes(app)


def configure_database(app):
    """
    Configure our database client when we are testing locally
    """
    if app.testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    else:
        Heroku(app)

def get_host(args):
    """
    Configure the host string to run our app on
    """
    if args.host:
        return args.host
    else:
        return {
            True: "127.0.0.1",
            False: "0.0.0.0"
        }[args.local]
