---
title: 'Python Built in Modules'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

-

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

-

::::::::::::::::::::::::::::::::::::::::::::::::

## collections / itertools

The `collections` and `itertools` modules have useful tools for working with data more efficiently:
`collections` helps us store and organize data, while `itertools` helps us iterate over and combine data.

The collections module allows us to use alternative data structures to Python's built-in containers; like dict, list, set, and tuple.

# When are collections useful? (might delete later)

Using collections module can solve some common data-handling problems in a simpler and cleaner way.
If our code becomes too long, repetitive or less readable, we could consider using collections.

### How can collections make working with data easier?

#### Counting repeated values

```python
orders = ["pizza", "burger", "pizza", "sushi", "burger", "pizza"]

counts = {}

for order in orders:
    if order not in orders:
        counts[order] = 0
    counts[order] += 1

print(counts)
```


```python
from collections import Counter

orders = ["pizza", "burger", "pizza", "sushi", "burger", "pizza"]

counts = Counter(orders)

print(counts)
```

Here, thanks to the collections library, we don't have to write the counting logic ourselves, instead we use the predefined Counter class that handles the counting for us.

In this example, if we want to find the most common order, we can even use a predefined function in the Counter class.

```python
count.most_common(1)[0][0] # first item from the most common (item, count) pair
```

#### Handling items more efficiently

By using deque, we can perform some of the operations that a list data structure does more efficiently.
In this example, we can display the most recently added elements to the list without having to write separate logic for it.

```python
from collections import deque

delivery_updates = deque(maxlen=3)

delivery_updates.append("Order received")
delivery_updates.append("Package prepared")
delivery_updates.append("Package shipped")
delivery_updates.append("Package out for delivery")
```

### Avoiding missing keys
What is the output of this line of code?
```python
snacks = {}
snacks["sweet"].append("chocolate")
```
:::::::::::::::: solution
This code raises a `KeyError`.
```python
KeyError: 'sweet'
```
Using normal dictionaries, we have to check if the key exist before adding a value to the dict.
::::::::::::::::

Good news: we could avoid that using defaultdict.
```python
snacks = defaultdict(list)
snacks["sweet"].append("chocolate")
```
Since we want to store multiple snacks under each category, we pass `list` to `defaultdict`.

In the background, this is what happens:

```python
snacks["sweet"] = []
snacks["sweet"].append("chocolate")
```
So every key starts with an empty list.

Now we can switch to the itertools.

### What is an iterable?
In order to be able to use itertools, we need to understand what an iterable is.
An iterable is a Python object such as a list, tuple, string or a dictionary that we can loop through.


### What is an iterator?
An iterator is an object that gives us the next item each time we ask for it.

::: callout
Many tools in the `itertools` package do not return a list object directly; instead, they return an iterator object. The reason for this is to optimize memory usage by generating values only when needed.
:::

### How can itertools make working with iterables easier?

#### Choosing groups
Using combinations, we can return all possible selections without repetition.
Many tools in `itertools` do not return a full list immediately. Instead, they return an iterator object.


```python
from itertools import combinations

toppings = ["cheese", "mushroom", "pepperoni"]

topping_pairs = combinations(toppings, 2)

print(list(combinations(toppings, 2)))
```

Output:
```python
[('cheese', 'mushroom'), ('cheese', 'pepperoni'), ('mushroom', 'pepperoni')]
```
In order to print the combinations, we converted them into a list.


#### Creating ordered arrangements
Using permutations, we can return all possible orders.
```python
from itertools import permutations

digits = ["1", "2", "3"]

possible_digits = permutations(digits)

print(list(possible_digits))
```

Output:
```python
[('1', '2', '3'), ('1', '3', '2'), ('2', '1', '3'), ('2', '3', '1'), ('3', '1', '2'), ('3', '2', '1')]
```

#### Combining multiple iterables
If we want to loop over multiple iterables as if they were one iterable, we can use `chain` from `itertools`.

```python
from itertools import chain

starters = ["soup", "salad"]
mains = ["pasta", "steak"]

full_menu = chain(starters, mains)

print(list(full_menu))
```

Output:
```python
['soup', 'salad', 'pasta', 'steak']
```

#### Repeating values
If we want to repeat the same values again and again, we can use `cycle` from `itertools`.

For example, we can rotate the  daily meeting host between the team members:

```python
from itertools import cycle

employees = ["Alice", "Bob", "Charlie"]
duties = cycle(employees)

for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
    print(f"{day}: {next(duties)}")

```
::: warning
We should only use `cycle()` with a stopping condition, like a fixed list of days or a `range()`, because it creates an infinite iterator.
:::

## logging

When writing code in Python, we sometimes want to track what our programs are doing.
Using `print()` in a small script may seem sufficient, but as the program grows, it becomes harder to understand which function is running when, where an error occurred, and which steps were successfully completed. This is exactly where logging comes in.
Logging allows us to capture important events that occur while the program is running. This makes it easier for us to understand the program's behavior and resolve issues.

`print()` simply prints a message to the screen. It’s useful for quick checks while the program is running, such as “Did I get here? What’s this value here?” but all messages appear to have the same level of importance.
Logging, on the other hand, assigns meaning and a severity level to messages.

```python

def transfer_money(sender, receiver, amount):
    print(f"Transfer initiated: {sender} -> {receiver}, amount: {amount}")

    if amount <= 0:
        print("Invalid amount. Transfer cancelled.")
        return

    if amount > 1000:
        print(f"Large transfer detected: {amount}")

    print(f"Transfer successful: {sender} sent {amount} to {receiver}")

```

```python
import logging

logging.basicConfig()

def transfer_money(sender, receiver, amount):
    logging.debug(f"Transfer initiated: {sender} -> {receiver}, amount: {amount}")

    if amount <= 0:
        logging.error("Invalid amount. Transfer cancelled.")
        return

    if amount > 1000:
        logging.warning(f"Large transfer detected: {amount}")

    logging.info(f"Transfer successful: {sender} sent {amount} to {receiver}")


transfer_money("Alice", "Bob", 500)
transfer_money("Bob", "Jonas", -20)
transfer_money("Jonas", "Alice", 2000)
```

We can see in this example, that the importance levels can vary, as different situations occur in different scenarios. If a transfer is successful, we simply want to be informed; if an excessive amount is sent, we get a warning; and if the amount is invalid, we receive an error message.

With logging, we can categorize these outputs into levels such as info, warning, and error, and later, if necessary, simply display warnings and errors while hiding normal transaction information.

### Why do logging?
Our goal in using logging is to leave traces of the program's behavior and the errors it encounters, so that we can resolve issues more easily using these traces.


### What to log?

Everything does not have to be logged. That is why we need to log only those events that matter.

Deciding what really matters might be challenging since we need to foresee which piece of information is critical during troubleshooting.

The following list of events is an example of what we need to log:

- errors which block the functionality of the program
- warnings about dangerous conditions
- successful execution of the program
- critical choices of the program
- external interactions, like API calls and DB queries

We can set the log levels that we want to show as following:
```python
logging.basicConfig(
    level=logging.INFO
)
```
Here, we capture all of the logging messages from info level and above.

::: warning
We must never log confidential data such as API keys, passwords, tokens, user personal information, etc.
:::

### Custom logging format

Imagine you're running a payment script overnight and something goes wrong.
Which log is more useful?

```
INFO:root:Transfer complete
INFO:root:Transfer failed
```
```
10:23:01 - INFO  - Transfer complete: Alice -> Bob, $200
10:23:04 - ERROR - Transfer failed: Bob -> Carol, $1500 (insufficient funds)
```

The second version tells us exactly when it happened and what went wrong without opening the code.

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-6s - %(message)s",
    datefmt="%H:%M:%S"
)
```
We do it by setting a `format` parameter in `basicConfig()`, using placeholder fields like `%(asctime)s` for the timestamp and `%(levelname)s` for the severity level.


## functools
Functools is a library that contains a collection of higher-order tools that simplify working with functions and callable objects.

### Why do we need functools?
In Python, functions do more than just run code.
Sometimes, we want to change how functions work, reuse them, or add to them.

The `functools` module has built-in tools for these kinds of situations, so we don't have to write the same helper code over and over.

It helps us clean up, speed up, and make our code easier to reuse.

### How can functools make working with functions easier?

#### Speeding up repeated calls
Sometimes executing a function can take a long time. If we call this function multiple times in our code, waiting for it to run from scratch each time results in a significant loss of time.

For situations like this, the `cache` decorator in the `functools` module stores the result of the function call in memory. If the function is called again with the same input, Python returns the cached result instead of recalculating it.

```python
from functools import cache

@cache
def calculate_price(product):
    print("Calculating price...")
    return product * 2

print(calculate_price(10))
print(calculate_price(10))
print(calculate_price(10))
```

Output:
```text
Calculating price...
20
20
20
```
As you can see here, the text "Calculating price..." is printed only once, meaning the function actually runs only once, and the result is retrieved from the cache for all subsequent calls.


#### What can be problematic about caching?
We can store an unlimited amount of data using a cache.
If we don’t want to fill memory with unnecessary data, we can solve this problem with `lru_cache`.

The `lru_cache` decorator works similarly to a `cache` but allows us to set a limit on the amount of data stored.

::: callout
LRU means **Least Recently Used**.
When the cache is full, Python removes the result that has not been used for the longest time.
:::

```python
from functools import lru_cache
import time

@lru_cache(maxsize=3)
def get_weather(city):
    time.sleep(1)  # simulates an API call
    return f"Sunny in {city}"
```

Here, the cache can store only 3 results.

```python
get_weather("Berlin")
get_weather("Tokyo")
get_weather("Paris")

print(get_weather.cache_info())
```

Output:

```text
CacheInfo(hits=0, misses=3, maxsize=3, currsize=3)
```

At this point, the cache is full:

```text
Berlin, Tokyo, Paris
```

If we call a cached city again, it becomes a cache hit:

```python
get_weather("Berlin")

print(get_weather.cache_info())
```

Output:
```text
CacheInfo(hits=1, misses=3, maxsize=3, currsize=3)
```

Now `"Berlin"` was used recently.
If we add a new city, one old result must be removed:

```python
get_weather("Sydney")
print(get_weather.cache_info())
```

Output:

```text
CacheInfo(hits=1, misses=4, maxsize=3, currsize=3)
```

The cache still contains only 3 results, because `maxsize=3`.
Since `"Tokyo"` was the least recently used city, it is removed to make space for `"Sydney"`.

```text
Paris, Berlin, Sydney
```

If we call `"Tokyo"` again, it has to be calculated again:
```python
get_weather("Tokyo")

print(get_weather.cache_info())
```

Output:
```text
CacheInfo(hits=1, misses=5, maxsize=3, currsize=3)
```
`Tokyo` was no longer in the cache, so this call is a cache miss.


#### Handling different input types
Using another decorator in functools, we can define different actions based on the input type a function recieves.
This decorator is called `singledispatch`.

For example, we can define a default function for an input type for which no specific version has been defined:

```python
from functools import singledispatch

@singledispatch
def search(data):
    print(f"Cannot process type: {type(data).__name__}")
```

Then we can write some special cases for strings, integers and lists:
```python
@search.register(str)
def _(data):
    print(f"Searching for: {data}")
```

```python
@search.register(int)
def _(data):
    print(f"Showing top {data} results.")
```

```python
@search.register(list)
def _(data):
    print(f"Searching in categories: {data}")
```
::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Can you find what these function calls return?
```python
search("machine learning")
```

```python
search(5)
```

```python
search(["books", "articles", "videos"])
```

```python
search(3.14)
```
:::::::::::::::::::::::: solution

## Output

```text
Searching for: 'machine learning'
```

```text
Showing top 5 results.
```

```text
Searching in categories: ['books', 'articles', 'videos']
```

```text
Cannot process type: float
```

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::



#### Preserving function information
`wraps` is used inside decorators to keep information about the original function, like its name and docstring.

```python
def my_decorator(func):
    def wrapper():
        print("Before the function runs")
        func()

    return wrapper


@my_decorator
def say_hello():
    """This function says hello."""
    print("Hello!")


print(say_hello.__name__)
print(say_hello.__doc__)
```

Output:
```text
wrapper
None
```
If we don't use "wraps", the decorated function might look like the "wrapper" function instead of the original function.


```python
from functools import wraps

# example using wraps

def my_decorator(func):
    @wraps(func)
    def wrapper():
        print("Before the function runs")
        func()

    return wrapper


@my_decorator
def say_hello():
    """This function says hello."""
    print("Hello!")


print(say_hello.__name__)
print(say_hello.__doc__)
```
Output:
```text
say_hello
This function says hello.
```

In this case, @wraps(func) copies the metadata from say_hello to the wrapper function.

Even though the decorated function runs through the wrapper, Python still keeps the name and docstring of the original function.

## multiprocessing




::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Can you do it?



:::::::::::::::::::::::: solution

## Output



:::::::::::::::::::::::::::::::::




::::::::::::::::::::::::::::::::::::::::::::::::





::::::::::::::::::::::::::::::::::::: keypoints

-

::::::::::::::::::::::::::::::::::::::::::::::::

