def hello(name: str = "User"):
    if name == "":
        raise ValueError("Name cannot be empty")
    return f"Hello, {name}!"
