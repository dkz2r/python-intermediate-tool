from abc import ABC, abstractmethod


class BaseReader(ABC):
    @abstractmethod
    def get_content(self, filepath: str) -> str:
        pass

    @abstractmethod
    def get_metadata(self, filepath: str) -> dict:
        pass
