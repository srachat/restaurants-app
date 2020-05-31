from pprint import pprint
from typing import Dict

from bs4 import BeautifulSoup
from bs4.element import Tag
import requests


def transform_dish_to_dict(dish_element: Tag) -> Dict[str, str]:
    return {
        "name": dish_element.find("strong").text,
        "description": dish_element.find("span", {"class", "food-alergens"}).text,
        "price": dish_element.find("span", {"class", "food-price"}).text,
    }


request = requests.get("https://www.bernardpub.cz/pub/andel")
soup = BeautifulSoup(request.content, 'html.parser')

daily_menu = soup.find_all("section", {"class", "daily-menu"})[0]
dishes = daily_menu.find_all("div", {"class", "single-food"})

readable_dishes_list = list(map(lambda dish: transform_dish_to_dict(dish), dishes))
pprint(readable_dishes_list)
