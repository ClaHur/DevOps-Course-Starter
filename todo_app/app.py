from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import TrelloService

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())
trello_service = TrelloService()

@app.route('/')
def index():
    return render_template('index.html', items = trello_service.get_items(), lists = trello_service.get_lists())

@app.route("/add_item", methods=["POST"])
def receive_form():
    form_value = request.form["todo"]
    trello_service.add_item(form_value)
    return redirect('/')

@app.route("/update_status", methods=["POST"])
def receive_update_form():
    item_id = request.json['itemId']
    is_checked = request.json['isChecked']
    trello_service.update_status(item_id, is_checked)
    return redirect('/')