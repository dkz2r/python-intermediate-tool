---
title: 'More On Class Objects'
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

- What are these methods that have `__` before and after their names?
- What are static properties and methods, and how do they differ from instance properties and methods?
- What are the `@property`, `@classmethod`, and `@staticmethod` decorators, and how do they work?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Add a custom `__str__` method to our Car class to specify how it should be represented as a string.
- Add a property to our Car class to calculate the age of the car based on the current year and the year it was made.
- Add a static property to our Car class to keep track of how many cars have been created, and a class method to retrieve this count.

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
    def __init__(self, account_holder, account_number, balance = 0.0):
        self.account_holder = account_holder
        self.account_number = account_number
        self.balance = balance

    def __eq__(self, other):
        return (self.account_holder == other.account_holder and
                self.account_number == other.account_number and
                self.balance == other.balance)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive")

    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
            else:
                raise ValueError("Insufficient funds")
        else:
            raise ValueError("Withdrawal amount must be positive")

    def get_balance(self):
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

    def __init__(self, account_holder, balance = 0.0):
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

### Decorators in Classes

Python has a number of built-in decorators that we can use to modify the behavior of our class
methods. There are a couple of decorators that are specific to classes, such as `@staticmethod` and
`@property`, which allow us to more easily define our classes.

::: hint

A decorator is a special kind of function that modifies the behavior of another function. They are
defined using the `@` symbol, followed by the name of the decorator function. In this case, we
use the `@staticmethod` decorator to indicate that the following method is a static method, so this
line must be placed directly above the method definition.

:::

In our `BankAccount` class, we currently have a method called `get_balance()` that returns the
current balance of the account. The user can call this method like `my_account.get_balance()`, but
it would be more natural to access the balance as a property, like `my_account.balance`. We can use
the `@property` decorator to make this possible:

```python
class BankAccount:
    def __init__(self, account_holder, balance = 0.0):
        # ... rest of the constructor ...
        self._balance = balance

    # ... rest of the class definition ...

    @property
    def balance(self):
        return self._balance
```

Now, we can access the balance as a property, without having to call a method:

```python
my_account = BankAccount(account_holder="Jimmy", balance=100.0)
print(my_account.balance)  # Output: 100.0
```

Similarly, we can explicitly define class or static methods using the `@classmethod` and
`@staticmethod` decorators, which can be useful for defining functionality that is related to the
class, but doesn't operate on any specific instance of the class. For example, suppose we wanted to
add a method to check if a deposit is valid - it should be a positive integer, and it shouldn't
exceed a certain limit. We can define this as a static method, since it doesn't operate on any
specific instance of the class:

```python
class BankAccount:
    # ... rest of the class definition ...

    @staticmethod
    def is_valid_deposit(amount):
        return amount > 0 and amount <= 10000
```

We can call this method directly on the class, without needing to create an instance of the class:

```python
print(BankAccount.is_valid_deposit(500))   # Output: True
print(BankAccount.is_valid_deposit(-100))  # Output: False
print(BankAccount.is_valid_deposit(15000)) # Output: False
```

As well as calling it within the instance methods of the class:

```python
class BankAccount:
    # ... rest of the class definition ...

    def deposit(self, amount):
        if BankAccount.is_valid_deposit(amount):
            self._balance += amount
        else:
            raise ValueError("Invalid deposit amount")
```

This let's us keep our code organized and modular - if the rules for defining a valid deposit
change, we only need to update the `is_valid_deposit` method, and all of the code that relies on it
will automatically use the updated logic.

## Updating our Car Class

Let's go back to our `Car` class and make some updates.

### Create a custom `__str__` method

```python
class Car:
    def __init__(self, make, model, year, color = "grey", fuel = "gasoline"):
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.fuel = fuel
        self.speed = 0

    def honk_horn(self):
        return "Honk! Honk!"

    def paint(self, new_color):
        self.color = new_color

    def make_engine_noise(self):
        if self.speed <= 10:
            return "putt putt"
        else:
            return "vroom!"

    def __str__(self):
        return f"A {self.color} {self.year} {self.make} {self.model} that runs on {self.fuel}."
```

### Add a property to get the car's age

```python
from datetime import datetime

class Car:
    # ... rest of the class definition ...

    @property
    def age(self):
        current_year = datetime.now().year
        return current_year - self.year
```

### Add a static property and a class method to keep track of how many cars have been created

```python
class Car:
    car_count = 0

    def __init__(self, make, model, year, color = "grey", fuel = "gasoline"):
        # ... rest of the constructor ...
        Car.car_count += 1

    @classmethod
    def get_car_count(cls):
        return cls.car_count
```

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Identify the mistake

The following code is supposed to define a `Bird` class that inherits from the `Animal` class and
overrides the `whoami` method to provide a specialized message. However, there is a mistake in
the code that prevents it from working as intended. Can you identify and fix the mistake?

```python
class Animal:
    def __init__(self, name):
        print(f"Creating an animal named {name}")
        self.name = name

class Bird(Animal):
    def whoami(self):
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
    def __init__(self, name):
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
    def __init__(self, name):
        print(f"Creating an animal named {name}")
        self.name = name

    def __str__(self):
        return f"I am an animal named {self.name}."

```

:::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::::


::::::::::::::::::::::::::::::::::::: challenge

## Challenge 3: Class Methods

In addition to instance methods, which operate on an instance of a class (and so have `self` as the
first parameter), we can also define class methods. These are methods that operate on the class itself,
and so have `cls` as the first parameter. Instead of the `@staticmethod` decorator, they are defined
using the `@classmethod` decorator.

Start with the following code. We want to be able to easily keep track of how many animals of each
species we have created since our code started running. To do this, we will need three things:

- 1. A class property that is a dictionary that keeps track of how many animals of each species
    have been created.
- 2. A way to update this dictionary every time a new instance of the `Animal` class is created.
- 3. A class method that allows us to easily get the count of how many animals of a specific
    species have been created.

```python
class Animal:
    def __init__(self, name, species):
        print(f"Creating an animal named {name}")
        self.name = name
        self.species = species

    # Your class method here
```

When we run the following code, we should see the output:

```python
animal1 = Animal(name="Moose", species="Alces alces")
animal2 = Animal(name="Mouse", species="Mus musculus")
animal3 = Animal(name="Moose", species="Alces alces")
animal4 = Animal(name="Squirrel", species="Sciurus carolinensis")
animal5 = Animal(name="Horseshoe Crab", species="Limulus polyphemus")

print(Animal.get_animal_count("Alces alces"))  # Output: 2
print(Animal.get_animal_count("Mus musculus"))  # Output: 1
```

:::::::::::::::: solution

```python
from collections import defaultdict

class Animal:
    animal_counts = defaultdict(int)

    def __init__(self, name, species):
        self.name = name
        self.species = species
        Animal.animal_counts[species] += 1

    @classmethod
    def get_animal_count(cls, species):
        return cls.animal_counts.get(species, 0)

```


:::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::::


::::::::::::::::::::::::::::::::::::: keypoints

- Dunder methods are special methods that start and end with double underscores.
- Static properties and methods are defined on the class itself, rather than on instances of the class.
- We can use the `@property` decorator to define properties that can be accessed like attributes.
- We can use the `@classmethod` decorator to define methods that operate on the class itself, rather than on instances of the class.
- We can use the `@staticmethod` decorator to define methods that don't operate on either the class or instances of the class, but are still related to the class in some way.

::::::::::::::::::::::::::::::::::::::::::::::::

