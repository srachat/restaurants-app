from typing import Dict, Any

from models.should_be_mapped import ShouldBeMapped
from slack_json_builder import create_markdown


class Dish(ShouldBeMapped):
	def __init__(self, name: str, price: str, description: str):
		self.name = name
		self.price = price
		self.description = description

	def to_map(self) -> Dict[str, Any]:
		return create_markdown(
			text=f"> *{self.name}*\n_{self.price}_\n_{self.description}_\n\n------"
		)
