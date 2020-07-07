from typing import Optional

from flask import Flask
from flask import request
from parsers import create_menu_json

app = Flask(__name__)


def get_menu(restaurants: Optional[str]):
    menu = create_menu_json(restaurants)
    return menu


@app.route("/menu", methods=["POST"])
def get_menu_normal_request():
    restaurants = request.form.get("restaurants", None)
    return get_menu(restaurants)


@app.route("/slack/menu", methods=["POST"])
def get_menu_slack_request():
    restaurants = request.form.get("text", None)
    return get_menu(restaurants)
