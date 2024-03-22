from time import sleep
from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import TrelloService

from todo_app.flask_config import Config
from todo_app.models import ListNames, ViewModel

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    trello_service = TrelloService()

    def reload_index():
        trello_service.clear_cache()
        return redirect('/')

    @app.route('/')
    def index():
        try:
            item_view_model = ViewModel(trello_service.get_items(), trello_service.get_lists())
            list_names = ListNames()
            return render_template('index.html', view_model=item_view_model, list_names=list_names)
        except Exception as e:
            # An exception will occur if the cached lists don't match the list IDs in .env
            # In this case we clear the cache and reload
            return reload_index()

    @app.route("/add_item", methods=["POST"])
    def add_item():
        item_name = request.form["todo"]
        trello_service.add_item(item_name)
        return redirect('/')

    @app.route("/update_status", methods=["POST"])
    def update_card():
        item_id = request.json['itemId']
        new_status = request.json['newStatus']
        trello_service.update_status(item_id, new_status)
        return redirect('/')

    @app.route("/delete_item", methods=["POST"])
    def delete_item():
        item_id = request.json['itemId']
        trello_service.delete_item(item_id)
        return redirect('/')
    
    return app