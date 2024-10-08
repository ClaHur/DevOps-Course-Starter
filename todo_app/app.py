from time import sleep
from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import MongoDbService

from todo_app.flask_config import Config
from todo_app.models import ListNames, ViewModel

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    mongodb_service = MongoDbService()

    @app.route('/')
    def index():
        item_view_model = ViewModel(mongodb_service.get_items(), mongodb_service.get_lists())
        list_names = ListNames()
        return render_template('index.html', view_model=item_view_model, list_names=list_names)

    @app.route("/add_item", methods=["POST"])
    def add_item():
        item_name = request.form["todo"]
        mongodb_service.add_item(item_name)
        return redirect('/')

    @app.route("/update_status", methods=["POST"])
    def update_card():
        item_id = request.json['itemId']
        new_status = request.json['newStatus']
        mongodb_service.update_status(item_id, new_status)
        return redirect('/')

    @app.route("/delete_item", methods=["POST"])
    def delete_item():
        item_id = request.json['itemId']
        mongodb_service.delete_item(item_id)
        return redirect('/')
    
    return app