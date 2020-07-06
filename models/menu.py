from typing import List, Dict, Any

from models.should_be_mapped import ShouldBeMapped
from models.dish import Dish


class Menu(ShouldBeMapped):
	def __init__(self, main_dishes: List[Dish], soups: List[Dish]):
		self.main_dishes = main_dishes
		self.soups = soups

	def to_map(self) -> Dict[str, Any]:
		return {
			"main_dishes": [dish.to_map() for dish in self.main_dishes],
			"soups": [soup.to_map() for soup in self.soups],
		}
