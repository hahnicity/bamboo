"""
bamboo.controllers
~~~~~~~~~~~~~~~~~
"""
from flask import request
from ujson import dumps

from bamboo.dbhandlers import handle_login, handle_new_due, handle_view_dues
from bamboo.constants import DUE_FIELDS
from bamboo.exceptions import (
    FieldNotFoundError, NoIDError, NoUserError, StatusCodeError
)
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
            return dumps({"response": error.message})
        else:
            return dumps({"response": {"id": id}})

    @app.route("/view", methods=["GET"])
    def view_dues():
        """
        Create a payment for a user
        """
        try:
            id = _get_id()
            dues_by_customer = handle_view_dues(id)
        except Exception as error:
            return dumps({"response": error.message})
        else:
            return dumps({"response": dumps(dues_by_customer)})

    @app.route("/due", methods=["POST"])
    def new_due():
        """
        Create a new payment
        """
        try:
            _validate_due_fields()
            handle_new_due(request.form)
        except Exception as error:
            return dumps({"response": error.message})
        else:
            return dumps({"response": "success"})

    def  _get_id():
        id = request.args.get("id")
        if not id:
            raise NoIDError()
        else:
            return id

    def _get_username():
        username = request.args.get("username")
        if not username:
            raise NoUserError()
        else:
            return username

    def _validate_due_fields():
        for field in DUE_FIELDS:
            if field not in request.form:
                raise FieldNotFoundError(field)
