from abc import ABCMeta, abstractmethod
from typing import Dict, Optional, Tuple, List

import requests
from bs4 import BeautifulSoup

Dish = Tuple[str, str, str]
Menu = Dict[str, List[Dict[str, str]]]

db = {}


class AbstractParser(metaclass=ABCMeta):
    restaurant_name: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def get_menu(cls) -> Optional[Menu]:
        return cls.fetch_from_db() or cls.get_parsed_from_web()

    @classmethod
    def fetch_from_db(cls) -> Optional[dict]:
        return db.get(cls.restaurant_name, None)

    @classmethod
    def get_parsed_from_web(cls) -> Menu:
        menu = cls.parse_menu()
        # save menu to db
        return menu

    @classmethod
    def parse_menu(cls) -> Menu:
        main_dishes = cls.parse_main_dishes_and_convert_to_json()
        soups = cls.parse_soups_and_convert_to_json()
        return cls.create_menu_dict(main_dishes, soups)

    @classmethod
    def parse_main_dishes_and_convert_to_json(cls) -> List[Dict[str, str]]:
        main_dishes = cls.parse_main_dishes()
        return [cls.convert_dish_to_json(dish) for dish in main_dishes]

    @classmethod
    def parse_soups_and_convert_to_json(cls) -> List[Dict[str, str]]:
        soups = cls.parse_soups()
        return [cls.convert_dish_to_json(dish) for dish in soups]

    @classmethod
    def convert_dish_to_json(cls, dish: Dish) -> Dict[str, str]:
        return {
            "name": dish[0],
            "description": dish[1],
            "price": dish[2],
        }

    @classmethod
    def create_menu_dict(cls, main_dishes: List[Dict[str, str]], soups: List[Dict[str, str]]) -> Menu:
        return {
            "main_dishes": main_dishes,
            "soups": soups,
        }

    @classmethod
    @abstractmethod
    def parse_main_dishes(cls) -> Tuple[Dish, ...]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def parse_soups(cls) -> Tuple[Dish, ...]:
        raise NotImplementedError

    @classmethod
    def populate_db(cls, main_dishes: Dict[str, str], soups: Dict[str, str]):
        pass

    @classmethod
    def get_page_content(cls) -> BeautifulSoup:
        request = requests.get(cls.url)
        return BeautifulSoup(request.content, 'html.parser')


