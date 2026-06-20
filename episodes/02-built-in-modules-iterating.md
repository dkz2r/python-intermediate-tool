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
- Learn how to use the `defaultdict` object to avoid missing keys in a dictionary.
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

Let's start with a common problem: How many times do specific elements appear in a given list? We 
could write our own code to do this, using a dictionary to store the elements as we see them and
incrementing the key each time we see them:

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

counts = Counter(orders)

print(counts)
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
Most Common value: ("pizza", 3)
```

So that works for our example, but what if there's a tie? For instance, what if we added a key to
`counts` called "chips" that also appeared 3 times? We could start adding to our code, but the 
`Counter` object comes pre-built with a method to do exactly that:

```python
most_common = count.most_commons(1) # first item from the most common (item, count) pair
print("Most Common value:", top_order)
```

Output:
```
pizza
```
#### Handling items more efficiently

By using deque, we can perform some of the operations that a list data structure does more efficiently.

Let's continue with the same example where we had a list of orders.

```python
from collections import deque

delivery_updates = deque(maxlen=3)

delivery_updates.append("burger")
delivery_updates.append("noodles")
delivery_updates.append("pizza")
delivery_updates.append("sushi")

print("Order added:", delivery_updates[-1])  # take the last entry
print(delivery_updates)
```

Output:
```
Order added: sushi
deque(['noodles', 'pizza', 'sushi'], maxlen=3)
```
As you can see here, burger is not added to the deque since its size is limited to 3.


::::::::::::::::::::::::::::::::::::: challenge
Let's say we have a dict of snacks.
```python
snacks = {}
snacks["sweet"].append("chocolate")
```
This operation returns a KeyError.
```python
KeyError: 'sweet'
```

Why do you think it happened?
:::::::::::::::::::::::::::::::::::::

::::::::::::::::solution
Using normal dictionaries, we have to check if the key exist before adding a value to the dict.
::::::::::::::::

:::::::::::::::::::::::::::::::::::::challenge
How can we use defaultdict in this instance?
:::::::::::::::::::::::::::::::::::::

::::::::::::::::solution

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
::::::::::::::::

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
Using permutations, we can return all possible sequences.
```python
from itertools import permutations

toppings = ["cheese", "mushroom", "pepperoni"]

possible_sequences = permutations(toppings)

print(list(possible_sequences))
```

Output:
```
[('cheese', 'mushroom', 'pepperoni'), ('cheese', 'pepperoni', 'mushroom'), ('mushroom', 'cheese', 'pepperoni'), ('mushroom', 'pepperoni', 'cheese'), ('pepperoni', 'cheese', 'mushroom'), ('pepperoni', 'mushroom', 'cheese')]
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
```
['soup', 'salad', 'pasta', 'steak']
```

#### Repeating values
If we want to repeat the same values again and again, we can use `cycle` from `itertools`.

For example, we can cycle through the daily orders for each day of the week:

```python
from itertools import cycle

orders = ["pizza", "burger", "sushi"]
rotating_orders = cycle(orders)

for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
    print(f"{day}: {next(rotating_orders)}")

```
Output:
```
Monday: pizza
Tuesday: burger
Wednesday: sushi
Thursday: pizza
Friday: burger
```
::: caution
We should only use `cycle()` with a stopping condition, like a fixed list of days or a `range()`, because it creates an infinite iterator.
:::


::::::::::::::::::::::::::::::::::::: keypoints

- The `collections` module provides useful functions and objects for working with data more efficiently, such as `Counter`, `deque`, and `defaultdict`.
- The `itertools` module provides useful functions for working with iterables, such as `combinations`, `permutations`, `chain`, and `cycle`.

::::::::::::::::::::::::::::::::::::::::::::::::

