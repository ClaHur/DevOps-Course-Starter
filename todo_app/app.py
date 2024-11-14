from flask import Flask, render_template, request, redirect, session, jsonify
from todo_app.data.mongo_db_service import MongoDbService
from werkzeug.middleware.proxy_fix import ProxyFix

from todo_app.flask_config import Config
from todo_app.models import ListNames, ViewModel, ViewModelUsers
from todo_app.oauth import blueprint, login_required

def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(Config())
    app.register_blueprint(blueprint, url_prefix="/login")
    mongodb_service = MongoDbService()

    @app.route('/')
    @login_required
    def index():
        item_view_model = ViewModel(mongodb_service.get_items(session['user_id']))
        list_names = ListNames()
        user_is_admin = mongodb_service.check_admin_user(session['user_id'])
        return render_template('index.html', view_model=item_view_model, list_names=list_names, username=session['username'], show_admin_link = user_is_admin)
    
    @app.route('/admin')
    @login_required
    def admin():
        user_is_admin = mongodb_service.check_admin_user(session['user_id'])
        if not user_is_admin:
            return render_template('unauthorised.html')
        users_view_model = ViewModelUsers(mongodb_service.get_users())
        return render_template('admin.html', view_model=users_view_model)
    
    @app.route('/unauthorised')
    def unauthorised():
        return render_template('unauthorised.html')

    @app.route("/add_item", methods=["POST"])
    @login_required
    def add_item():
        item_name = request.form["todo"]
        mongodb_service.add_item(item_name, session['user_id'])
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
    
    @app.route("/delete_user", methods=["POST"])
    @login_required
    def delete_user():
        user_id = request.json['userId']
        deleteUser = mongodb_service.delete_user(user_id, session['user_id'])
        if deleteUser == True:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, error="Unauthorized or deletion failed"), 403
    
    @app.route("/toggle_admin", methods=["POST"])
    @login_required
    def toggle_admin():
        user_id = request.json['userId']
        toggleAdmin = mongodb_service.toggle_admin(user_id, session['user_id'])
        if toggleAdmin == True:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, error="Unauthorized or toggle failed"), 403
    
    return app