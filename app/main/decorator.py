# -*- coding: utf-8 -*-
from flask import request, abort
from functools import wraps
from app import mongo

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = request.args.get("username", False)
        password = request.args.get("password", False)
        user = mongo.db.users.find_one_or_404()
        if username == user["username"] and password == user["password"]:
            pass
        else:
            abort(403)
        return func(*args, **kwargs)
    return wrapper