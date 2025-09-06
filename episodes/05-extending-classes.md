---
title: '05-extending-classes'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

- How do you write a lesson using R Markdown and `{sandpaper}`?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Explain how to use markdown with the new lesson template
- Demonstrate how to include pieces of code, figures, and nested challenge blocks

::::::::::::::::::::::::::::::::::::::::::::::::

## Extending Classes with Inheritance

So far you may be wondering why classes are useful. After all, all we've really done in essence is
make a tiny module with some functions in it that are slightly more complicated than normal
functions. One of the real powers of classes is the ability to limit code duplicate through a
concept called inheritance.

### Inheritance

Inheritance is a way to create a new class that contains all of the same properties and methods as
an existing class, but allows us to add additional new properties and methods, or to override
existing methods. This allows us to create a new class that is a specialized version of an existing
class, without having to rewrite a whole bunch of code.

Taking a look at our Car class from earlier, we might want to create a new class for a specific
type of car, like a Convertable Car. A Convertible Car is a type of Car, so it should have
everything that a Car has, but it also has some additional properties and methods, for example, it
might have a property to indicate whether the roof is up or down. We can create a new class called
ConvertibleCar that inherits from the Car class, and then add the new property and method to it.

```python
class ConvertibleCar(Car):
    def __init__(self, make: str, model: str, year: int, color: str = "grey"):
        super().__init__(make, model, year, color)
        self.roof_is_up = True

    def lower_roof(self) -> None:
        self.roof_is_up = False

    def raise_roof(self) -> None:
        self.roof_is_up = True
```

You can see that the ConvertibleCar class is defined in a similar way to the Car class, but it
inherits from the Car class by including it in parentheses after the class name. The `__init__`
method of the ConvertibleCar class also has a call to `super().__init__()`. The `super()` function
is a way to refer specifically to the parent class, in this case, the Car class. This allows us to
call the `__init__` method of the Car class, which sets up all of the properties that a Car has.

### Appling Inheritance to Our Document Class

For our `Document` class, we have a few different types of documents available from the
Project Gutenberg website. We are currently using plain text files, but there are also HTML files
that we can download. They will have the same information, but the data within will be structured
in a slightly different way. We can use inheritance to create a pair of new classes: `HTMLDocument`
and `PlainTextDocument`, that both inherit from the `Document` class. This will allow us to keep
all of the common functionality in the `Document` class, but to add any additional functionality
specific to each document type.



::::::::::::::::::::::::::::::::::::: keypoints

- Use `.md` files for episodes when you want static content
- Use `.Rmd` files for episodes when you need to generate output
- Run `sandpaper::check_lesson()` to identify any issues with your lesson
- Run `sandpaper::build_lesson()` to preview your lesson locally

::::::::::::::::::::::::::::::::::::::::::::::::

