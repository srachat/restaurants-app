from parsers.abstract_parser import AbstractParser
from parsers.bernard import BernardParser

restaurants_mapping = {
    BernardParser.restaurant_name: BernardParser,
}


def restaurant_factory(restaurant_name: str) -> AbstractParser:
    return restaurants_mapping.get(restaurant_name, AbstractParser)


def create_menu_json(restaurants: str) -> dict:
    if restaurants == "":
        separate_restaurants = list(restaurants_mapping.keys())
    else:
        separate_restaurants = restaurants.split(" ")
    result_blocks = []
    for restaurant in separate_restaurants:
        if restaurant in restaurants_mapping.keys():
            result_blocks.extend(restaurant_factory(restaurant.lower()).to_map())
    return {
        "blocks": result_blocks
    }
