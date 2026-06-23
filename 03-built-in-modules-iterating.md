---
title: 'Collections & Iterables'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

- What built in modules come with python that can help with iterable objects like lists and tuples?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Learn how to use the `Counter` object to efficiently count values from an iterable.
- Learn how to use the `deque` object to efficiently handle FIFO (First In, First Out) operations.
- Learn how to use the `combinations` function to return all possible selections without repetition.

::::::::::::::::::::::::::::::::::::::::::::::::

## collections / itertools

The `collections` and `itertools` modules have useful tools for working with data more efficiently:
`collections` helps us store and organize data, while `itertools` helps us iterate over and combine data.

The collections module allows us to use alternative data structures to Python's built-in containers; like dict, list, set, and tuple.

Using collections module can solve some common data-handling problems in a simpler and cleaner way.
Things like:

- How can I quickly count elements in a container?
- How can I easily add elements to a queue, that then removes them as they are not used?
- How can I quickly come up with all permutations of a list of objects?


## How can collections make working with data easier?

### Counting repeated values

Let's start with a common problem: How many times do specific elements appear in a given list? Say
we are working in a restaurant and want to know how popular each of our dishes are. We could write
our own code to do this, using a dictionary to store the elements as we see them and incrementing
the key each time we see them:

```python
orders = ["pizza", "burger", "pizza", "sushi", "burger", "pizza"]

counts = {}

for order in orders:
    if order not in counts:
        counts[order] = 0
    counts[order] += 1

print(counts)
```
Output:
```
{'pizza': 3, 'burger': 2, 'sushi': 1}
```

But we're lazy! This is a common enough piece of code to write that someone else has already
written an implementation and added it to the built-in python module `collections`:

```python
from collections import Counter

orders = ["pizza", "burger", "pizza", "sushi", "burger", "pizza"]

my_counter = Counter(orders)

print(my_counter)
```
Output:
```
Counter({'pizza': 3, 'burger': 2, 'sushi': 1})
```

Here, thanks to the collections library, we don't have to write the counting logic ourselves,
instead we use the predefined Counter class that handles the counting for us.

But notice that the result we get is not a `dict`, but a `Counter` object. This object can do many
of the same things as a dict, but has some additional methods that save us from writing mode code
again!

For example, let's take our dictionary result from above. If we want to find the value that appear
most frequently in the dictionary, we can start with something like this:

```python
counts = {'pizza': 3, 'burger': 2, 'sushi': 1}

most_common = (None, 0)
for key, count in counts.items():
    if count > most_common[1]:
        most_common = key, count

print("Most Common value:", most_common)
```

Output:
```
Most Common value: ('pizza', 3)
```

So that works for our example, but it's a couple lines of code to add, which adds complexity. We
could write a little function, or add some comments, but the easiest thing to do by far is to just
use the `Counter` object, which comes pre-built with a method to do exactly that:

```python
most_common = my_counter.most_common(1) # first item from the most common (item, count) pair
print("Most Common value:", most_common[0])
```

Output:
```
Most Common value: ('pizza', 3)
```

### Creating Queues

Another common task with iterable objects is to create a queue. Say our resturant wants to create a
system to track the the last three orders that were made, so we can see what is currently popular.
We can make some code to do this, using a list to store the orders and removing them each time we
add a new one:

```python
def add_order(order, orders):
    if len(orders) == 3:
        orders.pop(0) # remove the first item in the list
    orders.append(order)

delivery_updates = []
add_order("burger", delivery_updates)
add_order("noodles", delivery_updates)
add_order("pizza", delivery_updates)
print(delivery_updates)
add_order("sushi", delivery_updates)
print(delivery_updates)
```

But again, this is a common enough problem that the `collections` module has a built-in data
structure to handle it: `deque`, which stands for "double-ended queue". A `deque` allows us to add
and remove items from both ends of the queue efficiently, without having to write the logic
ourselves:

```python
from collections import deque

delivery_updates = deque(maxlen=3)

delivery_updates.append("burger")
delivery_updates.append("noodles")
delivery_updates.append("pizza")
print(delivery_updates)
delivery_updates.append("sushi")
print(delivery_updates)
```

Output:
```
deque(['burger', 'noodles', 'pizza'], maxlen=3)
deque(['noodles', 'pizza', 'sushi'], maxlen=3)
```

::: callout

`deque` has several other useful methods - check out `help(deque)`.

:::

## How can itertools make working with iterables easier?

Like we have a bunch of tools in the `collections` module to help us work with data in iterable
forms, we also have a bunch of tools in the `itertools` module to help us work with how we iterate
over data

::: callout
Many tools in the `itertools` package do not return a list object directly; instead, they return an
iterator object. The reason for this is to optimize memory usage by generating values only when
needed.
:::

### Choosing groups of items

Let's go back to our resturant example. Supposed we are focusing on pizzas. We have a list of all
the toppings we have, and we would like to know all the different combinations of toppings someone
could order. As usual, let's start by writing a simple implementation of this ourselves:

```python
toppings = ["cheese", "mushroom", "pepperoni"]

topping_pairs = []
for i in range(len(toppings)):
    for j in range(i + 1, len(toppings)):
        topping_pairs.append((toppings[i], toppings[j]))
print(topping_pairs)
```

Output:
```python
[('cheese', 'mushroom'), ('cheese', 'pepperoni'), ('mushroom', 'pepperoni')]
```

Ok, this works, but that's not the nicest code to read. We could write a function to do this, or
maybe add some comments or better variable names, but as before, there's a handy little python
function that we can use instead: `itertools.combinations`, which returns all possible combinations
of a specified length from an iterable:


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

::: callout

We have to use `list()` to convert the combinations object into a list, since the return value of
`combinations()` is an iterator, not a list. An iterator object can be iterated over, but it does
not support indexing or other list operations, instead generating values on the fly as we loop
through it.

Generators are far more memory efficient than lists, since they don't have to store all the values
in memory at once.

:::


### Creating ordered arrangements

Related to combinations - what if we want to know all of the different arrangements of toppings
that we could put on a pizza? For example, if we have three toppings, what are all the different
ways we could put those on a pizza?

The full code to do this ourselves would be a bit more complex than the combinations example, so
we'll just skip right to the built-in function that does this for us: `itertools.permutations`:

```python
from itertools import permutations

toppings = ["cheese", "mushroom", "pepperoni"]

possible_sequences = permutations(toppings)

print(list(possible_sequences))
```

Output:
```
[
    ('cheese', 'mushroom', 'pepperoni'),
    ('cheese', 'pepperoni', 'mushroom'),
    ('mushroom', 'cheese', 'pepperoni'),
    ('mushroom', 'pepperoni', 'cheese'),
    ('pepperoni', 'cheese', 'mushroom'),
    ('pepperoni', 'mushroom', 'cheese')
]
```

### Combining multiple iterables

Next, our restaurant is thinking of expanding our menu. Making it more into a nice sit-down place
instead. We've decided to add some starters, and we want to know what different combinations of
starters and mains we can have.

If we want to loop over multiple iterables as if they were one iterable, we can use `chain` from
`itertools`:

```python
from itertools import chain

starters = ["soup", "salad"]
mains = ["pizza", "burger", "sushi"]
desserts = ["ice cream", "cake"]

full_menu = chain(starters, mains, desserts)

for dish in full_menu:
    print(dish)
```

Output:
```
soup
salad
pizza
burger
sushi
ice cream
cake
```

::: callout

Why would I want to use `chain` instead of just adding the lists together with `+` or using `extend()`?

In our contrived example here, admittedly we could just add the lists together, but depending on
the use case there are a few reasons we might want to use `chain` instead:

- Readability: Using `chain` can make it clearer that we are treating multiple iterables as one sequence.
- Memory Efficiency: `chain` creates an iterator that generates items on the fly, which can be more memory efficient.
- Lazy Evaluation: If the iterables are large or infinite, `chain` allows us to iterate through them without needing to create a new list in memory.
- Flexibility: `chain` can be used with any iterable, not just lists, and can handle a variable number of iterables without needing to concatenate them first.

:::

### Repeating values

Next, we'd like to create a rotating "specials" menu for our resturant. We have some ideas for
dishes we want to feature, but we don't have enough dishes to fill a whole week. We want to make
sure that we cycle through all of the dishes we have, but we also want to make sure that we don't
repeat any dish until we've gone through all of them.

This is a perfect use case for `itertools.cycle`, which creates an infinite iterator that cycles
through all of the values in an iterable, and then starts again from the beginning once it reaches
the end:

```python
from itertools import cycle

orders = ["carbonara", "mussels", "steak", "salmon"]
rotating_orders = cycle(orders)

for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
    print(f"{day}: {next(rotating_orders)}")

```
Output:
```
Monday: carbonara
Tuesday: mussels
Wednesday: steak
Thursday: salmon
Friday: carbonara
Saturday: mussels
Sunday: steak
```

::: caution
We should only use `cycle()` with a stopping condition, like a fixed list of days or a `range()`,
because it creates an infinite iterator.
:::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Exhausting an Iterator

We defined earlier that an iterator is an object that implements the `__next__()` method, but what
happens if we call `__next__()` on an iterator more times than there are items in the iterable?

Take a look at this code, but don't run it yet:

```python
from itertools import combinations

toppings = ["cheese", "mushroom", "pepperoni"]
topping_pairs = combinations(toppings, 2)
print(next(topping_pairs))
print(next(topping_pairs))
print(next(topping_pairs))
print(next(topping_pairs)) # What happens here?
```

Do you think that it will:

A. Print "None", as there are no elements left in the iterator.
B. Raise some kind of error.
C. Print the first element again.

:::::::::::::::: solution

The correct answer is B. When we call `next()` on an iterator that has no more items to return, it
raises a `StopIteration` exception. This is how Python signals that the iterator has been exhausted
and there are no more items to iterate over.

We can handle this exception using a try-except block if we want to avoid the program crashing, or
we can use structures like for loops that automatically handle the `StopIteration` exception for us
when iterating over an iterable.

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

### Challenge 2: Print the top N most common values in a list

Start with the following code:

```python
from collections import Counter
import random

random.seed(0)
car_brands = ["Toyota", "Honda", "Ford", "BMW", "Audi"]
car_sales = [random.choice(car_brands) for _ in range(1000)]

my_counter = Counter(car_sales)
```

Write code to print the top 3 most common car brands in the `car_sales` list. Your output should
look something like this:

```
Toyota: 225
BMW: 210
Ford: 200
```

::: hint

Remember that the `Counter` object has a method to return the most common values, and it will
return a list of tuples, where each tuple contains the value and its count.

:::

::: hint

We can unpack tuples like this:

```python
name, age = ("Alice", 30)
print(name) # Alice
print(age) # 30
```

This also works in a for loop:

```python
people = [("Alice", 30), ("Bob", 25)]
for name, age in people:
    print(f"{name} is {age} years old.")
```

:::

:::::::::::::::: solution

```python
from collections import Counter
import random

random.seed(0)
car_brands = ["Toyota", "Honda", "Ford", "BMW", "Audi"]
car_sales = [random.choice(car_brands) for _ in range(1000)]

my_counter = Counter(car_sales)

for make, number in my_counter.most_common(3):
    print(f"{make}: {number}")
```

::::::::::::::::

:::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

### Challenge 3: Many Combinations

Let's expand our pizza toppings example. We have 10 different toppings, and we just want to know
how many different combinations toppings we can have on a pizza, based on the number of toppings
someone can choose. For example, if someone can only choose 3 toppings, how many different
combinations of 3 toppings can we have? What about 4?

Here's some starter code:

```python
from itertools import combinations

toppings = [
    "cheese",
    "mushroom",
    "pepperoni",
    "olives",
    "onions",
    "sausage",
    "bacon",
    "pineapple",
    "spinach",
    "artichoke"
]

# Your code here
```

Your output should look like this:

```
Number of combinations with 1 toppings: 10
Number of combinations with 2 toppings: 45
Number of combinations with 3 toppings: 120
Number of combinations with 4 toppings: 210
Number of combinations with 5 toppings: 252
Number of combinations with 6 toppings: 210
Number of combinations with 7 toppings: 120
Number of combinations with 8 toppings: 45
Number of combinations with 9 toppings: 10
Number of combinations with 10 toppings: 1
```

::: hint

Use a for loop to iterate over the number of toppings someone can choose:

```python
for i in range(1, len(toppings) + 1):
    # Your code here
```

:::

::: hint

You can't get the length of the combinations object directly, since it's an iterator and not an
actual list object. You will have to first convert it to a list, and then get the length of that list:

```python
len(list(all_combinations))
```
:::

:::::::::::::::: solution

```python
from itertools import combinations

toppings = [
    "cheese",
    "mushroom",
    "pepperoni",
    "olives",
    "onions",
    "sausage",
    "bacon",
    "pineapple",
    "spinach",
    "artichoke"
]

for i in range(1, len(toppings) + 1):
    all_combinations = combinations(toppings, i)
    print(f"Number of combinations with {i} toppings: {len(list(all_combinations))}")
```

::::::::::::::::

:::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

### Challenge 4: When to use `chain`?

We mentioned earlier that some of the reasons to use `chain` are because of it's performance and
memory efficiency. Try running the following code. What sort of results do you get?

Try increasing the number of items in the lists, and see how it affects the performance of the code.

```python
import random
import sys
import time
from itertools import chain

# Create two large lists of random integers
random.seed(0)
list1 = [random.randint(0, 100) for _ in range(10000000)]
list2 = [random.randint(0, 100) for _ in range(10000000)]

# Version 1: Using list.extend
v1_starting_memory = sys.getsizeof(list1) + sys.getsizeof(list2)
v1_start_time = time.time()

combined_list = list1.copy()
combined_list.extend(list2)
sum_combined = sum(combined_list)

v1_end_time = time.time()
v1_ending_memory = sys.getsizeof(combined_list)

print(f"Version 1 (extend) - Time taken: {v1_end_time - v1_start_time:.4f} seconds")
print(f"Version 1 (extend) - Memory used: {v1_ending_memory - v1_starting_memory:,} bytes")

# Version 2: Using itertools.chain

v2_starting_memory = sys.getsizeof(list1) + sys.getsizeof(list2)
v2_start_time = time.time()

combined_chain = chain(list1, list2)
sum_combined_chain = sum(combined_chain)

v2_end_time = time.time()
v2_ending_memory = sys.getsizeof(combined_chain)

print(f"Version 2 (chain) - Time taken: {v2_end_time - v2_start_time:.4f} seconds")
print(f"Version 2 (chain) - Memory used: {v2_ending_memory - v2_starting_memory} bytes")

print("Sums match?", sum_combined == sum_combined_chain)
```

:::::::::::::::: solution

The exact results will vary based on your machine, but you should see something like this:

```python
Version 1 (extend) - Time taken: 1.9273 seconds
Version 1 (extend) - Memory used: -70,257,144 bytes
Version 2 (chain) - Time taken: 1.1214 seconds
Version 2 (chain) - Memory used: -1,670,257,152 bytes
Sums match? True
```

At the size of the data we are using in our toy examples here, the speed difference may not be
significant but the memory usage should be far lower for `chain` than for `extend`. This is because
`chain` is creating an iterator that generates values as we loop through it, rather than creating a
new list in memory that contains all the values from both lists.

::::::::::::::::

:::::::::::::::::::::::::::::::::::::


::::::::::::::::::::::::::::::::::::: challenge

### Challenge 5: Efficient Data Processing with itertools

The following code will generate a large list of

```python
import random

def generate_log(N=50):
    users = ["Alice", "Bob", "Charlie", "David", "Eve"]
    actions = ["login", "logout", "purchase", "view"]
    for i in range(N):
        yield {"user": random.choice(users), "action": random.choice(actions)}

log_entries = list(generate_log())
```

Using the methods we've talked about from the `itertools` module, write code that will answer the
following questions about the log entries:

1. How many times did each user login?
2. What are the last 5 actions performed by each user?
3. What are all the unique actions performed by each user?

:::::::::::::::: solution

1. To count

::::::::::::::::

:::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- The `collections` module provides useful functions and objects for working with data more efficiently, such as `Counter`, `deque`, and `defaultdict`.
- The `itertools` module provides useful functions for working with iterables, such as `combinations`, `permutations`, `chain`, and `cycle`.

::::::::::::::::::::::::::::::::::::::::::::::::

