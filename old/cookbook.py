
# Unpacking of tagged tuples of varying sizes

p = (4, 5)
x, y = p

a = [1, 2, 3]
x, y, z = a
x

first, *middle, last = [1, 2, 3, 5]

def func(x, y):
    return x + y
func(*[1, 2])

line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
line.split(':')

records = [
     ('foo', 1, 2),
     ('bar', 'hello'),
     ('foo', 3, 4),
]

def do_foo(x, y):
    print('foo', x, y)

def do_bar(s):
    print('bar', s)

for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_bar(*args)
        


# generator

list(range(5))    
    
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x # turns the function to a generator
        x += increment

for n in frange(0, 4, 0.5):
    print(n)
list(frange(0, 4, 0.5))


# =============================================================================
# Functions
# =============================================================================


# Functions That Accept Any Number of Arguments
def avg(first, *rest):
    print(rest)
    return (first + sum(rest)) / (1 + len(rest))
avg(*[1, 2, 3])
avg(1, 2, 3)

def anyargs(*args, **kwargs):
    print(args) # A tuple
    print(kwargs) # A dict
anyargs(2, 4, 6, name='peter', grade='a+')

# Functions That Only Accept Keyword Arguments
def recv(maxsize, *, block):
    # place the keyword arguments after a * argument
    'Receives a message'
    pass
recv(1024, True) # TypeError
recv(1024, block=True) # Ok

def mininum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m
mininum(1, 5, 2, -5, 10) # Returns -5
mininum(1, 5, 2, -5, 10, clip=0) # Returns 0

# Attaching Informational Metadata to Function Arguments
def add(x:int, y:int) -> int:
    return x + y
help(add)
add.__annotations__

# Returning Multiple Values from a Function
def myfun():
    return 1, 2, 3
a, b, c = myfun()
a, *b = myfun()

# Defining Functions with Default Arguments
def spam(a, b=None):
    # Using a list as a default valuen
    # default values need to be immutable
    if b is None: # essential, don't write 'if not b'
        b = []

_no_value = object()
def spam(a, b=_no_value):
    if b is _no_value: 
        print('No b value supplied')
spam(1)
spam(1, 2)
spam(1, None)

# Defining Anonymous or Inline Functions
add = lambda x, y: x + y
add('hello', ' world')

names = ['David Beazley', 'Brian Jones',
         'Raymond Hettinger', 'Ned Batchelder']
sorted(names, key=lambda name: name.split()[-1].lower())

# Capturing Variables in Anonymous Functions
x = 5
f = lambda y: x + y
f(3)
x = 2
f(3)
x = 1
f = lambda y, x=x: x + y
f(2)
x = 5
f(7)
funcs = [lambda x, n=n: x+n for n in range(5)]
for f in funcs:
    print(f(0))

# Making an N-Argument Callable Work As a Callable with Fewer Arguments
def spam(a, b, c, d):
    print(a, b, c, d)

from functools import partial
s1 = partial(spam, 1) # a = 1
s1(4, 5, 6)
s2 = partial(spam, d=42)
s2(1, 2, 3)
s3 = partial(spam, 1, 2, d=42) # a = 1, b = 2, d = 42
s3(3)

points = [ (1, 2), (3, 4), (5, 6), (7, 8) ]
import math
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)
pt = (4, 3)
distance(pt, points[0])
points.sort(key=partial(distance, pt))
points

# Replacing Single Method Classes with Functions
from urllib.request import urlopen
class UrlTemplate:
    def __init__(self, template):
        self.template = template
    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))
# Example use. Download stock data from yahoo
yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))

def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

# Carrying Extra State with Callback Functions
def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)
    # Invoke the callback with the result
    callback(result)  
def print_result(result):
    print('Got:', result)
def add(x, y):
    return x + y
apply_async(add, (2, 3), callback=print_result)
apply_async(add, ('hello', 'world'), callback=print_result)

class ResultHandler:
    def __init__(self):
        self.sequence = 0
    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))
r = ResultHandler()
apply_async(add, (2, 3), callback=r.handler)
apply_async(add, ('hello', 'world'), callback=r.handler)

def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler
handler = make_handler()
apply_async(add, (2, 3), callback=handler)
apply_async(add, ('hello', 'world'), callback=handler)

def make_handler():
    # coroutine
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
handler = make_handler()  
next(handler) # Advance to the yield
apply_async(add, (2, 3), callback=handler.send)
apply_async(add, ('hello', 'world'), callback=handler.send)

# Inlining Callback Functions

# Accessing Variables Defined Inside a Closure
def sample():
    n = 0
    # Closure function
    def func():
        print('n =', n)
    # Accessor methods for n
    def get_n():
        return n
    def set_n(value):
        nonlocal n
        n = value
    # Attach as function attributes
    func.get_n = get_n
    func.set_n = set_n
    return func
f = sample()
f()
f.set_n(10)
f()
f.get_n()

# =============================================================================
# Classes and Objects
# =============================================================================

# Changing the String Representation of Instances
class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        # eval(repr(x)) == x
        return 'Pair({0.x}, {0.y})'.format(self)
    def __str__(self):
        return '({0.x}, {0.y})'.format(self)
p = Pair(3, 4)
p
str(p)
print(p)
print('p is {0!r}'.format(p)) # __repr__
print('p is {0}'.format(p)) # __str__
eval(repr(p)) 

# Customizing String Formatting
_formats = {
    'ymd' : '{d.year}-{d.month}-{d.day}',
    'mdy' : '{d.month}/{d.day}/{d.year}',
    'dmy' : '{d.day}/{d.month}/{d.year}'
    }
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)
d = Date(2012, 12, 21)
format(d)
format(d, 'mdy')
'The date is {:mdy}'.format(d)

# Making Objects Support the Context-Management
from socket import socket, AF_INET, SOCK_STREAM
class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.sock = None
    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        return self.sock
    def __exit__(self, exc_ty, exc_val, tb):
        # inputs: exeption type, value, traceback
        # garanteed to run no matter what
        self.sock.close()
        self.sock = None

from functools import partial
conn = LazyConnection(('www.python.org', 80))
# Connection closed
with conn as s:
    # conn.__enter__() executes: connection open
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    # conn.__exit__() executes: connection closed

class LazyConnection:
    # support nested 'with statements'
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.connections = []
    def __enter__(self):
        sock = socket(self.family, self.type)
        sock.connect(self.address)
        self.connections.append(sock)
        return sock
    def __exit__(self, exc_ty, exc_val, tb):
        self.connections.pop().close()
    
# Saving Memory When Creating a Large Number of Instances
class Date:
    # only for classes that serve as frequently used data structures
    # slots uses a much more compact internal representation for instances
    __slots__ = ['year', 'month', 'day'] # an optimization tool
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
d = Date(2019, 12, 30)

# Encapsulating Names in a Class
class A:
    def __init__(self):
        self._internal = 0 # An internal attribute
        self.public = 1 # A public attribute
    def public_method(self):
        '''
        A public method
        '''
        pass
    def _internal_method(self):
        pass
class B:
    def __init__(self):
        self.__private = 0 # renamed to _B__private
    def __private_method(self):
        pass
    def public_method(self):
        self.__private_method() # renamed to _B__private_method
class C(B):
    def __init__(self):
        super().__init__()
        # _C__private
        self.__private = 1 # Does not override B.__private        
    def __private_method(self):
        # _C__private_method
        # Does not override B.__private_method()
        pass
lambda_ = 2.0 # Trailing _ to avoid clash with lambda keyword

# Creating Managed Attributes
class Person:
    def __init__(self, first_name):
        self.first_name = first_name
        
    # Getter function
    @property
    def first_name(self):
        return self._first_name
    
    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value
        
    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")
        
a = Person('Guido')
a.first_name
a.first_name = 'Peter'
a.first_name
del a.first_name
a.first_name = 3
Person(3)

Person.first_name.fget
Person.first_name.fset
Person.first_name.fdel

class Person:
    def __init__(self, first_name):
        self.set_first_name(first_name)
    # Getter function
    def get_first_name(self):
        return self._first_name
    # Setter function
    def set_first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value
    # Deleter function (optional)
    def del_first_name(self):
        raise AttributeError("Can't delete attribute")
    # Make a property from existing get/set methods
    name = property(get_first_name, set_first_name, del_first_name)

a = Person('Guido')
a.get_first_name()
a.set_first_name('Peter')
a.get_first_name()
a.del_first_name()
a.set_first_name(3)
Person(3)

import math
class Circle:
    def __init__(self, radius):
        self.radius = radius
    @property
    def area(self):
        return math.pi * self.radius ** 2
    @property
    def perimeter(self):
        return 2 * math.pi * self.radius
c = Circle(4.0)
c.radius
c.area
c.perimeter

# Calling a Method on a Parent Class
class A:
    def spam(self):
        print('A.spam')
class B(A):
    def spam(self):
        print('B.spam')
        super().spam() # Call parent spam()

class A:
    def __init__(self):
        self.x = 0
class B(A):
    def __init__(self):
        super().__init__()
        self.y = 1

class Base:
    def __init__(self):
        print('Base.__init__')
class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')
class B(Base):
    def __init__(self):
        Base.__init__(self)
        print('B.__init__')
class C(A,B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        print('C.__init__')
c = C() # Base.__init__ called twice!

class Base:
    def __init__(self):
        print('Base.__init__')
class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init__')
class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')
class C(A, B):
    def __init__(self):
        super().__init__() # Only one call to super() here
        print('C.__init__')
c = C()
C.__mro__ # method resolution order

# Extending a Property in a Subclass

# Creating a New Kind of Class or Instance Attribute

# Using Lazily Computed Properties

















