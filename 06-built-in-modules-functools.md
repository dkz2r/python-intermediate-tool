---
title: 'Decorators & Caching'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

- What is a decorator and how can it be useful?
- What built in functionalities come with the `functools` module?
- What is caching and how can it speed up my code?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Implement a simple decorator using `functools`.
- Explain how caching works and how to use it with `functools`.
- Demonstrate how to use `singledispatch` to handle different input types in a function.

::::::::::::::::::::::::::::::::::::::::::::::::

## functools

The `functools` module is a collection of higher-order tools that simplify working with functions
and callable objects. Much like the `itertools` and `collections` modules, `functools` is part of
the Python standard library and contains useful additions to functions and callable objects.

In the last few episodes, we've talked about various methods and functions that we come with
python that we can use to avoid "reinventing the wheel" and writing code for simple tasks that
have already been solved. Within the `functools` module, we have several tools called "decorators"
that can help us with these kinds of situations, and can be easily added onto an existing function
to modify its behavior without changing the function's code!

## What is a decorator?

You might have seen a decorator in the wild already - on the line before a function definition, you
can sometimes see a line that starts with an `@` symbol, followed by a name. This is a decorator,
and it is a way to modify the behavior of a function without changing its code.

We can write our own simple decorator to see how it works. Let's say we want to time exactly how
long a function takes to run and print a little message before and after the function runs. We can
write a decorator to do this for us:

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        print(f"Starting {func.__name__}...")
        start_time = time.time() # Note the start time
        result = func(*args, **kwargs) # Run the function with any arguments it might have
        end_time = time.time() # Note the end time
        print(f"{func.__name__} finished in {end_time - start_time:.4f} seconds.")
        return result # In case the function returns something, we want to return that as well
    return wrapper

@timer
def slow_function():
    time.sleep(2)
    print("Finished sleeping!")

slow_function()
```

## Caching

Sometimes executing a function can take a long time. This could be for a number of reasons. Maybe
the function is performing a calculation that takes a long time, or maybe it is making a request to
an external API that takes a few seconds to respond. In these cases, if the response is going to
be the same for the same input, we can use a caching decorator to store the result of the function
call in memory.

Here's an example of a function that calculates the price of a product. Here, the calculation is
trivial, so we've added a time.sleep statement to simulate a long calculation:

```python
import time

def calculate_price(product):
    print("Calculating price...")
    time.sleep(2)
    return product * 2

print(calculate_price(10))
print(calculate_price(10))
print(calculate_price(20))
print(calculate_price(10))
print(calculate_price(20))
```

Output:
```
Calculating price...
20
Calculating price...
20
Calculating price...
40
Calculating price...
20
Calculating price...
40
```

You can see that calling this function over and over results in having to wait the two seconds each
time it is called, even for instances where the input is the same.

Let's try using the `cache` decorator from the `functools` module. We don't need to modify our
function code at all - just add the `@cache` decorator above the function definition:

```python
from functools import cache # Add this import

@cache # Add this decorator
def calculate_price(product):
    print("Calculating price...")
    return product * 2

print(calculate_price(10))
print(calculate_price(10))
print(calculate_price(20))
print(calculate_price(10))
print(calculate_price(20))
```

Output:
```
Calculating price...
20
20
Calculating price...
40
20
40
```
We still have to wait for the first call to `calculate_price(10)` and `calculate_price(20)`, but
after that, the results are cached and returned immediately for subsequent calls with the same
input. We can even see that the print statement is not being executed for each of the repeated
calls, which tells us that python is entirely skipping the function code and just returning the
cached result.


#### What can be problematic about caching?
We can theoretically store an unlimited amount of data using a cache. Our toy example above is only
storing integers, but imagine if we were caching API requests that were several MB in size, and we
were making hundreds of requests per second. If we don’t want to fill memory with unnecessary data,
we can solve this problem with `lru_cache`.

The `lru_cache` decorator works similarly to a `cache` but allows us to set a limit on the amount
of data stored.

::: callout
LRU means **Least Recently Used**. When the cache is full, Python removes the result that has not
been used for the longest time.
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

print(get_weather.cache_info()) # Access the cache info
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
Using another decorator in functools, we can define different actions based on the input type a
function receives. This decorator is called `singledispatch`.

::: callout

If you are coming from another  programming language, this is similar to function overloading.

:::

For example, we can define a default function for an input type for which no specific version has
been defined:

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

## Challenge 1: Caching Calculations

We have a calculation that takes a long time to run, and we want to cache the results to speed up
our program. What is the correct way of applying a decorator to this function?

1:

```python
@cache()
def long_calculation(x):
```

2:
```python
cache
def long_calculation(x):
```

3:
```python
@cache
def long_calculation(x):
```

4:
```python
@lru_cache(maxsize=128)
def long_calculation(x):
```

:::::::::::::::: solution

Either option 3 or 4 is correct. Option 3 uses the `cache` decorator, which caches all results
without limit. Option 4 uses the `lru_cache` decorator, which caches results with a limit of 128
results.

Option 1 is incorrect because the `cache` decorator does not take any arguments, so the parentheses
are not needed.

Option 2 is incorrect because it does not use the `@` symbol to apply the decorator to the function.

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Writing our own decorator

We have an application that needs to access data stored on a device in our lab. Unfortunately, the
device is somewhat temperamental, and sometimes fails to respond to our request. Your colleague has
already written some code to retrieve data from the device, but at the moment it's a while loop that
uses a try/except block to keep trying until it gets a response:

```python
##### Everything between these lines is mocking an unreliable device. Do not modify this code. #####
import random

random.seed(42)

class DeviceError(Exception):
    pass

class Device:
    def __init__(self):
        self.collected = 0

    def __iter__(self):
        return self

    def __next__(self):
        print("+++ Attempting to access next reading... +++")
        if self.collected >= 10:
            raise StopIteration
        if random.random() < 0.2: # 20% of the time, the device fails
            raise DeviceError("Device not responding")
        self.collected += 1
        return f"datapoint_{self.collected}"

    def reset(self):
        self.collected = 0
####################################################################################################

flaky_device = Device()

results = []
while len(results) < 10:
    try:
        data = next(flaky_device)
        print("retrieved data!")
        results.append(data)
    except DeviceError:
        print("retrying...")

print(results)
```

This works, but we now have the issue where we have a number of different devices that we need to
access, and we don't want to have to write the same while loop with a try/except block for each
device. See if you can write a decorator that will handle the retrying for us, so we can just call
the function that retrieves the data from the device, and it will automatically retry if it fails.

Some starter code:

```python
# Replace the underscores with your function names
def _____(func):
    def _______(*args, **kwargs):
        # ... your code here ...
    return _______

# Decorate this function
def get_next_reading(device):
    return next(device)

# This is our new while loop for retrieving the data.
results = []
while len(results) < 10:
    results.append(get_next_reading(flaky_device))

print(results)
```

::: hint

The wrapper function should contain the while loop and the try/except block, returning the result
if the function call is successful, and retrying if it fails.

:::

:::::::::::::::::::::::: solution

```python
def retry(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                result = func(*args, **kwargs)
                print("retrieved data!")
                return result
            except DeviceError:
                print("retrying...")
    return wrapper

@retry
def get_next_reading(device):
    return next(device)

results = []
while len(results) < 10:
    results.append(get_next_reading(flaky_device))

print(results)
```

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::


::::::::::::::::::::::::::::::::::::: keypoints

- The `functools` module provides useful tools for working with functions, such as `cache`, `lru_cache`, `singledispatch`, and `wraps`.
- Caching can speed up repeated function calls by storing results in memory, but it can also consume memory if not used carefully.
- The `singledispatch` decorator allows us to define different behaviors for a function based on the type of its input.
- The `wraps` decorator helps preserve the original function's metadata when creating decorators.

::::::::::::::::::::::::::::::::::::::::::::::::
