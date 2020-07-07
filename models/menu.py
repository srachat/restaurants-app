from typing import List, Dict, Any

from models.should_be_mapped import ShouldBeMapped
from models.dish import Dish
from slack_json_builder import create_section, create_markdown, create_element_of_type


class Menu(ShouldBeMapped):
	def __init__(self, main_dishes: List[Dish], soups: List[Dish]):
		self.main_dishes = main_dishes
		self.soups = soups

	def to_map(self) -> List[Dict[str, Any]]:
		return [
			create_section(create_markdown("`Main dishes`")),
			create_element_of_type(
				"section",
				"fields",
				[dish.to_map() for dish in self.main_dishes] or [create_markdown("No main dishes available")]
			),
			create_section(create_markdown("`Soups`")),
			create_element_of_type(
				"section",
				"fields",
				[soup.to_map() for soup in self.soups] or [create_markdown("No soups available")]
			),
		]
