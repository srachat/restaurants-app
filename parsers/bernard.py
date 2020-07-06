from typing import List

from bs4 import Tag, BeautifulSoup

from models.dish import Dish
from parsers.abstract_parser import AbstractParser


class BernardParser(AbstractParser):
    @classmethod
    def find_main_dish_elements(cls, content: BeautifulSoup) -> List[Tag]:
        daily_menu = content.find_all("section", {"class", "daily-menu"})[0]
        dish_elements = daily_menu.find_all("div", {"class", "single-food"})
        return dish_elements

    @classmethod
    def find_soup_elements(cls, content: BeautifulSoup) -> List[Tag]:
        return []

    @classmethod
    def transform_element_to_dish(cls, dish_element: Tag) -> Dish:
        name = dish_element.find("strong").text
        price = dish_element.find("span", {"class", "food-price"}).text
        description = dish_element.find("span", {"class", "food-alergens"}).text
        return Dish(name, price, description)

    restaurant_name = "bernard"
    url = "https://www.bernardpub.cz/pub/andel"
