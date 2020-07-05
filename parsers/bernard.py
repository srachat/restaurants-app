from typing import Tuple

from bs4 import Tag, BeautifulSoup

from parsers.abstract_parser import AbstractParser, Dish


def transform_dish_to_tuple(dish_element: Tag) -> Tuple[str, str, str]:
    return \
        dish_element.find("strong").text, \
        dish_element.find("span", {"class", "food-alergens"}).text, \
        dish_element.find("span", {"class", "food-price"}).text


class BernardParser(AbstractParser):
    @classmethod
    def parse_main_dishes(cls, content: BeautifulSoup) -> Tuple[Dish, ...]:
        content = cls.get_page_content()

        daily_menu = content.find_all("section", {"class", "daily-menu"})[0]
        dishes = daily_menu.find_all("div", {"class", "single-food"})

        readable_dishes_list = tuple(map(lambda dish: transform_dish_to_tuple(dish), dishes))
        return readable_dishes_list

    @classmethod
    def parse_soups(cls, content: BeautifulSoup) -> Tuple[Dish, ...]:
        return tuple()

    restaurant_name = "bernard"
    url = "https://www.bernardpub.cz/pub/andel"
