from abc import ABC, abstractmethod


class Document(ABC):
    @property
    def gutenberg_url(self) -> str | None:
        if self.id:
            return f"https://www.gutenberg.org/cache/epub/{self.id}/pg{self.id}.txt"
        return None

    @property
    def line_count(self) -> int:
        return len(self.content.splitlines())

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.content = self.get_content(filepath)

        self.metadata = self.get_metadata(filepath)
        self.title = self.metadata.get("title")
        self.author = self.metadata.get("author")
        self.id = self.metadata.get("id")

    def get_word_occurrence(self, word: str) -> int:
        return self.content.lower().count(word.lower())

    @abstractmethod
    def get_content(self, filepath: str) -> str:
        pass

    @abstractmethod
    def get_metadata(self, filepath: str) -> dict[str, str | None]:
        pass
