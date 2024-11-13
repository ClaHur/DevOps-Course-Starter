from flask import Flask, render_template, request, redirect
from todo_app.data.mongo_db_service import MongoDbService

from todo_app.flask_config import Config
from todo_app.models import ListNames, ViewModel
from todo_app.oauth import blueprint, login_required

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.register_blueprint(blueprint, url_prefix="/login")
    mongodb_service = MongoDbService()

    @app.route('/')
    @login_required
    def index():
        item_view_model = ViewModel(mongodb_service.get_items())
        list_names = ListNames()
        return render_template('index.html', view_model=item_view_model, list_names=list_names)

    @app.route("/add_item", methods=["POST"])
    @login_required
    def add_item():
        item_name = request.form["todo"]
        mongodb_service.add_item(item_name)
        return redirect('/')

    @app.route("/update_status", methods=["POST"])
    @login_required
    def update_item():
        item_id = request.json['itemId']
        new_status = request.json['newStatus']
        mongodb_service.update_status(item_id, new_status)
        return redirect('/')

    @app.route("/delete_item", methods=["POST"])
    @login_required
    def delete_item():
        item_id = request.json['itemId']
        mongodb_service.delete_item(item_id)
        return redirect('/')
    
    return app