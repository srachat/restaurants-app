from parsers.abstract_parser import AbstractParser
from parsers.bernard import BernardParser

restaurants_mapping = {
    BernardParser.restaurant_name: BernardParser,
}


def restaurant_factory(restaurant_name: str) -> AbstractParser:
    return restaurants_mapping.get(restaurant_name, AbstractParser)


def create_menu_json(restaurants: str) -> dict:
    separate_restaurants = restaurants.split(" ")
    return {
        restaurant: restaurant_factory(restaurant).get_menu().to_map()
        for restaurant in separate_restaurants
        if restaurant in restaurants_mapping.keys()
    }
