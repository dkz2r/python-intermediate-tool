# Class Objects Challenges Collection

This document contains a collection of challenges that build on the class objects content from episode 06. Each challenge is designed to be solvable within a few minutes and covers different aspects of working with Python classes.

## Theme: Animal Kingdom

All challenges will use an animal theme to create a cohesive learning experience.

---

## Challenge 1: Create a Basic Animal Class

**Task**: Create a basic `Animal` class with the following properties and methods:

- Properties: `name` (str), `species` (str), `age` (int)
- Methods: `make_sound()` that returns a generic animal sound

**Example usage**:
```python
animal = Animal(name="Generic", species="Unknown", age=1)
print(animal.make_sound())  # Should return "Some generic animal sound"
```

**Difficulty**: Easy
**Type**: Coding

---

## Challenge 2: Multiple Choice - Class Instantiation

**Question**: What happens when you create an instance of a class?

**Options**:
A) The `__init__` method is automatically called
B) A new object is created in memory
C) The class blueprint is copied
D) All of the above

**Correct Answer**: D) All of the above

**Difficulty**: Easy
**Type**: Multiple Choice

---

## Challenge 3: Inheritance - Create a Dog Class

**Task**: Create a `Dog` class that inherits from the `Animal` class and:

- Overrides the `make_sound()` method to return "Woof!"
- Adds a new method `fetch()` that returns "I'm fetching the ball!"

**Example usage**:
```python
dog = Dog(name="Buddy", species="Canine", age=3)
print(dog.make_sound())  # Should return "Woof!"
print(dog.fetch())       # Should return "I'm fetching the ball!"
```

**Difficulty**: Medium
**Type**: Coding

---

## Challenge 4: Multiple Choice - Method Parameters

**Question**: In a class method, what does the `self` parameter represent?

**Options**:
A) The class itself
B) The current instance of the class
C) A static reference to the class
D) The parent class

**Correct Answer**: B) The current instance of the class

**Difficulty**: Easy
**Type**: Multiple Choice

---

## Challenge 5: Add Behavior to Animal Class

**Task**: Add a method to the `Animal` class called `eat()` that:

- Takes a parameter `food` (str)
- Returns a string like "{name} is eating {food}"

**Example usage**:
```python
lion = Animal(name="Simba", species="Lion", age=2)
print(lion.eat("meat"))  # Should return "Simba is eating meat"
```

**Difficulty**: Easy
**Type**: Coding

---

## Challenge 6: Multiple Choice - Class Properties

**Question**: How do you access a property of a class instance?

**Options**:
A) `ClassName.property`
B) `instance.property`
C) `self.property`
D) Both A and B

**Correct Answer**: B) `instance.property`

**Difficulty**: Easy
**Type**: Multiple Choice

---

## Challenge 7: Create a Cat Class with Special Behavior

**Task**: Create a `Cat` class that inherits from `Animal` and:

- Overrides `make_sound()` to return "Meow!"
- Adds a property `lives` (int) with default value 9
- Adds a method `lose_life()` that decrements `lives` by 1

**Example usage**:
```python
cat = Cat(name="Whiskers", species="Feline", age=1)
print(cat.make_sound())  # Should return "Meow!"
print(cat.lives)         # Should return 9
cat.lose_life()
print(cat.lives)         # Should return 8
```

**Difficulty**: Medium
**Type**: Coding

---

## Challenge 8: Multiple Choice - Method Overriding

**Question**: What happens when a child class overrides a parent class method?

**Options**:
A) The parent method is completely replaced
B) The child method is called instead of the parent
C) Both parent and child methods are called
D) Both A and B

**Correct Answer**: D) Both A and B

**Difficulty**: Medium
**Type**: Multiple Choice

---

## Challenge 9: Add Default Values to Animal Class

**Task**: Modify the `Animal` class `__init__` method to:

- Make `age` have a default value of 1
- Make `species` have a default value of "Unknown"

**Example usage**:
```python
animal = Animal(name="Mystery")
print(animal.age)     # Should return 1
print(animal.species) # Should return "Unknown"
```

**Difficulty**: Easy
**Type**: Coding

---

## Challenge 10: Create a Bird Class with Flying

**Task**: Create a `Bird` class that inherits from `Animal` and:

- Adds a property `can_fly` (bool) with default value True
- Adds a method `fly()` that returns "I'm flying!" if `can_fly` is True, otherwise "I can't fly"

**Example usage**:
```python
parrot = Bird(name="Polly", species="Parrot", age=2)
print(parrot.fly())  # Should return "I'm flying!"

penguin = Bird(name="Pingu", species="Penguin", age=3, can_fly=False)
print(penguin.fly()) # Should return "I can't fly"
```

**Difficulty**: Medium
**Type**: Coding

---

## Challenge 11: Multiple Choice - Class Design

**Question**: What principle does the following code demonstrate?
```python
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

class Dog(Animal):
    def bark(self):
        return "Woof!"
```

**Options**:
A) Encapsulation
B) Inheritance
C) Polymorphism
D) Abstraction

**Correct Answer**: B) Inheritance

**Difficulty**: Medium
**Type**: Multiple Choice

---

## Challenge 12: Add Type Hints to Animal Class

**Task**: Add type hints to the `Animal` class methods and properties.

**Example solution**:
```python
class Animal:
    def __init__(self, name: str, species: str = "Unknown", age: int = 1):
        self.name: str = name
        self.species: str = species
        self.age: int = age

    def make_sound(self) -> str:
        return "Some generic animal sound"

    def eat(self, food: str) -> str:
        return f"{self.name} is eating {food}"
```

**Difficulty**: Easy
**Type**: Coding

---

## Challenge 13: Create a Zoo Class

**Task**: Create a `Zoo` class that:

- Has a property `animals` (list) initialized as an empty list in `__init__`
- Has a method `add_animal()` that takes an `Animal` instance and adds it to the list
- Has a method `animal_sounds()` that returns a list of sounds from all animals

**Example usage**:
```python
zoo = Zoo()
dog = Dog(name="Rex", species="Canine", age=4)
cat = Cat(name="Fluffy", species="Feline", age=2)
zoo.add_animal(dog)
zoo.add_animal(cat)
print(zoo.animal_sounds())  # Should return ["Woof!", "Meow!"]
```

**Difficulty**: Hard
**Type**: Coding

---

## Challenge 14: Multiple Choice - Class Relationships

**Question**: What is the relationship between a parent class and a child class?

**Options**:
A) Composition
B) Inheritance
C) Association
D) Aggregation

**Correct Answer**: B) Inheritance

**Difficulty**: Medium
**Type**: Multiple Choice

---

## Challenge 15: Add Validation to Animal Class

**Task**: Modify the `Animal` class to validate that:

- `age` is a positive integer
- `name` is not empty

Raise appropriate exceptions if validation fails.

**Example usage**:
```python
try:
    animal = Animal(name="", species="Unknown", age=1)
except ValueError as e:
    print(e)  # Should print error about empty name

try:
    animal = Animal(name="Valid", species="Unknown", age=-1)
except ValueError as e:
    print(e)  # Should print error about negative age
```

**Difficulty**: Hard
**Type**: Coding