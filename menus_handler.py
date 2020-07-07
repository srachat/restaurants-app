from flask import Flask
from flask import request
from parsers import create_menu_json

app = Flask(__name__)


@app.route("/menu", methods=["POST"])
def get_menu():
    restaurants = request.form.get("restaurants", None)
    menu = create_menu_json(restaurants)
    return menu
