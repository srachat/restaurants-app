from flask import Flask
from flask import request
from parsers import create_menu_json

app = Flask(__name__)


@app.route("/menu")
def get_menu():
    restaurants = request.form["restaurants"]
    menu = create_menu_json(restaurants)
    return menu
