import sys

sys.path.insert(0, "src")

from textanalysis_tool.document import Document
from textanalysis_tool.plain_text_document import PlainTextDocument
from textanalysis_tool.html_document import HTMLDocument

# Test the PlainTextDocument class
plain_text_doc = PlainTextDocument(filepath="scratch/pg2680.txt")
print(f"Plain Text Document Title: {plain_text_doc.title}")
print(f"Plain Text Document Author: {plain_text_doc.author}")
print(f"Plain Text Document ID: {plain_text_doc.id}")
print(f"Plain Text Document Line Count: {plain_text_doc.line_count}")
print(f"Plain Text Document 'the' Occurrences: {plain_text_doc.get_word_occurrence('the')}")
print(f"Plain Text Document Gutenberg URL: {plain_text_doc.gutenberg_url}")
print(f"Type of Plain Text Document: {type(plain_text_doc)}")
print(f"Parent Class: {type(plain_text_doc).__bases__[0]}")

print("=" * 40)

# Test the HTMLDocument class
html_doc = HTMLDocument(filepath="scratch/pg2680-images.html")
print(f"HTML Document Title: {html_doc.title}")
print(f"HTML Document Author: {html_doc.author}")
print(f"HTML Document ID: {html_doc.id}")
print(f"HTML Document Line Count: {html_doc.line_count}")
print(f"HTML Document 'the' Occurrences: {html_doc.get_word_occurrence('the')}")
print(f"HTML Document Gutenberg URL: {html_doc.gutenberg_url}")
print(f"Type of HTML Document: {type(html_doc)}")
print(f"Parent Class: {type(html_doc).__bases__[0]}")

print("=" * 40)

# We can't use the Document class directly
doc = Document(filepath="scratch/pg2680.txt")