from functools import wraps
import os
from flask_dance.contrib.github import make_github_blueprint
from flask import redirect, url_for
from flask_dance.contrib.github import github

blueprint = make_github_blueprint(
    client_id = os.getenv('OAUTH_CLIENT_ID'),
    client_secret = os.getenv('OAUTH_CLIENT_SECRET'),
)
    
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not github.authorized:
            return redirect(url_for("github.login"))
        else:
            return func(*args, **kwargs)
    return wrapper