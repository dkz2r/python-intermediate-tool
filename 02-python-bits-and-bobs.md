---
title: 'Python Bits and Bobs'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

- What are some elements of python that are not covered in beginner courses but are still useful to know?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

-

::::::::::::::::::::::::::::::::::::::::::::::::

## Bits and Bobs

There are some elements of python that are fundamental elements of the language, but that are not
typically covered in beginner courses, either because they are not strictly necessary to know to
get started with programming, because they are only useful in edge cases, or because they are simply
shorthand ways of doing things that are already possible in other ways. In this episode, we will
cover some of these elements, and how they can be useful in your own code.

### Tuple Unpacking

Tuple unpacking is a feature in Python that allows you to assign values from a tuple (or any
iterable) to multiple variables in a single statement. This can make your code more readable and
concise, as long as you use it responsibly.

Here's an example of tuple unpacking in action:

```python
# Without tuple unpacking
geo_coordinates = (50.4651, 6.03548)
latitude = geo_coordinates[0]
longitude = geo_coordinates[1]

# With tuple unpacking
latitude, longitude = geo_coordinates
```

It can also be used to unpack values from a function that returns multiple values:

```python
def get_coordinates():
    return (50.4651, 6.03548)

latitude, longitude = get_coordinates()
```

It's a great shorthand, but keep in mind that it can make your code less readable if overused or
used in complex situations.

#### Asterisk Unpacking

As a bonus, you can also use an asterisk `*` to unpack the remaining values of a tuple into a list:

```python
geo_data = (50.4651, 6.03548, 100, 200, 300)
latitude, longitude, *other_values = geo_data
```

Or the double asterisk `**` to unpack the remaining values of a dictionary into another dictionary:

```python
geo_data = {"latitude": 50.4651, "longitude": 6.03548, "altitude": 100, "speed": 200}
latitude, longitude, **other_values = geo_data
```

#### *args and **kwargs

You might have seen the `*args` and `**kwargs` syntax in function definitions before. These are
used to allow a function to accept an arbitrary number of positional and keyword arguments,
respectively. This can be useful when you want to create a function that can handle a variable
number of inputs, or when you want to pass arguments to another function without knowing in advance
how many arguments will be passed.

```python
def make_a_pizza(size, **kwargs):
    print(f"Making a {size} pizza")
    add_toppings(**kwargs)

def add_toppings(**toppings):
    for topping, amount in toppings.items():
        print(f"Adding {amount} {topping}")

make_a_pizza("large", mushrooms=10, salami=8, green_peppers=5)
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

### Membership Testing

The keyword `in` can be used to quickly check if an element is present in a list, tuple, set, or
dictionary. This can be useful for checking if a value exists in a collection without having to
write a loop or use a more complex method. Here's an example:

```python
toppings = ["pepperoni", "mushrooms", "green peppers"]

if "mushrooms" in toppings:
    print("Mushrooms are available!")
else:
    print("Mushrooms are not available.")
```

### Chained Comparison Operators

What if we have a situation where we want to check if a number is between two other numbers? We
could use something like this:

```python
my_number = int(input("Please enter a number: "))
if 10 < my_number and my_number < 20:
    print("Good!")
else:
    print("Not good!")
```

but a more elegant way to do this is to use chained comparison operators:

```python
my_number = int(input("Please enter a number: "))
if 10 < my_number < 20:
    print("Good!")
else:
    print("Not good!")
```

This is both shorter and more readable.

### `any` and `all`

The built-in functions `any` and `all` can be used to check if any or all elements of an iterable
are true, respectively. This can be useful for checking if a list of conditions are met without
having to write a loop to check each condition individually. Here's an example:

```python
available_toppings = ["pepperoni", "mushrooms", "green peppers"]

pizza1_toppings = ["pepperoni", "mushrooms"]
pizza2_toppings = ["pepperoni", "pineapple"]

can_make_pizza1 = all(topping in available_toppings for topping in pizza1_toppings)
can_make_pizza2 = all(topping in available_toppings for topping in pizza2_toppings)

print(f"Can make pizza 1: {can_make_pizza1}")  # Output: True
print(f"Can make pizza 2: {can_make_pizza2}")  # Output: False
```

### String Formatting

We have a couple options for formatting strings in Python:

**format()**

```python
topping, price = "mushrooms", 1.50
formatted_string = "The price of {} is ${:.2f}".format(topping, price)
print(formatted_string)  # Output: The price of mushrooms is $1.50
```

**f-strings**

```python
topping, price = "mushrooms", 1.50
formatted_string = f"The price of {topping} is ${price:.2f}"
print(formatted_string)  # Output: The price of mushrooms is $1.50
```

**sprintf-style formatting**

```python
topping, price = "mushrooms", 1.50
formatted_string = "The price of %s is $%.2f" % (topping, price)
print(formatted_string)  # Output: The price of mushrooms is $1.50
```

::: callout

The ".2f" part specifies that this number should be formatted as a floating-point number with 2
decimal places. You can also use other format specifiers, such as ",.d" for integers with commas as
thousands separators, or "e" for scientific notation.

:::

### `_` as a throwaway variable

You might sometimes see the underscore `_` used as a variable name in Python. This is a convention
that indicates that the variable is a "throwaway" variable, meaning that it is not going to be used
later in the code. This can be useful when you need to unpack a tuple or list in a loop, but you
don't care about one of the values. Here's an example:

```python
for _, value in enumerate(["a", "b", "c"]):
    print(value)
```

::::::::::::::::::::::::::::::::::::: challenge

## Challenge: Swapping Values

We can use tuple unpacking to swap the values of two variables without needing a temporary
variable. Take the following code that swaps the values of `a` and `b`:

```python
a = 23
b = 42

temp = a
a = b
b = temp
```

Can you rewrite this code without using the `temp` variable, using tuple unpacking instead?


:::::::::::::::: solution

```python
a = 23
b = 42

a, b = b, a
```


:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge: Checking User Input

We have a small script that asks the user for a series of words that are longer than 4 characters
but shorter than 10 characters. Additionally we want to make sure that none of their words are in
the banned list. Use the `all` and `any` functions to complete the following code:

```python
banned_words = ["hunter2", "secret", "turtle"]

user_words = input("Please enter a series of words, separated by spaces: ").split()

# Check that words are longer than 4 characters and shorter than 10 characters
valid_length = # Your code here

# Check that none of the words are in the banned list
not_banned = # Your code here

if valid_length and not_banned:
    print("All words are valid!")
```


:::::::::::::::: solution

```python
banned_words = ["hunter2", "secret", "turtle"]

user_words = input("Please enter a series of words, separated by spaces: ").split()

# Check that words are longer than 4 characters and shorter than 10 characters
valid_length = all(4 < len(word) < 10 for word in user_words)

# Check that none of the words are in the banned list
not_banned = all(word not in banned_words for word in user_words)

if valid_length and not_banned:
    print("All words are valid!")
```


:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge: Parse the Sensor Data

We have a sensor that is sending us data. Our colleague has already written some code to parse part
of the data, but needs help to parse the rest of it. The data is in the following format:

```python
sensor_data = "humidity,pressure,altitude:65%,129mb,103m"
measurements = sensor_data.split(":")[0].split(",") # Get a list of the measurement names
values = sensor_data.split(":")[1].split(",") # Get a list of the measurement values
```

We would like to print out the formatted measurements and their values like this:

```
Humidity: 65%
Pressure: 129mb
Altitude: 103m
```

::: hint

Use the `zip` function to combine the `measurements` and `values` lists

:::

::: hint

Use tuple unpacking in a for loop to pull out the measurements and values from the zipped list.

:::

:::::::::::::::: solution

```python
for measurement, value in zip(measurements, values):
    print(f"{measurement.capitalize()}: {value}")
```

For good measure, we also use the `capitalize()` method to capitalize the first letter of each
measurement name.

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge: Use Chained Comparison Operators

Rewrite the following code using chained comparison operators:

```python
temperature_outside = 34
temperature_inside = 29

if temperature_outside > 30 and temperature_inside < 25:
    print("It's hot outside, but cool inside.")
elif temperature_outside < 25 and temperature_inside > 30:
    print("It's cool outside, but hot inside.")
elif temperature_outside > 30 and temperature_inside > 30:
    print("It's hot everywhere.")
else:
    print("It's probably a nice day.")

```


:::::::::::::::: solution

Note that chained comparison operators only work when something is in a range. So while we can use
them for the first two conditions, we cannot use them for the third.

```python
if temperature_outside > 30 > temperature_inside:
    print("It's hot outside, but cool inside.")
elif temperature_outside < 25 < temperature_inside:
    print("It's cool outside, but hot inside.")
elif temperature_outside > 30 and temperature_inside > 30:
    print("It's hot everywhere.")
else:
    print("It's probably a nice day.")
```

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::







::::::::::::::::::::::::::::::::::::: keypoints

-

::::::::::::::::::::::::::::::::::::::::::::::::

