---
title: 'More On Class Objects'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

-

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

-

::::::::::::::::::::::::::::::::::::::::::::::::

## Expanding on Class Objects

In the previous episode, we saw how to define a simple class object in python, and how to create
instances of that class. In this episode, we will expand on that knowledge and see how to add more
functionality to our class objects, and how to use some of the built-in features of python classes.

### Dunder Methods

The `__init__` method is called a "dunder" (double underlined) method in python. There are a number
of other dunder methods that we can define, that will interact with various built-in functions and
operators. For example, we can define a `__str__` method, that will allow us to specify how our
object should be represented as a string when we call `str()` on it. Likewise, we can define
`__eq__`, which would tell python how to behave when we compare two objects for equality.

Several dunder methods are created automatically when we define a class, such as `__repr__`, which 
provides a string representation of the object for debugging purposes, and `__class__`, which
provides a reference to the class of the object. 

Let's go back to our bank account example. We can see a list of all of the dunder methods our
object has by using the `dir()` function:

```python
print(dir(my_account))
```

These all have basic implementations that are created automatically when we define the class, but 
we can override these with our own implementations if we want to add specific behavior.

Try this for example: Let's define two class instances with identical properties, and then ask
python if they are the same:

```python
account1 = BankAccount(account_holder="Todd", account_number=123, balance=100.0)
account2 = BankAccount(account_holder="Todd", account_number=123, balance=100.0)

print(account1 == account2)  # Output: False
```

::: callout

Under the hood, the `==` operator calls the `__eq__` method of the class. We can view the signature
of this method by using the `help()` function:

```python
help(BankAccount.__eq__)
```

```
Help on wrapper_descriptor:

__eq__(self, value, /) unbound builtins.object method
    Return self==value.
```

So it accepts a single parameter, `value`, which is the object that we are comparing to. The `self`
parameter is the instance of the class that we are calling the method on. The method should return
`True` if the two objects are considered equal, and `False` otherwise.

:::

This is because the `==` operator is comparing the memory addresses of the two objects, which are
different. If we want to compare the properties of the two objects instead, we can define our own
`__eq__` method that tells python that two `BankAccount` objects are equal if their 
`account_holder`, `account_number`, and `balance` properties are all the same.

```python
class BankAccount:
    def __init__(self, account_holder: str, account_number: int, balance: float = 0.0):
        self.account_holder = account_holder
        self.account_number = account_number
        self.balance = balance

    def __eq__(self, other) -> bool:
        return (self.account_holder == other.account_holder and
                self.account_number == other.account_number and
                self.balance == other.balance)

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive")

    def withdraw(self, amount: float) -> None:
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
            else:
                raise ValueError("Insufficient funds")
        else:
            raise ValueError("Withdrawal amount must be positive")

    def get_balance(self) -> float:
        return self.balance
```

Running the same code as before will now give us the output:

```python
account1 = BankAccount(account_holder="Todd", account_number=123, balance=100.0)
account2 = BankAccount(account_holder="Todd", account_number=123, balance=100.0)
print(account1 == account2)  # Output: True
```

There are a large list of dunder methods that we can customize, and they can be used to add a lot of
additional functionality to our classes. You can find a full list of them here: 
https://docs.python.org/3/reference/datamodel.html#special-method-names

### Static Properties

We've been dealing entirely with instance methods so far, which are stored on the specific instance
of the class that is created when we call the constructor. However we can also define static
properties and methods, which are stored on the class itself, and not on any specific instance. 
These allow us to define functionality that is related to the class, but doesn't operate on any 
specific instance of the class.

Let's add a static property to our `BankAccount` class that automatically assigns the next 
available account number to each new account that is created, rather than having to pass it in as 
a parameter to the constructor:

```python
class BankAccount:
    # Static property to keep track of the next available account number
    next_account_number = 10000
    
    def __init__(self, account_holder: str, balance: float = 0.0):
        self.account_holder = account_holder
        BankAccount.next_account_number += 1
        self.account_number = BankAccount.next_account_number
        self.balance = balance

    # ... rest of the class definition ...
```

Running our code from earlier, we can see that the account numbers are now automatically assigned:

```python
my_account = BankAccount(account_holder="Jimmy", balance=100.0)
print(my_account.account_holder)  # Output: Jimmy
print(my_account.account_number)  # Output: 10001
print(my_account.balance)         # Output: 100.0

another_account = BankAccount(account_holder="Mike", balance=2000.0)
print(another_account.account_holder)  # Output: Mike
print(another_account.account_number)  # Output: 10002
print(another_account.balance)         # Output: 2000.0
```

We can still manually set the account number if we want to, but if we don't, it will automatically 
be assigned for us.


::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Identify the mistake

The following code is supposed to define a `Bird` class that inherits from the `Animal` class and
overrides the `whoami` method to provide a specialized message. However, there is a mistake in
the code that prevents it from working as intended. Can you identify and fix the mistake?

```python
class Animal:
    def __init__(self, name: str):
        print(f"Creating an animal named {name}")
        self.name = name

class Bird(Animal):
    def whoami() -> str:
        return f"I am a bird. My name is irrelevant."
```

::: hint

When we try to run the code we get the following error:

```
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[7], line 14
     11         return f"I am a bird. My name is irrelevant."
     13 animal = Bird("boo")
---> 14 animal.whoami()

TypeError: Bird.whoami() takes 0 positional arguments but 1 was given
```

:::

:::::::::::::::: solution

We have forgotten to include the `self` parameter in the `whoami` method of the `Bird` class. The
`self` parameter is required for instance methods in Python, as it refers to the instance of the
class. Without it, the method cannot access instance properties or methods.

:::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::::


::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: The __str__ Method

We looked at the `__eq__` method as an example of a dunder method that we can define to customize 
the behavior of our class objects. Another common dunder method to define is the `__str__` method,
which allows us to specify how our object should be represented as a string when we call `str()` on
it.

Try to define a `__str__` method for the following class object that will create the following
output when run:

```python
class Animal:
    def __init__(self, name: str):
        print(f"Creating an animal named {name}")
        self.name = name

    # Your __str__ method here

animal = Animal("Moose")
print(str(animal))
```

output:
```
Creating an animal named Moose
I am an animal named Moose.
```


:::::::::::::::: solution

```python
class Animal:
    def __init__(self, name: str):
        print(f"Creating an animal named {name}")
        self.name = name

    def __str__(self) -> str:
        return f"I am an animal named {self.name}."

```

:::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::::


::::::::::::::::::::::::::::::::::::: challenge

## Challenge 3: Static Methods

In addition to instance methods, which operate on an instance of a class (and so have `self` as the
first parameter), we can also define static methods. These are methods that don't operate on an
instance of the class, and so don't have `self` as the first parameter. Instead, they are defined
using the `@staticmethod` decorator.

Create a static method called `is_animal` that takes a single parameter, `obj`, and returns
`True` if `obj` is an instance of the `Animal` class, and `False` otherwise.

```python
class Animal:
    def __init__(self, name: str):
        print(f"Creating an animal named {name}")
        self.name = name

    # Your static method here
```

::: hint

A decorator is a special kind of function that modifies the behavior of another function. They are
defined using the `@` symbol, followed by the name of the decorator function. In this case, we
use the `@staticmethod` decorator to indicate that the following method is a static method, so this
line must be placed directly above the method definition.

:::

::: hint

You can use the python built-in function `isinstance` to check if an object is an instance of a
class. (https://docs.python.org/3/library/functions.html#isinstance)

:::

:::::::::::::::: solution

```python
class Animal:
    def __init__(self, name: str):
        print(f"Creating an animal named {name}")
        self.name = name

    @staticmethod
    def is_animal(obj: object) -> bool:
        return isinstance(obj, Animal)
```

:::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1:


:::::::::::::::: solution


:::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

-

::::::::::::::::::::::::::::::::::::::::::::::::

