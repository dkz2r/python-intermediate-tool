import sys

sys.path.insert(0, "./src")

from textanalysis_tool.document import Document

total_tests = 3
passed_tests = 0
failed_tests = 0

# Check that we can create a Document object
doc = Document(filepath="tests/example_file.txt", title="Test Document")
if doc.title == "Test Document" and doc.filepath == "tests/example_file.txt":
    passed_tests += 1
else:
    failed_tests += 1

# Test the methods
if doc.get_line_count() == 2:
    passed_tests += 1
else:
    failed_tests += 1

if doc.get_word_occurrence("test") == 2:
    passed_tests += 1
else:
    failed_tests += 1

print(f"Total tests: {total_tests}")
print(f"Passed tests: {passed_tests}")
print(f"Failed tests: {failed_tests}")
