"""
bamboo.controllers
~~~~~~~~~~~~~~~~~
"""
from flask import request
from ujson import dumps

from bamboo.dbhandlers import (
    handle_login,
    handle_new_due,
    handle_pay_in_full,
    handle_view_dues,
    handle_view_dues_by_friend
)
from bamboo.constants import DUE_FIELDS, PAYMENT_FIELDS
from bamboo.exceptions import (
    FieldNotFoundError,
    NoIDError,
    NoUserError,
    StatusCodeError
)
from bamboo.thirdparty import get_facebook_user


def create_routes(app):
    @app.route("/login", methods=["GET"])
    def login():
        """
        Handle login for customers to the app
        """
        try:
            username = _get_username()
            id = handle_login(get_facebook_user(username))
        except Exception as error:
            return dumps({"response": error.message}), 400
        else:
            return dumps({"response": {"id": id}})

    @app.route("/viewbyfriend", methods=["GET"])
    def view_dues_by_friend():
        """
        View all dues owed to/by a friend to a customer
        """
        try:
            id = _get_id("id")
            friend_id = _get_id("friend_id")
            separate_dues = handle_view_dues_by_friend(id, friend_id)
        except Exception as error:
            return dumps({"response": error.message}), 400
        else:
            return dumps({"response": separate_dues})

    @app.route("/view", methods=["GET"])
    def view_dues():
        """
        View all dues owed to/from customer
        """
        try:
            id = _get_id("id")
            dues_by_customer = handle_view_dues(id)
        except Exception as error:
            return dumps({"response": error.message}), 400
        else:
            return dumps({"response": dumps(dues_by_customer)})

    @app.route("/due", methods=["POST"])
    def new_due():
        """
        Create a new due
        """
        try:
            _validate_due_fields()
            handle_new_due(request.form)
        except Exception as error:
            return dumps({"response": error.message}), 400
        else:
            return dumps({"response": "success"})

    @app.route("/payinfull", methods=["POST"])
    def pay_in_full():
        """
        Pay a friend in full
        """
        try:
            _validate_payment_fields()
            handle_pay_in_full(request.form)
        except Exception as error:
            return dumps({"response": error.message}), 400
        else:
            return dumps({"response": "success"})


    def  _get_id(key):
        id = request.args.get(key)
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

    def _validate_payment_fields():
        for field in PAYMENT_FIELDS:
            if field not in request.form:
                raise FieldNotFoundError(field)
