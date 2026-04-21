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

