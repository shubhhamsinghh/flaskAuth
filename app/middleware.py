import functools
from flask import session, redirect, url_for
from flask_login import current_user, logout_user


# middleware guest
def guest(view_func):
    @functools.wraps(view_func)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('tasks.dashboard'))
        return view_func(*args, **kwargs)
    return decorated
