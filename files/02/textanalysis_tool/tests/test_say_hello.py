import sys

sys.path.insert(0, "./src")

from textanalysis_tool import say_hello

result = say_hello.hello("My Name")

if result == "Hello, My Name!":
    print("Test passed!")
else:
    print("Test failed!")
