
from urllib.parse import parse_qs
from itertools import islice
from datetime import datetime
import json

# =============================================================================
# E.P.1 i4: Write Helper Functions Instead of Complex Expressions
# =============================================================================

"""
Move complex expressions into helper functions, especially if you need to use the
same logic repeatedly.
"""

my_values = parse_qs('red=5&blue=0&green=',
                     keep_blank_values=True)
my_values
my_values['green']
my_values.get('green')
my_values.get('opacity')

# one liners are hard to read
green = my_values.get('green', [''])[0] or 0
opacity = my_values.get('opacity', [''])[0] or 0 # 0 as default
red = int(my_values.get('red', [''])[0] or 0)

# clearer with ternary
red = my_values.get('red', [''])
red = int(red[0]) if red[0] else 0

# even clearer
green = my_values.get('green', [''])
if green[0]:
    green = int(green[0])
else:
    green = 0

# clearest with a helper function
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        found = int(found[0])
    else:
        found = default
    return found

green = get_first_int(my_values, 'green')


# =============================================================================
# E.P.1 i14: Prefer Exceptions to Returning None
# =============================================================================

def divide(a, b):
    try:
        return a/b
    except ZeroDivisionError:
        return None

x, y = 0, 5
result = divide(x, y)
# Functions that return None to indicate special meaning are error prone
if not result:
    print('Invalid inputs') # This is wrong!

# slightly better
def divide(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None

success, result = divide(x, y)
if not success:
    print('Invalid inputs')

# best, raise exceptions to indicate special situations instead of returning None
def divide(a, b):
    try:
        return a/b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e

x, y = 5, 2
# expect the calling code to handle exceptions properly when they’re documented
try:
    result = divide(x, y)
except ValueError:
    print('Invalid inputs')
else:
    print('Result is %.1f' % result)

# =============================================================================
# E.P.1 i15: Know How Closures Interact with Variable Scope
# =============================================================================

def sort_priority(values, group):
    def helper(x):
        if x in group:
           return (0, x)
        return (1, x)
    values.sort(key=helper)

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)

def sort_priority(numbers, group):
    found = False
    def helper(x):
        # indicate when a closure can modify a variable in its enclosing scopes
        # caution against using nonlocal for anything beyond simple functions
        nonlocal found
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

# better, avoids nonlocal
class Sorter(object):
    def __init__(self, group):
        self.group = group
        self.found = False
    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)
        return (1, x)
sorter = Sorter(group)
numbers.sort(key=sorter)
assert sorter.found is True

# =============================================================================
# E.P.1 i16: Consider Generators Instead of Returning Lists
# =============================================================================

def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1) # cubersome, can ran out of memory
    return result

address = 'Four score and seven years ago…'
result = index_words(address)
result

# better solution with generator
def index_words_iter(text):
    if text: 
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1
            
list(index_words_iter(address))

# better for large input
def index_file(handle):
    offset = 0
    for line in handle: # for arbitrarily large inputs
        if line:
            yield offset
        for letter in line:
            offset += 1
            if letter == ' ':
                yield offset

with open('/tmp/address.txt', 'r') as f:
    it = index_file(f)
    results = islice(it, 0, 3)
    print(list(results))

# =============================================================================
# E.P.1 i17: Be Defensive When Iterating Over Arguments
# =============================================================================

def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100*value/total
        result.append(percent)
    return result

visits = [15, 35, 80]
percentages = normalize(visits)

def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)

it = read_visits('/tmp/my_numbers.txt')
percentages = normalize(it)
percentages # []

"""
The iterator protocol is how Python for loops and related expressions traverse the
contents of a container type. When Python sees a statement like for x in foo it will
actually call iter(foo). The iter built-in function calls the foo.__iter__ special
method in turn. The __iter__ method must return an iterator object (which itself
implements the __next__ special method). Then the for loop repeatedly calls the
next built-in function on the iterator object until it's exhausted (and raises a
StopIteration exception).
https://docs.python.org/3.7/tutorial/classes.html#iterators
"""

class ReadVisits(object):
    """
    iterable container
    """
    
    def __init__(self, data_path):
        self.data_path = data_path
    
    def __iter__(self):
        """
        allocate a new iterator object each time it gets called
        """
        with open(self.data_path) as f:
            for line in f:
                yield int(line)

visits = ReadVisits('/tmp/my_numbers.txt')
percentages = normalize(visits) # [11.5, 26.9, 61.5]

it = visits.__iter__()
next(it)

def normalize_defensive(numbers):
    if iter(numbers) is iter(numbers): # An iterator — bad!
        raise TypeError('Must supply a container')
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

visits = [15, 35, 80]
normalize_defensive(visits) # No error
it = iter(visits) # returns iterator
normalize_defensive(it) # error
visits = ReadVisits('/tmp/my_numbers.txt')
normalize_defensive(visits) # No error

iter(visits)

# =============================================================================
# E.P.1 i18: Reduce Visual Noise with Variable Positional Arguments
# =============================================================================

def log(message, *values): # optional *args
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print('%s: %s' % (message, values_str))

log('My numbers are', 1, 2)
log('Hi there') # Much better
favorites = [7, 33, 99]
log('Favorite colors', *favorites)

def my_generator():
    for i in range(10):
        yield i
        
def my_func(*args): # best when #args is small
    print(args)
    
it = my_generator()
my_func(*it) # turned into a tuple before passed to your function

#use keyword-only arguments when you want to extend functions that accept *args

# =============================================================================
# E.P.1 i19: Provide Optional Behavior with Keyword Arguments
# =============================================================================

def remainder(number, divisor):
    return number % divisor

# Optional keyword arguments should always be passed by keyword instead of by
# position.

# =============================================================================
# E.P.1 i20: Use None and Docstrings to Specify Dynamic Default Arguments
# =============================================================================

# Default arguments are only evaluated once 
# during function definition at module load time.
def log(message, when=datetime.now()): # now() only executed once
    print('%s: %s' % (when, message))
log('Hi there!')
log('Hi again!')

def log(message, when=None):
    """
    Log a message with a timestamp.
    Args:
        message: message to print.
        when: datetime of when the message occurred.
        Defaults to the present time.
    """
    when = datetime.now() if when is None else when
    print('%s: %s' % (when, message))

def decode(data, default=None):
    """
    Load JSON data from a string.
    Args:
        data: JSON data to decode.
        default: Value to return if decoding fails.
        Defaults to an empty dictionary.
    """
    if default is None:
        default = {}
    try:
        return json.loads(data)
    except ValueError:
        return default

a = decode('a', {'c': 'c'})
b = decode('b', {'c': 'c'})
a is b

# =============================================================================
# E.P.1 i21: Enforce Clarity with Keyword-Only Arguments
# =============================================================================

def safe_division(number, divisor, *, # enforce keyword only arguments
                  ignore_overflow=False, 
                  ignore_zero_division=False):
    try:
        return number/divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

safe_division(1, 10**500, ignore_overflow=True)
safe_division(1, 0, ignore_zero_division=True)
safe_division(1, 10**500, True, False)

# =============================================================================
# E.P.1 i42: Define Function Decorators with functools.wraps
# =============================================================================

def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r, %r) -> %r' %
              (func.__name__, args, kwargs, result))
        return result
    return wrapper

# equivalent to fibonacci = trace(fibonacci)
@trace
def fibonacci(n):
    """ 
    Return the n-th Fibonacci number
    """
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))

fibonacci(3)

# can cause strange behaviors in tools such as debuggers
fibonacci # breaks
help(fibonacci) # breaks

from functools import wraps
"""
a decorator that helps you write decorators.
it copies all of the important metadata about the inner function 
to the outer function. ensures
"""

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r, %r) -> %r' %
              (func.__name__, args, kwargs, result))
        return result
    return wrapper

@trace
def fibonacci(n):
    """ 
    Return the n-th Fibonacci number
    """
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))

fibonacci
help(fibonacci)













































