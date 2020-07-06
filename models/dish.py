from typing import Dict, Any

from models.should_be_mapped import ShouldBeMapped


class Dish(ShouldBeMapped):
	def __init__(self, name: str, price: str, description: str):
		self.name = name
		self.price = price
		self.description = description

	def to_map(self) -> Dict[str, Any]:
		return {
			"name": self.name,
			"price": self.price,
			"description": self.description
		}
