"""
bamboo.controllers
~~~~~~~~~~~~~~~~~
"""
from functools import wraps

from flask import request
from ujson import dumps

from bamboo import dbhandlers
from bamboo.constants import DUE_FIELDS, PAYMENT_FIELDS
from bamboo.exceptions import (
    BAD_REQUEST_ERRORS,
    CONFLICT_ERRORS,
    FieldNotFoundError,
    NoIDError,
    NoUserError
)
from bamboo.thirdparty import get_facebook_user


def handle_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BAD_REQUEST_ERRORS as error:
            return dumps({"response": error.message}), 400
        except CONFLICT_ERRORS as error:
            return dumps({"response": error.message}), 409
    return wrapper


def create_routes(app):
    @app.route("/login", methods=["GET"])
    @handle_request
    def login():
        """
        Handle login for customers to the app
        """
        username = _get_username()
        id = dbhandlers.handle_login(get_facebook_user(username))
        return dumps({"response": {"id": id}})

    @app.route("/viewbyfriend", methods=["GET"])
    @handle_request
    def view_dues_by_friend():
        """
        View all dues owed to/by a friend to a customer
        """
        id = _get_id("id")
        friend_id = _get_id("friend_id")
        separate_dues = dbhandlers.handle_view_dues_by_friend(id, friend_id)
        return dumps({"response": separate_dues})

    @app.route("/view", methods=["GET"])
    @handle_request
    def view_dues():
        """
        View all dues owed to/from customer
        """
        id = _get_id("id")
        dues_by_customer = dbhandlers.handle_view_dues(id)
        return dumps({"response": dumps(dues_by_customer)})

    @app.route("/due", methods=["POST"])
    @handle_request
    def new_due():
        """
        Create a new due
        """
        _validate_fields(DUE_FIELDS)
        dbhandlers.handle_new_due(request.form)
        return dumps({"response": "success"})

    @app.route("/payinfull", methods=["POST"])
    @handle_request
    def pay_in_full():
        """
        Pay a friend in full
        """
        _validate_fields(PAYMENT_FIELDS)
        dbhandlers.handle_pay_in_full(request.form)
        return dumps({"response": "success"})


    def  _get_id(key):
        """
        Get a user id from a GET request
        """
        id = request.args.get(key)
        if not id:
            raise NoIDError()
        else:
            return id

    def _get_username():
        """
        Get a username from a GET request
        """
        username = request.args.get("username")
        if not username:
            raise NoUserError()
        else:
            return username

    def _validate_fields(fields):
        """
        Validate that correct parameters for a POST request were sent
        """
        for field in fields:
            if field not in request.form:
                raise FieldNotFoundError(field)
