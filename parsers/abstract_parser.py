from abc import ABCMeta, abstractmethod
from typing import Dict, Optional, Tuple, List

import requests
from bs4 import BeautifulSoup

Dish = Tuple[str, str, str]
Menu = Dict[str, List[Dict[str, str]]]

db = {}

MAIN_DISHES = "main_dishes"
SOUPS = "soups"


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
        main_dishes = cls.parse_dishes_and_convert_to_json(MAIN_DISHES)
        soups = cls.parse_dishes_and_convert_to_json(SOUPS)
        return cls.create_menu_dict(main_dishes, soups)

    @classmethod
    def parse_dishes_and_convert_to_json(cls, dish_type: str) -> List[Dict[str, str]]:
        content = cls.get_page_content()
        if dish_type == MAIN_DISHES:
            dishes = cls.parse_main_dishes(content)
        elif dish_type == SOUPS:
            dishes = cls.parse_soups(content)
        else:
            raise ValueError(f"Incorrect dish_type provided: {dish_type}. "
                             f"Please provide either {MAIN_DISHES} or {SOUPS}")
        return [cls.convert_dish_to_json(dish) for dish in dishes]

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
            MAIN_DISHES: main_dishes,
            SOUPS: soups,
        }

    @classmethod
    @abstractmethod
    def parse_main_dishes(cls, content: BeautifulSoup) -> Tuple[Dish, ...]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def parse_soups(cls, content: BeautifulSoup) -> Tuple[Dish, ...]:
        raise NotImplementedError

    @classmethod
    def populate_db(cls, main_dishes: Dict[str, str], soups: Dict[str, str]):
        pass

    @classmethod
    def get_page_content(cls) -> BeautifulSoup:
        request = requests.get(cls.url)
        return BeautifulSoup(request.content, 'html.parser')


