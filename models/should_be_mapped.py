from abc import ABCMeta, abstractmethod
from typing import Any, Dict


class ShouldBeMapped(metaclass=ABCMeta):
	@abstractmethod
	def to_map(self) -> Dict[str, Any]:
		raise NotImplementedError
