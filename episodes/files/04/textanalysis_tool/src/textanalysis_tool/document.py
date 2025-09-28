import re


class Document:

    CONTENT_PATTERN = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*(.*?)\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"

    def __init__(self, filepath: str, title: str = "", author: str = "", id: int = 0):
        self.filepath = filepath
        self.content = self.get_content(filepath)

        self.title = title
        self.author = author
        self.id = id

    def get_content(self, filepath: str) -> str:
        raw_text = self.read(filepath)
        if not raw_text:
            raise ValueError(f"File {filepath} contains no content.")

        if isinstance(raw_text, bytes):
            raise ValueError(f"File {self.filepath} is not a valid text file.")

        match = re.search(self.CONTENT_PATTERN, raw_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        raise ValueError(f"File {filepath} is not a valid Project Gutenberg Text file.")

    def read(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def get_line_count(self) -> int:
        return len(self.content.splitlines())

    def get_word_occurrence(self, word: str) -> int:
        return self.content.lower().count(word.lower())
