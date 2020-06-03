from abc import ABCMeta, abstractmethod
from typing import Optional


db = {
    "restaurant_1": {
        "main_dish": "main_dish_1",
        "soup": "soup_1",
    },
    "restaurant_2": {
        "main_dish": "main_dish_2",
        "soup": "soup_2",
    },
}


class MenuParser(metaclass=ABCMeta):
    restaurant_name = None

    @classmethod
    def get_menu(cls) -> str:
        return cls.fetch_from_db() or cls.parse_from_web()

    @classmethod
    def fetch_from_db(cls) -> Optional[dict]:
        return db.get(cls.restaurant_name, None)

    @classmethod
    @abstractmethod
    def parse_from_web(cls):
        raise NotImplementedError


class FirstParser(MenuParser):
    restaurant_name = "restaurant_1"

    @classmethod
    def parse_from_web(cls):
        pass


class SecondParser(MenuParser):
    restaurant_name = "restaurant_2"

    @classmethod
    def parse_from_web(cls):
        pass


class ThirdParser(MenuParser):
    restaurant_name = "restaurant_3"

    @classmethod
    def parse_from_web(cls):
        db[cls.restaurant_name] = {
            "main_dish": "another_variant",
            "soup": "another",
        }
        return db[cls.restaurant_name]


class MenuFactory:
    restaurants_mapping = {
        FirstParser.restaurant_name: FirstParser,
        SecondParser.restaurant_name: SecondParser,
        ThirdParser.restaurant_name: ThirdParser,
    }

    @staticmethod
    def factory(restaurant_name: str) -> MenuParser:
        return MenuFactory.restaurants_mapping.get(restaurant_name, MenuParser)


class MenuDispatcher:
    @staticmethod
    def create_menu_json(restaurants: str) -> dict:
        separate_restaurants = restaurants.split(" ")
        return {
            restaurant: MenuFactory.factory(restaurant).get_menu()
            for restaurant in separate_restaurants
            if restaurant in MenuFactory.restaurants_mapping.keys()
        }


def main():
    restaurants = "restaurant_1 restaurant_2 restaurant_3 restaurant_4"
    menu = MenuDispatcher.create_menu_json(restaurants)
    print(menu)


if __name__ == "__main__":
    main()
