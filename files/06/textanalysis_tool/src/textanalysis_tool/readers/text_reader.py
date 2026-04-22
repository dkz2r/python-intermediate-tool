import re

from .base_reader import BaseReader


class TextReader(BaseReader):
    TITLE_PATTERN = r"^Title:\s*(.*?)\s*$"
    AUTHOR_PATTERN = r"^Author:\s*(.*?)\s*$"
    ID_PATTERN = r"^Release date:\s*.*?\[eBook #(\d+)\]"
    CONTENT_PATTERN = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*(.*?)\*\*\* END OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"

    def read(self, filepath: str) -> str:
        with open(filepath, encoding="utf-8") as file_obj:
            return file_obj.read()

    def _extract_metadata_element(self, pattern: str, text: str) -> str | None:
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return None

    def get_content(self, filepath: str) -> str:
        raw_text = self.read(filepath)
        match = re.search(self.CONTENT_PATTERN, raw_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        raise ValueError(f"File {filepath} is not a valid Project Gutenberg Text file.")

    def get_metadata(self, filepath: str) -> dict:
        raw_text = self.read(filepath)

        title = self._extract_metadata_element(self.TITLE_PATTERN, raw_text)
        author = self._extract_metadata_element(self.AUTHOR_PATTERN, raw_text)
        extracted_id = self._extract_metadata_element(self.ID_PATTERN, raw_text)

        return {
            "title": title,
            "author": author,
            "id": int(extracted_id) if extracted_id else None,
        }
