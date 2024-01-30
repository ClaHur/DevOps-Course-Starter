from flask import Flask, render_template, request
from todo_app.data.session_items import add_item, get_items

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items = get_items())

@app.route("/add_item", methods=["POST"])
def receive_form():
    form_value = request.form["todo"]
    add_item(form_value)
    return render_template('index.html', items = get_items())