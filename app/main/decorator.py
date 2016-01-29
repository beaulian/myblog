from flask import request, abort
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        usename = request.args.get("usename", False)
        password = request.args.get("password", False)
        if usename == "xxx" and password == "xxxx":
            pass
        else:
            abort(403)
        return func(*args, **kwargs)
    return wrapper