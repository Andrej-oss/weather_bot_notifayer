from abc import ABC, abstractmethod
from typing import Dict


class WeatherProvider(ABC):
    @abstractmethod
    def fetch(self) -> Dict:
        pass
