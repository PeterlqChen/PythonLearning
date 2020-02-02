

from collections import deque # use collections.deque for queue
from math import pi
from random import randint

# =============================================================================
# from https://docs.python.org/3/tutorial/datastructures.html
# =============================================================================

queue = deque(["Eric", "John", "Michael"])
queue.append("Terry")
queue.popleft() 

#list(map(lambda x: x**2, range(10)))
[x**2 for x in range(10)]
[(x, x**2) for x in range(6)]
vec = [[1,2,3], [4,5,6], [7,8,9]]
[num for elem in vec for num in elem]

[str(round(pi, i)) for i in range(1, 6)]

matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ]
[[row[i] for row in matrix] for i in range(4)] # transpose
list(zip(*matrix)) # Unpacking Argument Lists
list(zip([1, 2, 3, 4], [5, 6, 7, 8]))

empty = ()
singleton = 'hello',

basket = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}   
basket
a = set('abracadabra')
b = set('alacazam')
a 
b                                 # unique letters in a
a - b                              # letters in a but not in b
a | b                              # letters in a or b or both
a & b                              # letters in both a and b
a ^ b                 
a = {x for x in 'abracadabra' if x not in 'abc'}
a

tel = {'jack': 4098, 'sape': 4139}
list(tel)
sorted(tel)
dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
{x: x**2 for x in (2, 4, 6)}
dict(sape=4139, guido=4127, jack=4098)

for i, v in enumerate(['tic', 'tac', 'toe']):
    print(i, v)

questions = ['name', 'quest', 'favorite color']
answers = ['lancelot', 'the holy grail', 'blue']
for q, a in zip(questions, answers):
    print('What is your {0}?  It is {1}.'.format(q, a))

for i in reversed(range(1, 10, 2)):
    print(i)

basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
for f in sorted(set(basket)):
    print(f)

(1, 2, 3)              < (1, 2, 4)
[1, 2, 3]              < [1, 2, 4]
'ABC' < 'C' < 'Pascal' < 'Python'
(1, 2, 3, 4)           < (1, 2, 4)
(1, 2)                 < (1, 2, -1)
(1, 2, 3)             == (1.0, 2.0, 3.0)
(1, 2, ('aa', 'ab'))   < (1, 2, ('abc', 'a'), 4)

# =============================================================================
# E.P.1 i5: Know How to Slice Sequences
# =============================================================================

a = list(bytes(list(range(97, 107))).decode('utf-8'))
a[:]
first_twenty_items = a[:20] # slicing returns a copy
last_twenty_items = a[-20:]
a[20]
a[2:7] = [99, 22, 14] # list will grow or shrink
b = a[:]
assert b == a and b is not a
b = a
a[:] = [101, 102, 103]
assert a is b

# =============================================================================
# E.P.1 i6: Avoid Using start, end, and stride in a Single Slice
# =============================================================================

a = list(bytes(list(range(97, 107))).decode('utf-8'))
a[::2] # Prefer positive stride values in slices without start or end indexes.
a[1::2]
a[::-1] # Avoid negative stride values if possible.

x = b'abc'
x[::-1]

w = '你好吗'
w[::-1]
x = w.encode('utf-8')
x
y = x[::-1]
y.decode('utf-8') # error

# Avoid using start, end, and stride together in a single slice
# consider using one assignment to stride and another to slice.
# or use islice from the itertools
b = a[::2] 
c = b[1:-1] 

# =============================================================================
# E.P.1 i7: Use List Comprehensions Instead of map and filter
# =============================================================================

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = map(lambda x: x ** 2, a)
list(squares)
squares = [x**2 for x in a] # easier to read
even_squares = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
even_squares = [x**2 for x in a if x % 2 == 0] # easier to read

chile_ranks = {'ghost': 1, 'habanero': 2, 'cayenne': 3}
rank_dict = {rank: name for name, rank in chile_ranks.items()}
chile_len_set = {len(name) for name in rank_dict.values()}

# =============================================================================
# E.P.1 i8: Avoid More Than Two Expressions in List Comprehensions
# =============================================================================

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
squared = [[x**2 for x in row] for row in matrix]

a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
b = [x for x in a if x > 4 if x % 2 == 0]
c = [x for x in a if x > 4 and x % 2 == 0] # same

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
filtered = [[x for x in row if x % 3 == 0]
            for row in matrix if sum(row) >= 10]

# =============================================================================
# E.P.1 i9: Consider Generator Expressions for Large Comprehensions
# =============================================================================

[x**2 for x in range(20)] # can crash for large inputs
it = (x**2 for x in range(20)) # generator expression
it
next(it)
roots = ((x, x**0.5) for x in it) # Chaining generators executes very quickly
next(roots)

# =============================================================================
# E.P.1 i10: Prefer enumerate Over range
# =============================================================================

random_bits = 0
for i in range(5):
    if randint(0, 1):
        random_bits |= 1 << i
random_bits

flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
for i, flavor in enumerate(flavor_list, 1):
    print('%d: %s' % (i, flavor))

# =============================================================================
# E.P.1 i11: Use zip to Process Iterators in Parallel
# =============================================================================

names = ['Cecilia', 'Lise', 'Marie']
letters = [len(n) for n in names]

# better to have same length
zip(names, letters) # generator yielding tuples until one list is exhausted
list(zip(names, letters))

longest_name = None
max_letters = 0
for name, count in zip(names, letters):
    if count > max_letters:
        longest_name = name
        max_letters = count

# =============================================================================
# E.P.1 i46: Use Built-in Algorithms and Data Structures
# =============================================================================

# double-ended queue
fifo = deque()
fifo.append(1) # Producer
x = fifo.popleft() # Consumer

# ordered dictionary
# keeps track of the order in which its keys were inserted
# simplify testing and debugging by making all code deterministic
from collections import OrderedDict 

a = OrderedDict()
a['foo'] = 1
a['bar'] = 2
b = OrderedDict()
b['foo'] = 'red'
b['bar'] = 'blue'
for value1, value2 in zip(a.values(), b.values()):
    print(value1, value2)

# default dictionary
# automatically stores a default value when a key doesn't exist
from collections import defaultdict

int()
stats = defaultdict(int)
stats['my_counter'] += 1

# heap queue
from heapq import heappush, heappop, nsmallest

a = []
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 4)
a
type(a)
print(heappop(a), heappop(a), heappop(a), heappop(a))

nsmallest(1, a)[0]
a[0]

# bisection
x = list(range(10**6))
i = x.index(991234)

from bisect import bisect_left

# iterator tools
"""
Linking iterators together
• chain: Combines multiple iterators into a single sequential iterator.
• cycle: Repeats an iterator’s items forever.
• tee: Splits a single iterator into multiple parallel iterators.
• zip_longest: A variant of the zip built-in function that works well with
iterators of different lengths.
Filtering items from an iterator
• islice: Slices an iterator by numerical indexes without copying.
• takewhile: Returns items from an iterator while a predicate function returns
True.
• dropwhile: Returns items from an iterator once the predicate function returns
False for the first time.
• filterfalse: Returns all items from an iterator where a predicate function
returns False. The opposite of the filter built-in function.
Combinations of items from iterators
• product: Returns the Cartesian product of items from an iterator, which is a
nice alternative to deeply nested list comprehensions.
• permutations: Returns ordered permutations of length N with items from an
iterator.
• combination: Returns the unordered combinations of length N with
unrepeated items from an iterator.
"""


























