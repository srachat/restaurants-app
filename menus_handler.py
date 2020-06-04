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
    def get_menu(cls) -> Optional[dict]:
        return cls.fetch_from_db() or cls.get_parsed_from_web()

    @classmethod
    def fetch_from_db(cls) -> Optional[dict]:
        return db.get(cls.restaurant_name, None)

    @classmethod
    def get_parsed_from_web(cls) -> Optional[dict]:
        main_dish = cls.parse_main_dish()
        soup = cls.parse_soup()
        cls.populate_db(main_dish, soup)
        return cls.fetch_from_db()

    @classmethod
    @abstractmethod
    def parse_main_dish(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def parse_soup(cls) -> str:
        raise NotImplementedError

    @classmethod
    def populate_db(cls, main_dish: str, soup: str):
        db[cls.restaurant_name] = {
            "main_dish": main_dish,
            "soup": soup,
        }


class FirstParser(MenuParser):
    @classmethod
    def parse_main_dish(cls) -> str:
        pass

    @classmethod
    def parse_soup(cls) -> str:
        pass

    restaurant_name = "restaurant_1"


class SecondParser(MenuParser):
    @classmethod
    def parse_main_dish(cls) -> str:
        pass

    @classmethod
    def parse_soup(cls) -> str:
        pass

    restaurant_name = "restaurant_2"


class ThirdParser(MenuParser):
    @classmethod
    def parse_main_dish(cls) -> str:
        return "this is some other dish"

    @classmethod
    def parse_soup(cls) -> str:
        return "this is some other soup"

    restaurant_name = "restaurant_3"


restaurants_mapping = {
    FirstParser.restaurant_name: FirstParser,
    SecondParser.restaurant_name: SecondParser,
    ThirdParser.restaurant_name: ThirdParser,
}


def restaurant_factory(restaurant_name: str) -> MenuParser:
    return restaurants_mapping.get(restaurant_name, MenuParser)


def create_menu_json(restaurants: str) -> dict:
    separate_restaurants = restaurants.split(" ")
    return {
        restaurant: restaurant_factory(restaurant).get_menu()
        for restaurant in separate_restaurants
        if restaurant in restaurants_mapping.keys()
    }


def main():
    restaurants = "restaurant_1 restaurant_2 restaurant_3 restaurant_4"
    print(db)
    menu = create_menu_json(restaurants)
    print(menu)
    print(db)


if __name__ == "__main__":
    main()
