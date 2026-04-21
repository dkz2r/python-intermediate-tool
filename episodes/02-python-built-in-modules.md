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

