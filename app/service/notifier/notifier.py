from abc import ABC, abstractmethod


class Notifier(ABC):

    @abstractmethod
    async def send(self, recipient: str, message: str):
        pass
