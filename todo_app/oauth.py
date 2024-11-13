from functools import wraps
import os
from flask_dance.contrib.github import make_github_blueprint
from flask import redirect, url_for, session
from flask_dance.contrib.github import github
from flask_dance.consumer import oauth_authorized

from todo_app.data.mongo_db_service import MongoDbService

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

@oauth_authorized.connect
def github_logged_in(blueprint, token):
    if not token:
        session['user_id'] = None
        return False
    response = blueprint.session.get("/user")
    user_id = str(response.json()['id'])
    username = response.json()['login']

    session['user_id'] = user_id
    session['username'] = username
    
    mongodb_service = MongoDbService()
    mongodb_service.add_user_if_new(user_id, username)