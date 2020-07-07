from abc import ABCMeta, abstractmethod
from typing import Optional, List, Any, Dict

import requests
from bs4 import BeautifulSoup, Tag

from models.menu import Menu
from models.dish import Dish
from slack_json_builder import create_divider, create_section, create_markdown

db = {}


class AbstractParser(metaclass=ABCMeta):
    restaurant_name: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def get_menu(cls) -> Menu:
        return cls.fetch_from_db() or cls.parse_from_web_and_save_to_db()

    @classmethod
    def fetch_from_db(cls) -> Optional[dict]:
        return db.get(cls.restaurant_name, None)

    @classmethod
    def parse_from_web_and_save_to_db(cls) -> Menu:
        menu = cls.parse_menu()
        # save menu to db
        return menu

    @classmethod
    def parse_menu(cls) -> Menu:
        content = cls.get_page_content()
        main_dishes = cls.parse_main_dishes(content)
        soups = cls.parse_soups(content)
        return Menu(main_dishes, soups)

    @classmethod
    def parse_main_dishes(cls, content: BeautifulSoup) -> List[Dish]:
        main_dish_elements = cls.find_main_dish_elements(content)
        return cls.transform_elements_to_dishes(main_dish_elements)

    @classmethod
    def parse_soups(cls, content: BeautifulSoup) -> List[Dish]:
        soup_elements = cls.find_soup_elements(content)
        return cls.transform_elements_to_dishes(soup_elements)

    @classmethod
    def transform_elements_to_dishes(cls, dish_elements: List[Tag]) -> List[Dish]:
        return list(map(
            lambda element: cls.transform_element_to_dish(element),
            dish_elements
        ))

    @classmethod
    def populate_db(cls, main_dishes: List[Dish], soups: List[Dish]):
        pass

    @classmethod
    def get_page_content(cls) -> BeautifulSoup:
        request = requests.get(cls.url)
        return BeautifulSoup(request.content, 'html.parser')

    @classmethod
    def to_map(cls) -> List[Dict[str, Any]]:
        return [
            create_divider(),
            create_section(create_markdown(f"*<{cls.url}|{cls.restaurant_name}>*")),
            *cls.get_menu().to_map(),
            create_divider()
        ]

    # Methods that should be overwritten
    @classmethod
    @abstractmethod
    def find_main_dish_elements(cls, content: BeautifulSoup):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def find_soup_elements(cls, content: BeautifulSoup):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def transform_element_to_dish(cls, dish_element: Tag) -> Dish:
        raise NotImplementedError
