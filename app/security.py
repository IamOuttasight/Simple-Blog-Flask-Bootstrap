from functools import wraps
from flask import session
from flask import flash
from flask import redirect
from flask import url_for


def is_logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized. Please, log in', 'danger')
            return redirect(url_for('login'))
    return wrapper

# NOTE: modify me
def is_author(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return
        # if 'logged_in' in session:
        #     return f(*args, **kwargs)
        # else:
        #     flash('Unauthorized. Please, log in', 'danger')
        #     return redirect(url_for('login'))
    return wrapper