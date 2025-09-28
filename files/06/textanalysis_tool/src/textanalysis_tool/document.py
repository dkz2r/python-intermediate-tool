from textanalysis_tool.readers.base_reader import BaseReader


class Document:
    @property
    def gutenberg_url(self) -> str | None:
        if self.id:
            return f"https://www.gutenberg.org/cache/epub/{self.id}/pg{self.id}.txt"
        return None

    @property
    def line_count(self) -> int:
        return len(self.content.splitlines())

    def __init__(self, filepath: str, reader: BaseReader):
        self.filepath = filepath
        self.content = reader.get_content(filepath)

        metadata = reader.get_metadata(filepath)
        self.title = metadata.get("title")
        self.author = metadata.get("author")
        self.id = metadata.get("id")

    def get_word_occurrence(self, word: str) -> int:
        return self.content.lower().count(word.lower())
