# Lazy Iterators

[toc]

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1UWSD3cpDQ5ia-EDbSrjHYnLQOL2hHRhJ?usp=sharing)

## Cyclic Iterators

- In Python, we can also create Cyclic Iterators

- Cyclic Iterators are infinite iterators which can provide any number of data elements in the cyclic fashion

- Python has in-built cyclic iterators in the `itertools` module

- Below example shows the cyclic iterator to print the `NSWE` alphabets in a cyclic manner for 10 alphabets

  ```python
  import itertools
  
  n = 10
  iter_cycl = itertools.cycle('NSWE')
  [f'{i}{next(iter_cycl)}' for i in range(1, n+1)]
  ```

- We can also create a custom cyclic iterator

  ```python
  class CyclicIterator:
      def __init__(self, lst):
          self.lst = lst
          self.i = 0
  
      def __iter__(self):
          return self
  
      def __next__(self):
          result = self.lst[self.i % len(self.lst)]
          self.i += 1
          return result
  
  iter_cycl = CyclicIterator('NSWE')
  
  for i in range(10):
      print(next(iter(iter_cycl)))
  ```

  

## Lazy Iterables

- The Iterables we have defined till now, has a finite length which is defined during instantiating the Iterable

- Such Iterables pre-compute all the data for all the elements of the iterable

- This adds extra memory usage since all the computations results need to stored in the memory

- Lazy Iterables are the kind of Iterables which are of infinite length and then perform the compute on specific range of data, only when they are asked to do so

- Lazy Iterators are responsible for making the Iterables as Lazy Iterables and they can be accessed by using `iter()` method on the Iterable

- The following class is a lazy iterable which calculates the squares only when it is called and does not pre-compute squares for a range of data

  ```python
  # Square Iterable
  class Squares:
    def __iter__(self):
      return self.SquareIterator()
  
    # Square Iterator
    class SquareIterator:
      def __init__(self):
        self.i = 0
  
      def __iter__(self):
        return self
  
      def __next__(self):
        result = self.i ** 2
        self.i += 1
        return result
  ```

  ```python
  # Initializing Lazy Iterable
  square_lazy_iterables = Squares()
  
  # Accessing Lazy Iterator from the Iterable
  square_lazy_iterator = iter(square_lazy_iterables)
  
  # The compute is only performed when the iterator is called
  for _ in range(10):
      print(next(square_lazy_iterator))
  ```

- `range()`, `zip()` and `enumerate()`  is an in-built Lazy Iterables in Python

- Their instantiate speed and operation speed proves that they are lazy iterables in Python



## Sorting Iterables

- To perform sorting, the iterables needs to a finite Iterable

- Sorting can be done by using `sorted()`

- In order to sort in reverse order, we can use `sorted(iterable, reverse=True)`

- The following example shows random number generating Iterable and sorting the 10 random number in normal and reverse order

  ```python
  import random
  
  class RandomInts:
      def __init__(self, length, *, seed=0, lower=0, upper=10):
          self.length = length
          self.seed = seed
          self.lower = lower
          self.upper = upper
          
      def __len__(self):
          return self.length
      
      def __iter__(self):
          return self.RandomIterator(self.length, 
                                     seed = self.seed, 
                                     lower = self.lower,
                                     upper=self.upper)
      
      
      class RandomIterator:
          def __init__(self, length, *, seed, lower, upper):
              self.length = length
              self.lower = lower
              self.upper = upper
              self.num_requests = 0
              random.seed(seed)
              
          def __iter__(self):
              return self
          
          def __next__(self):
              if self.num_requests >= self.length:
                  raise StopIteration
              else:
                  result = random.randint(self.lower, self.upper)
                  self.num_requests += 1
                  return result
  
  randoms = RandomInts(10)
  ```

  ```python
  sorted(randoms)
  sorted(randoms, reverse=True)
  ```



## Iterating Callable

- We can use closures as a part of iterator

- Closures will update their nonlocal variable everytime the Iterator is called

- The closures will be updated in the `__next__()` function of the iterator 

- This block of code is a closure which updates the counter everytime the closure is called

  ```python
  # CLOSURES
  def counter():
      i = 0
      def inc():
          nonlocal i 
          i += 1
          return i
      return inc
  ```

- This block of code is an Iterator which initializes the closure in the `__init__()` method of the Iterator

  ```python
  # ITERATOR
  class CounterIterator:
      def __init__(self, counter_callable, sentinel):
          self.counter_callable = counter_callable
          self.sentinel = sentinel
          self.is_consumed = False
  
      def __iter__(self):
          return self
  
      def __next__(self):
          if self.is_consumed:
              raise StopIteration
          else:
              result = self.counter_callable()
              if result == self.sentinel:
                  self.is_consumed = True
                  raise StopIteration
  
              else:
                  return result
  ```

- This code block shows that everytime we iterate over the iterator, the counter closure updates its value and the value is returned by the iterator

  ```python
  cnt = counter()
  cnt_iter = CounterIterator(cnt, 5)
  
  for c in cnt_iter:
      print(c)
  ```



## Delegating Iterators

- Delegating Iterators are the kind of Iterators which has a dataset that is an Iterator

- Since the dataset itself is an Iterator, we do not need to write the `__next__()` method 

- This is how we delegate the work by adding dataset which itself is an Iterator

- The class that we have created for this purpose is an Iterable

- NamedTuples are Iterators which are added to the `PersonNames` class which makes the class iterable

- We have not added the `__next__()` method to the class and still we can iterate over it

  ```python
  from collections import namedtuple
  
  Person = namedtuple('Person', 'first last')
  
  class PersonNames:
      def __init__(self, persons):
          try:
              self._persons = [person.first.capitalize()
                               + ' ' + person.last.capitalize()
                              for person in persons]
          except (TypeError, AttributeError):
              self._persons = []
  
      def __iter__(self):
          return iter(self._persons)
  ```

  ```python
  persons = [Person('michaeL', 'horDON'), Person('srikanth', 'latify'), Person('maX', 'VertaPPEn')]
  
  person_names = PersonNames(persons)
  
  for p in person_names:
      print(p)
  ```



## Reversed Iteration

- The Iterables can by reversed by overwriting the `__reversed__` method of the Iterable

- The `__reversed__` method will return an Iterator object with an argument flag to reverse the elements

- The `__ next__()` method of the iterator will return the in reverse order if flag for reverse is raised

- In the below example, an Iterable is created for deck of cards and the deck is called in the reverse order by implementing the `__reversed__()` method

  ```python
  _SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
  _RANKS = tuple(range(2, 11) ) + ('J', 'Q', 'K', 'A')
  from collections import namedtuple
  
  Card = namedtuple('Card', 'rank suit')
  
  class CardDeck:
      def __init__(self):
          self.length = len(_SUITS) * len(_RANKS)
  
      def __len__(self):
          return self.length
      
      def __iter__(self):
          return self.CardDeckIterator(self.length)
          
      def __reversed__(self):
          return self.CardDeckIterator(self.length, reverse=True)
      
      class CardDeckIterator:
          def __init__(self, length, *, reverse=False):
              self.length = length
              self.reverse = reverse
              self.i = 0
              
          def __iter__(self):
              return self
          
          def __next__(self):
              if self.i >= self.length:
                  raise StopIteration
              else:
                  if self.reverse:
                      index = self.length -1 - self.i
                  else:
                      index = self.i
                  suit = _SUITS[index // len(_RANKS)]
                  rank = _RANKS[index % len(_RANKS)]
                  self.i += 1
                  return Card(rank, suit)
  ```

  ```python
  deck = CardDeck()
  
  deck = reversed(CardDeck())
  for card in deck:
      print(card)
  ```



## Using Iterators as function arguments

- Iterators can also be used as an arguments for the functions

- The important point to note here is that Iterators are exhaustible

- Once they are called as exhausted then they won't return any data which will lead to the `ValueError`

- In the below code block, an Iterator is created to generate random numbers

  ```python
  import random
  
  class Randoms:
      def __init__(self, n):
          self.n = n
          self.i = 0
          
      def __iter__(self):
          return self
      
      def __next__(self):
          if self.i >= self.n:
              raise StopIteration
          else:
              self.i += 1
              return random.randint(0, 100)
  ```

- The iterator is initialized and iterated over all the elements by the `min()`

  ```python
  random.seed(0)
  l = Randoms(10)
  
  min(l)
  ```

- Since all the elements are exhausted, the `max()` function will return `ValueError` on the same iterator

  ```python
  max(l)
  ```

  

---



# Code Details

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/18Uog28L9AdZ4uco65BUma3w8CZ0ArEMv?usp=sharing)

## Goal 1

### Problem Statement

Refactor the Polygon class so that all the calculated properties are lazy properties, i.e. they should still be calculated properties, but they should not have to get recalculated more than once (since we made our Polygon class "immutable").



### Solution

- The two main parts for this goal are:
  1. All the calculated properties are lazy properties i.e. they should not have to get recalculated
  2. Polygon class should be immutable
- For achieve the goal, I have tried 3 approached in which the 3rd approach satisfied the goal conditions



#### Approach 1

- In order to make sure that properties are not calculated again and again, I started with modifying the memoize decorator for properties

  ```python
  def memoize(fn):
      """
      Decorator for memoization
      :param fn: Function on which memoization to be implemented
      :return: Closure (inner)
      """
      from functools import wraps
      cache = dict()
  
      @wraps(fn)
      def inner(self=None):
          """
          Closure to store and update cache
          :param args: arguments passed to the function
          :return: output of the function from cache if output is present in cache
          """
          if fn.__name__ not in cache:
              cache[fn.__name__] = fn(self)
          return cache[fn.__name__]
      return inner
  ```

- Using this decorator on the properties made the properties lazy

  ```python
  class Polygon(object):
      def __init__(self, n, R):
          if n < 3:
              raise ValueError('Polygon must have at least 3 vertices.')
          self._n = n
          self._R = R
          self.cache = dict()
          
      def __repr__(self):
          return f'Polygon(n={self._n}, R={self._R})'
      
      @property
      @memoize
      def count_vertices(self):
          return self._n
      
      @property
      @memoize
      def count_edges(self):
          return self._n
      
      @property
      @memoize
      def circumradius(self):
          return self._R
      
      @property
      @memoize
      def interior_angle(self):
          return (self._n - 2) * 180 / self._n
  
      @property
      @memoize
      def side_length(self):
          return 2 * self._R * math.sin(math.pi / self._n)
      
      @property
      @memoize
      def apothem(self):
          return self._R * math.cos(math.pi / self._n)
      
      @property
      @memoize
      def area(self):
          return self._n / 2 * self.side_length * self.apothem
      
      @property
      @memoize
      def perimeter(self):
          return self._n * self.side_length
      
      def __eq__(self, other):
          if isinstance(other, self.__class__):
              return (self.count_edges == other.count_edges 
                      and self.circumradius == other.circumradius)
          else:
              return NotImplemented
          
      def __gt__(self, other):
          if isinstance(other, self.__class__):
              return self.count_vertices > other.count_vertices
          else:
              return NotImplemented
  ```

- But the issue with this approach was - whenever I was creating another instance of the same class Polygon, it was still returning the cached data for the properties. This is a functional error so I changed the approach



#### Approach 2

- This approach is referred from [this link](https://www.programmersought.com/article/5402869953/)

- In this approach, a lazy decorator was created using class as a decorator

  ```python
  class lazy(object):
      def __init__(self, func):
          self.func = func
   
      def __get__(self, instance, cls):
          val = self.func(instance)
          setattr(instance, self.func.__name__, val)
          return val
  ```

- After decorating the properties with this decorator, the functionality part was achieved

  ```python
  class LazyPolygon:
      def __init__(self, n, R):
          if n < 3:
              raise ValueError('Polygon must have at least 3 vertices.')
          self._n = n
          self._R = R
          self.cache = dict()
          
      def __repr__(self):
          return f'Polygon(n={self._n}, R={self._R})'
      
      @lazy
      def count_vertices(self):
          return self._n
      
      @lazy
      def count_edges(self):
          return self._n
      
      @lazy
      def circumradius(self):
          return self._R
      
      @lazy
      def interior_angle(self):
          return (self._n - 2) * 180 / self._n
  
      @lazy
      def side_length(self):
          return 2 * self._R * math.sin(math.pi / self._n)
      
      @lazy
      def apothem(self):
          return self._R * math.cos(math.pi / self._n)
      
      @lazy
      def area(self):
          return self._n / 2 * self.side_length * self.apothem
      
      @lazy
      def perimeter(self):
          return self._n * self.side_length
      
      def __eq__(self, other):
          if isinstance(other, self.__class__):
              return (self.count_edges == other.count_edges 
                      and self.circumradius == other.circumradius)
          else:
              return NotImplemented
          
      def __gt__(self, other):
          if isinstance(other, self.__class__):
              return self.count_vertices > other.count_vertices
          else:
              return NotImplemented
  ```

- This approach worked but had an issue - properties were mutable

- After creating an instance, all the properties were calculated lazily but the properties were mutable so I could define an object of regular polygon with 3 edges, get all it's parameters and still change the number of edges while keeping the other parameter same

- Since the class was not mutable, I tried another approach



#### Approach 3

- In this approach, again referenced from [this link](https://www.programmersought.com/article/5402869953/), a decorator is created and applied on the properties

- The decorator checks if the property is already available, if it's not then only it is calculated otherwise the available value is returned

  ```python
  def lazy_property(func):
      """
      Decorator function for lazy calculations of the property
      :param func: method to be decorator
      :return: closure
      """
      attr_name = "_lazy_" + func.__name__
   
      @property
      def _lazy_property(self):
          """
          Function to calculate the property if not already done
          :param self: instance
          :return: value of the property
          """
          if not hasattr(self, attr_name):
              setattr(self, attr_name, func(self))
          return getattr(self, attr_name)
      return _lazy_property
  ```

- After decorating the properties, the class properties become lazy and the class also becomes immutable i.e. we cannot change the value of the properties externally

  ```python
  class Polygon:
      """
      Class for lazy properties
      """
      def __init__(self, n, circumradius):
          """
          Constructor
          """
          if n < 3:
              raise ValueError('Polygon must have at least 3 vertices.')
          self._n = n
          self._R = circumradius
          self.cache = dict()
          
      def __repr__(self):
          """
          Function to print the details of class instance
          """
          return f'Polygon(n={self._n}, R={self._R})'
      
      @lazy_property
      def count_vertices(self):
          """
          Property to return number of vertices of the regular polygon
          """
          return self._n
      
      @lazy_property
      def count_edges(self):
          """
          Property to return number of edges of the regular polygon
          """
          return self._n
      
      @lazy_property
      def circumradius(self):
          """
          Property to return circumradius of the regular polygon
          """
          return self._R
      
      @lazy_property
      def interior_angle(self):
          """
          Property to return interior angle of the regular polygon
          """
          return (self._n - 2) * 180 / self._n
  
      @lazy_property
      def side_length(self):
          """
          Property to return length of each side of the regular polygon
          """
          return 2 * self._R * math.sin(math.pi / self._n)
      
      @lazy_property
      def apothem(self):
          """
          Property to return perpendicular distancd from center of circle to side of the regular polygon
          """
          return self._R * math.cos(math.pi / self._n)
      
      @lazy_property
      def area(self):
          """
          Property to return area of the regular polygon
          """
          return self._n / 2 * self.side_length * self.apothem
      
      @lazy_property
      def perimeter(self):
          """
          Property to return perimeter of the regular polygon
          """
          return self._n * self.side_length
      
      def __eq__(self, other):
          """
          Property to implement equality operator for multiple regular polygon
          """
          if isinstance(other, self.__class__):
              return (self.count_edges == other.count_edges 
                      and self.circumradius == other.circumradius)
          else:
              return NotImplemented
          
      def __gt__(self, other):
          """
          Property to implement greater than operator for multiple regular polygon
          """
          if isinstance(other, self.__class__):
              return self.count_vertices > other.count_vertices
          else:
              return NotImplemented
  ```

- This approach worked properly and made the properties lazy as well as the class immutable



### Test Cases

The test cases for `goal_1.py` are in `test_goal_1.py`

| Test Case             | Description                                                  |
| --------------------- | ------------------------------------------------------------ |
| `test_polygon()`      | Test case to check functionality of polygon class            |
| `test_immutability()` | Test case to check if the polygon is immutable               |
| `test_outputs()`      | Test case to check if proper outputs are created when another instance is created |





## Goal 2

### Problem Statement

Refactor the Polygons (sequence) type, into an iterable. Make sure also that the elements in the iterator are computed lazily - i.e. you can no longer use a list as an underlying storage mechanism for your polygons.

You'll need to implement both an iterable, and an iterator.



### Solution

- To convert the class into an Iterable, I have added the `PolygonIterator` class and the `__iter__` method to the `Polygon` class

- `ratio_data` and `get_collection` are also added to the `PolygonIterator` class in order to use them for slicing, indexing and calculating maximum efficiency polygon

- The `__len__` method is used to print the number of polygons present in the collection

- The `__repr__` method provides details about the collection

- The `__getitem__` method is implemented to access the instances of polygons by indexing and slicing

- The `max_efficiency_polygon` property is added to calculate the number of edges of polygon with maximum area to perimeter ratio

  ```python
  class Polygons:
      """
      Iterable for regular polygons
      """
      def __init__(self, circumradius):
          """
          Constructor
          :param circumradius: radius of a circle in which the polygons are inscribed in
          """
          if circumradius < 0:
              raise ValueError('R must be greater than 0')
          self._m = 2
          self._R = circumradius
          self._instance = None
  
      def __iter__(self):
          """
          Method to make this class Iterable
          :return: Instance of the Iterator class
          """
          self._instance = self.PolygonIterator(self)
          return self._instance
  
      class PolygonIterator:
          """
          Iterator class for the Iterable
          """
          def __init__(self, obj):
              """
              Constructor
              """
              self._obj = obj
              self._ratio_data = dict()
              self.collection = []
  
          def __iter__(self):
              """
              Method to make this class Iterator
              """
              return self
  
          def __next__(self):
              """
              Method to iterate over the values of iterator
              """
              # Increment the number of edges
              self._obj._m += 1
  
              # Create a polygon with number of edges and circumradius
              polygon = Polygon(self._obj._m, self._obj._R)
  
              # Calculate the ratio using the porperties of the polygon
              ratio = polygon.area / polygon.perimeter
  
              # Keep a record of edges and ratio
              if self._obj._m not in self._ratio_data:
                  self._ratio_data[self._obj._m] = ratio
  
              # Append all the polygon instances
              self.collection.append(polygon)
  
              return polygon
  
          @property
          def ratio_data(self):
              """
              Property to access ratio of area to perimeter of all the polygon
              """
              return self._ratio_data
  
          @property
          def get_collection(self):
              """
              Property to access instances of all the polygons
              """
              return self.collection
          
      def __len__(self):
          """
          Method to print the number of polygons in an instance
          """
          return len(self._instance.ratio_data)
      
      def __repr__(self):
          """
          Method to print information of collections
          """ 
          return f'Collection of regular Polygons from edges 3 to {len(self._instance.ratio_data) + 2}'
      
      def __getitem__(self, index):
          """
          Method to access the polygons using slicing and indexing
          """
          if isinstance(index, int):
              if index < 0:
                  index = len(self._instance.ratio_data) + index
              if index < 0 or index > len(self._instance.ratio_data):
                  raise IndexError
              else:
                  return self._instance.get_collection[index]
          else:
              start, stop, step = index.indices(len(self._instance.ratio_data))
              rng = range(start, stop, step)
              return [self._instance.get_collection[index] for index in rng]
      
      @property
      def max_efficiency_polygon(self):
          """
          Property to access the number of edges of a polygon with maximum area to perimeter ratio
          """
          sorted_polygons = sorted(self._instance.ratio_data, reverse=True)
          return sorted_polygons[0]
  ```

  

### Test Cases

The test cases for `goal_2.py` are in `test_goal_2.py`

| Test Cases                   | Description                                                 |
| ---------------------------- | ----------------------------------------------------------- |
| `test_polygons_iterable()`   | Test case to check if Polygons is Iterable                  |
| `test_repr_implementation()` | Test case to check if `__repr__` is implemented             |
| `test_len_implementation()`  | Test case to check if `__len__` is implemented              |
| `test_indexing()`            | Test case to check if indexing is implemented               |
| `test_slicing()`             | Test case to check if slicing is implemented                |
| `test_max_efficiency()`      | Test case to check if maximum efficiency polygon is correct |

