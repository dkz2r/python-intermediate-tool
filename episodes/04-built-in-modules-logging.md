---
title: 'The Logging Module'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

- What can I do to log my code more effectively than using print statements?
- How can I set up and customize the logging module in Python?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Demonstrate a small example of how to use the logging module in Python.
- Explain the importance of logging and how it differs from using print statements.

::::::::::::::::::::::::::::::::::::::::::::::::

## logging

When writing code in Python, we sometimes want to track what our programs are doing.
Using `print()` in a small script may seem sufficient, but as the program grows, it becomes harder
to understand which function is running when, where an error occurred, and which steps were
successfully completed. This is exactly where logging comes in.

Logging allows us to capture important events that occur while the program is running. This makes
it easier for us to understand the program's behavior and resolve issues.

`print()` simply prints a message to the screen. It’s useful for quick checks while the program is
running, such as “Did I get here? What’s this value here?” but all messages appear to have the same
level of importance. Logging, on the other hand, assigns meaning and a severity level to messages.

Let's look at an example of a little banking application that transfers money between accounts.

```python
import random

random.seed(42)

accounts = {
    "Liz": 500,
    "Jack": 3000,
    "Kenneth": 10000
}

def transfer_money(sender, receiver, amount):
    if amount <= 0:
        return

    # Check if sender has enough balance
    if accounts[sender] < amount:
        return

    # Perform the transfer
    accounts[sender] -= amount
    accounts[receiver] += amount

transfer_money("Liz", "Jack", 200) # valid
transfer_money("Jack", "Kenneth", -20) # invalid - negative
transfer_money("Liz", "Kenneth", 1000) # invalid - exceeds balance
transfer_money("Kenneth", "Liz", 2000) # large
```

We want to track the transfer process, so we add some print statements to our code:

```python
accounts = {
    "Liz": 500,
    "Jack": 3000,
    "Kenneth": 10000
}

def transfer_money(sender, receiver, amount):
    print(f"Transfer initiated: {sender} -> {receiver}, amount: {amount}")

    if amount <= 0:
        print("Transfer failed: Invalid amount.")
        return

    if amount > 1000:
        print(f"Large transfer detected: {amount}")

    # Check if sender has enough balance
    if accounts[sender] < amount:
        print(f"Transfer failed: {sender} has insufficient funds.")
        return

    # Perform the transfer
    accounts[sender] -= amount
    accounts[receiver] += amount

    print(f"Transfer successful: {sender} sent {amount} to {receiver}")

transfer_money("Liz", "Jack", 200) # valid
transfer_money("Jack", "Kenneth", -20) # invalid - negative
transfer_money("Liz", "Kenneth", 1000) # invalid - exceeds balance
transfer_money("Kenneth", "Liz", 2000) # large
```

Output:
```
Transfer initiated: Liz -> Jack, amount: 200
Transfer successful: Liz sent 200 to Jack
Transfer initiated: Jack -> Kenneth, amount: -20
Invalid amount. Transfer cancelled.
Transfer initiated: Liz -> Kenneth, amount: 1000
Transfer failed: Liz has insufficient funds.
Transfer initiated: Kenneth -> Liz, amount: 2000
Large transfer detected: 2000
Transfer successful: Kenneth sent 2000 to Liz
```

That certainly makes it much easier to understand what's going on! However this might be a little
too much information. What if we only want to see when something goes wrong, like the invalid
amount or the insufficient funds? Or maybe we want to be notified about large transfers, but not
about every successful transfer?

We could start adding a bunch of extra logic, where we assign the importance of a message to a
value and check if that value is above a threshold before printing it. But this makes our code more
complex and harder to maintain. But luckily, this is exactly what the logging module is designed
for!


```python
import logging

logging.basicConfig()

accounts = {
    "Liz": 500,
    "Jack": 3000,
    "Kenneth": 10000
}

def transfer_money(sender, receiver, amount):
    logging.info(f"Transfer initiated: {sender} -> {receiver}, amount: {amount}")

    if amount <= 0:
        logging.error("Transfer failed: Invalid amount.")
        return

    if amount > 1000:
        logging.warning(f"Large transfer detected: {amount}")

    # Check if sender has enough balance
    if accounts[sender] < amount:
        logging.error(f"Transfer failed: {sender} has insufficient funds.")
        return

    # Perform the transfer
    accounts[sender] -= amount
    accounts[receiver] += amount

    logging.info(f"Transfer successful: {sender} sent {amount} to {receiver}")

transfer_money("Liz", "Jack", 200) # valid
transfer_money("Jack", "Kenneth", -20) # invalid - negative
transfer_money("Liz", "Kenneth", 1000) # invalid - exceeds balance
transfer_money("Kenneth", "Liz", 2000) # large
```

Output:
```
ERROR:root:Transfer failed: Invalid amount.
ERROR:root:Transfer failed: Liz has insufficient funds.
WARNING:root:Large transfer detected: 2000
```

Logging has five levels of importance. Generally, the levels are as follows:

- DEBUG: Detailed information, typically of interest only when diagnosing problems.
- INFO: Confirmation that things are working as expected.
- WARNING: An indication that something unexpected happened, but the software is still working as expected.
- ERROR: Due to a more serious problem, the software has not been able to perform some function.
- CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

We can set the minimum level of importance that we want to see in our logs by configuring the
logging module. In the example above, we can add the parameter `level=logging.DEBUG` to
`basicConfig()`. This will show all messages, as DEBUG is the lowest level.

::: callout

If we are working in a Jupyter Notebook, we will need to restart the kernel in order to update the
logging configuration after changing the `basicConfig()` parameters. This is because the logging
is set up only once per session, and subsequent calls to `basicConfig()` will not have any effect.

:::

### Why do logging?
Our goal in using logging is to leave traces of the program's behavior and the errors it
encounters, so that we can resolve issues more easily using these traces. If the program is running
into issues, we can add debugging or info messages to the code to help understand what is going
on. Once we fix the issue, we can leave these messages in the code to assist us in the future, but
we can raise the logging level so that we are not overwhelmed by too much information while the
program is running smoothly.


### What to log?

Everything does not have to be logged. That is why we need to log only those events that matter.

Deciding what really matters might be challenging since we need to foresee which piece of
information is critical during troubleshooting.


::: caution
We must never log confidential data such as API keys, passwords, tokens, user personal information,
etc.
:::

::: callout
### Custom logging format

Imagine you're running a payment script overnight and something goes wrong.
Which log is more useful?

```
ERROR:root:Transfer failed: Invalid amount.
ERROR:root:Transfer failed: Liz has insufficient funds.
```
```
10:23:01 - INFO  - Transfer failed: Invalid amount.
10:23:04 - ERROR - Transfer failed: Liz has insufficient funds.
```

The second version tells us exactly when it happened and what went wrong without opening the code.
We do set our own format by setting the `format` parameter in `basicConfig()`, using placeholder
fields like `%(asctime)s` for the timestamp and `%(levelname)s` for the severity level.

```python
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)-6s - %(message)s", datefmt="%H:%M:%S"
)
```

For a full list of available fields, see the [official documentation](https://docs.python.org/3/library/logging.html#logrecord-attributes).
:::


::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Logging Levels

What will be the output of the following code snippet?

```python
import logging
logging.basicConfig(level=logging.WARNING)

logging.debug("This is a debug message")
logging.info("This is an info message")
logging.warning("This is a warning message")
logging.error("This is an error message")
```

- A. Only the warning message will be printed.
- B. Both the warning and error messages will be printed.
- C. Only the debug and info messages will be printed.
- D. The debug, info, and warning will all be printed.

:::::::::::::::: solution

The correct answer is B. Both the warning and error messages will be printed. The logging level
indicates the *minimum* severity level that will be logged.

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge: Add Logging to a Function

Given the following code snippet:

```python
def calculate_discount(price, discount_percent):
    if discount_percent < 0:
        return price  # Invalid discount

    if discount_percent > 100:
        return 0  # Maximum discount

    final_price = price * (1 - discount_percent / 100)
    return final_price
```

Add logging statements to the `calculate_discount` function to log the following events:

- When the function is called, log the input price and discount percentage at the INFO level.
- If the discount percentage is invalid (less than 0), log an ERROR message.
- If the discount percentage is greater than 100, log a WARNING message.

When you run the following code:

```python
import logging

logging.basicConfig(level=logging.INFO)

calculate_discount(100, 20)  # valid
calculate_discount(100, -10)  # invalid - negative
calculate_discount(100, 150)  # invalid - exceeds 100
```

You should see something like the following output:

```
INFO:root:Calculating discount for price: 100, discount_percent: 20
INFO:root:Calculating discount for price: 100, discount_percent: -10
ERROR:root:Invalid discount percentage: less than 0
INFO:root:Calculating discount for price: 100, discount_percent: 150
WARNING:root:Discount percentage exceeds 100, setting to maximum discount
```

:::::::::::::::: solution

```python
def calculate_discount(price, discount_percent):
    logging.info(f"Calculating discount for price: {price}, discount_percent: {discount_percent}")

    if discount_percent < 0:
        logging.error("Invalid discount percentage: less than 0")
        return price  # Invalid discount

    if discount_percent > 100:
        logging.warning("Discount percentage exceeds 100, setting to maximum discount")
        return 0  # Maximum discount

    final_price = price * (1 - discount_percent / 100)
    return final_price
```

:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge: Custom Logging Format

Given the following code snippet:

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Application started")
logging.warning("Low disk space")
logging.error("Failed to connect to database")
```

Modify the following code so that our logs look like this:

```
[2026-06-21 19:48:17] [INFO] (Line 7) - Message: Application started
[2026-06-21 19:48:17] [WARNING] (Line 8) - Message: Low disk space
[2026-06-21 19:48:17] [ERROR] (Line 9) - Message: Failed to connect to database
```

Refer to the [official documentation](https://docs.python.org/3/library/logging.html#logrecord-attributes)
for the available fields and how to set a custom logging format.

::: hint



:::

:::::::::::::::: solution

We can set a custom logging format by using the `format` parameter in `basicConfig()`. We will use
the `asctime` field for the timestamp, and the `levelname` field for the severity level.

```python
import logging

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(levelname)s] (Line %(lineno)d) - Message: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

logging.info("Application started")
logging.warning("Low disk space")
logging.error("Failed to connect to database")
```



:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- The `logging` module is useful for tracking the behavior of our program.
- Using logging levels makes it easy to filter important messages from less important ones.
- Custom logging formats can provide more context and make logs easier to understand.

::::::::::::::::::::::::::::::::::::::::::::::::
