"""
bamboo.controllers
~~~~~~~~~~~~~~~~~
"""
from flask import request
from ujson import dumps

from bamboo.dbhandlers import handle_login, handle_view_dues
from bamboo.exceptions import NoUserError, StatusCodeError
from bamboo.oauth import get_user


def create_routes(app):
    @app.route("/login", methods=["GET"])
    def login():
        """
        Handle login for customers to the app
        """
        try:
            username = _get_username()
            id = handle_login(get_user(username))
        except Exception as error:
            return dumps({"response": error})
        else:
            return dumps({"response": {"id": id}})

    @app.route("/view", methods=["GET"])
    def view_dues():
        """
        Create a payment for a user
        """
        try:
            id = request.args.get("id")
            dues_by_customer = handle_view_dues(id)
        except Exception as error:
            return dumps({"response": error})
        else:
            return dumps({"response": dumps(dues_by_customer)})

    def _get_username():
        username = request.args.get("username")
        if not username:
            raise NoUserError()
        else:
            return username
