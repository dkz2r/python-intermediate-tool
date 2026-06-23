---
title: 'Iterables and Generators'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

- What is an iterable in Python?
- What is a generator in Python?
- How can I succinctly create a list or dictionary in Python?
- What are sets and how can I use them in Python?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Understand what makes an object iterable in Python.
- Learn how to create and use generators in Python.
- Understand the difference between iterables and generators.
- Learn how to use set operations.
- Understand how a `defaultdict` works and how to use it.

::::::::::::::::::::::::::::::::::::::::::::::::

## What is an Iterable?

This might be a new term, but you've certainly been working with iterables as soon as you started
learning python. Anything that you can loop over in a `for` loop is an iterable, so this includes
basic data structures like lists, tuples, and dictionaries, as well as strings.

::: callout

More specifically, an iterable is any Python object that implements the `__iter__()` method, which
returns an iterator. An iterator is an object that implements the `__next__()` method, which
returns the next item in the sequence when called.

:::

### What's happening under the hood?

You may have heard that in python "Everything is an object". This is true, and it means that even
basic data structures like lists and dictionaries are actually objects that have their own defined
methods and attributes. You've probably already used some of these methods, like when you use
`my_list.append(1)` to add an item to a list or `"my_string".upper()` to convert a string to
uppercase.

The convention in python is to use the `__` (double underscore) to denote special methods that are
not intended to be called directly by the user. These are often called "dunder" methods (short for
"double underscore"). When you use a `for` loop to iterate over an iterable, Python is actually
calling the `__iter__()` method of the iterable to get an iterator, and then calling the `__next__()`
method of the iterator to get each item in the sequence.

We can test this in action by creating a simple list and using these methods directly:

```python
my_list = [1, 2, 3]

# Get an iterator from the list
my_iterator = my_list.__iter__()
print(my_iterator)  # This will print the iterator object

# Get the next item from the iterator
print(my_iterator.__next__())  # This will print 1
print(my_iterator.__next__())  # This will print 2
```

## List Comprehensions

Say we wanted to create a list of the squares of the numbers from 0 to 9. We could do this with a
`for` loop like this:

```python
squared = []
for x in range(10):
    squared.append(x**2)
```

However there's a more concise way to do this using what's called a list comprehension:

```python
squared = [x**2 for x in range(10)]
```

What's going on here? This is called a list comprehension, and it's a concise way to create lists.
The syntax is `[expression for item in iterable]`, where `expression` is the value that will be
added to the list for each `item` in the `iterable`.

List comprehensions can also include an optional `if` statement to filter items from the iterable.
For example, if we only wanted the squares of the even numbers from 0 to 9, we could do this:

```python
squared = [x**2 for x in range(10) if x % 2 == 0]
```

List comprehensions are very useful for creating lists, but if overused or used in complex ways,
they can make your code harder to read. It's important to strike a balance between conciseness and
readability.

## Dictionary Comprehensions

Related to list comprehensions are dictionary comprehensions, which allow you to create dictionaries
in a similar way. The syntax for a dictionary comprehension is
`{key_expression: value_expression for item in iterable}`.

```python
squared_dict = {x: x**2 for x in range(10)}
```

## `zip` and `enumerate`

We can iterate over a dictionary using a for loop like this:

```python
my_dict = {'a': 1, 'b': 2, 'c': 3}
for key, value in my_dict.items():
    print(key, value)
```

This works because the `items()` method of a dictionary returns an iterable of key-value pairs.
The `zip` function is a built-in function that allows you to iterate over multiple iterables at the
same time. It takes two or more iterables as arguments and returns an iterator that produces tuples
containing the corresponding elements from each iterable.

```python
x_values = ["a", "b", "c"]
y_values = [1, 2, 3]

for x, y in zip(x_values, y_values):
    print(x, y)
```

The `enumerate` function is related, as it allows you to iterate over an iterable while keeping
track of the index of the current item. It takes an iterable as an argument and returns an iterator
that produces tuples containing the index and the corresponding item from the iterable.

```python
my_list = ['a', 'b', 'c']
for index, value in enumerate(my_list):
    print(index, value)
```

## Generator Functions

A generator is a special type of iterable that allows you to generate values on the fly, rather
than storing them all in memory all at once. This can be extremely useful when working with large
data, or when you want to create an infinite sequence of values.

You can create a generator using a generator function, which is defined like a normal function but
uses the `yield` keyword instead of `return`. When you call a generator function, it returns a
generator object, which is an iterator that can be used to iterate over the values generated by the
function.

Here's an example of a simple generator function that performs a countdown:

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1
    yield "Blast off!"
```

When you call this function, it returns a generator object:

```python
counter = countdown(5)
print(counter)
```

```
<generator object countdown at 0x000001238D3EBDC0>
```

But if we call this generator in a `for` loop, it will yield the values one at a time:

```python
for number in countdown(5):
    print(number)
```

```
5
4
3
2
1
Blast off!
```

We can also use the `next()` function to get the next value from the generator:

```python
counter = countdown(5)
print(next(counter))  # This will print 5
print(next(counter))  # This will print 4
```

::: callout

Generator Comprehensions

Just like we have list comprehensions and dictionary comprehensions, we also have generator
comprehensions. The syntax for a generator comprehension is similar to a list comprehension, but
it uses parentheses instead of square brackets:

```python
squared_gen = (x**2 for x in range(10))
```

This creates a generator that will yield the squares of the numbers from 0 to 9. You can iterate
over this generator in a `for` loop or use the `next()` function to get the next value.

:::

## Sets and Set Operations

A set is an unordered collection of unique elements. In Python, you can create a set using the
`set()` function or by using curly braces `{}`. For example:

```python
my_set = {1, 2, 3}
```

Sets work just like lists, but they have some important differences that makes them very useful in
certain situations:

- Sets are unordered, which means that the elements in a set do not have a specific order. This means
  that you cannot access elements in a set using an index like you can with a list.
- Sets do not allow duplicate elements. If you try to add a duplicate element to a set, it will simply
  be ignored.
- Sets support mathematical set operations like union, intersection, difference, and symmetric
  difference.

This makes sets very useful for tasks like removing duplicates from a list, checking for membership,
and checking for overlap between two collections of data.

For a toy example, let's say we are running a survey asking people what their favorite fruit is, and
we want to find out just how many different fruits are in the list. We can use a set to do this:

```python
fruit_survey_1 = ["apple", "banana", "orange", "apple", "grape", "banana"]
survey_1_set = set(fruit_survey_1)
print(survey_1_set)
```

```
{'grape', 'banana', 'orange', 'apple'}
```

Then, let's imagine we perform the survey again with a different group of people, and we want to
compare the results to see which fruits are popular across both surveys. We can use set operations
to do this:

```python
fruit_survey_2 = ["banana", "kiwi", "grape", "melon", "orange", "kiwi"]
survey_2_set = set(fruit_survey_2)

# Find the union of the two sets (all fruits from both surveys)
all_unique_fruits = survey_1_set.union(survey_2_set)
print("Fruits in either survey:", all_unique_fruits)

# Find the intersection of the two sets (fruits that are in both surveys)
common_fruits = survey_1_set.intersection(survey_2_set)
print("Fruits in both surveys:", common_fruits)

# Find only the fruits that are in survey 1 but not in survey 2
unique_to_survey_1 = survey_1_set.difference(survey_2_set)
print("Fruits only in survey 1:", unique_to_survey_1)
```

Output:
```
Fruits in either survey: {'banana', 'kiwi', 'apple', 'melon', 'grape', 'orange'}
Fruits in both surveys: {'banana', 'orange', 'grape'}
Fruits only in survey 1: {'apple'}
```

::::::::::::::::::::::::::::::::::::: challenge

## Challenge: Write a Dictionary Comprehension

Convert the following list of tuples into a dictionary using a dictionary comprehension, but only
if the price of the fruit is less than 5.0:

```python
fruit_prices = [("apple", 1.5), ("banana", 10), ("coconut", 2.0), ("orange", 0.75), ("grape", 3.0)]
```

::: hint

Remember that the syntax for a dictionary comprehension is
`{key_expression: value_expression for item in iterable if condition}`.

:::


:::::::::::::::: solution

```python
fruit_prices_dict = {fruit: price for fruit, price in fruit_prices if price < 5.0}
print(fruit_prices_dict)
```

Output:
```
{'apple': 1.5, 'coconut': 2.0, 'orange': 0.75, 'grape': 3.0}
```

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge: Jagged Zips

What happens if we try to zip two iterables of different lengths? Take a look at the following
code. What do you think will happen?

```python
x_values = ["a", "b", "c"]
y_values = [1, 2]

for x, y in zip(x_values, y_values):
    print(x, y)
```

A. It will raise an error because the iterables are of different lengths.
B. It will zip the iterables together, but only up to the length of the shorter iterable.
C. It will zip the iterables together, and fill in missing values with `None`.

:::::::::::::::: solution

The correct answer is B. The `zip` function will zip the iterables together, but only up to the
length of the shorter iterable. This means that when zipping, you don't need to necessarily have
the same number of elements in each iterable, but you need to keep this in mind, since there is no
explicit error raised.

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge: Set Operations

Here are two lists of students who attended two different classes. Use set operations to find out:

1. Which students attended both classes?
2. Which students attended only the first class?
3. Which students attended only the second class?
4. How many unique students attended at least one of the classes?

```python
class_a_students = ["Alice", "Bob", "Charlie", "David"]
class_b_students = ["Charlie", "David", "Eve", "Frank"]
```

:::::::::::::::: solution

```python
class_a_set = set(class_a_students)
class_b_set = set(class_b_students)

# Students who attended both classes
both_classes = class_a_set.intersection(class_b_set)
print("Students who attended both classes:", both_classes)

# Students who attended only the first class
only_class_a = class_a_set.difference(class_b_set)
print("Students who attended only the first class:", only_class_a)

# Students who attended only the second class
only_class_b = class_b_set.difference(class_a_set)
print("Students who attended only the second class:", only_class_b)

# Unique students who attended at least one class
num_unique_students = len(class_a_set.union(class_b_set))
print("Unique students who attended at least one class:", num_unique_students)
```

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- An iterable is any Python object that implements the `__iter__()` method, which returns an iterator.
- Iterators also implement the `__next__()` method, which returns the next item in the sequence when called.
- A generator is a special type of iterable that allows you to generate values on the fly, rather than storing them all in memory at once.
- Sets are unordered collections of unique elements that support mathematical set operations like union, intersection, difference, and symmetric difference.

::::::::::::::::::::::::::::::::::::::::::::::::