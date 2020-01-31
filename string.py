
import os

# =============================================================================
# from the https://docs.python.org/3/tutorial/inputoutput.html
# =============================================================================

# formated string literals

year = 2016
event = 'Referendum'
f'Results of the {year} {event}'
F'Results of the {year} {event}'

import math
f'The value of pi is approximately {math.pi:.3f}.'

table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 7678}
for name, phone in table.items():
    print(f'{name:10} ==> {phone:10d}')

animals = 'eels'
# '!a' applies ascii(), '!s' applies str(), and '!r' applies repr()
f'My hovercraft is full of {animals!r}.'

# string format method

'{1} and {0}'.format('spam', 'eggs')
print('This {food} is {adjective}.'.format(food='spam', adjective='absolutely horrible'))
print('The story of {0}, {1}, and {other}.'.format('Bill', 'Manfred', other='Georg'))
yes_votes = 42_572_654
no_votes = 43_132_495
percentage = yes_votes / (yes_votes + no_votes)
'{:-9} YES votes  {:2.2%}'.format(yes_votes, percentage)

table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 8637678}
print('Jack: {0[Jack]:d}; Sjoerd: {0[Sjoerd]:d}; '
              'Dcab: {0[Dcab]:d}'.format(table))
print('Jack: {Jack:d}; Sjoerd: {Sjoerd:d}; Dcab: {Dcab:d}'.format(**table))

# manual string formatting

s = 'Hello, world.'
str(s)
repr(s)
repr(3)

print('a', 'b', end='_')
for x in range(1, 11):
    print(repr(x).rjust(2), repr(x*x).rjust(3), end=' ')
    # Note use of 'end' on previous line
    print(repr(x*x*x).rjust(4))
    
'-3.14'.zfill(7)
'The value of pi is approximately %5.3f.' % math.pi

# Using with is also much shorter than writing equivalent try-finally blocks
with open('workfile') as f:
    read_data = f.read()


# =============================================================================
# E.P.1 i3: Know the Differences Between bytes, str, and unicode
# =============================================================================

"""
it’s important to do encoding and decoding of Unicode at the furthest boundary 
of your interfaces. The core of your program should use Unicode character types
and should not assume anything about character encodings.
"""

# bytes and str instances can’t be used together with operators
help(bytes)
b'abc'
bytes([97, 98, 99])
b'' == '' # False, bytes and str instances are never equivalent

good_utf = '好的'.encode('utf-8') # to bytes
good_utf.decode('utf-8') # to str

def to_str(bytes_or_str):
    """
    Instances of bytes contain raw 8-bit values. 
    Instances of str contain Unicode characters.
    """
    
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value # Instance of str

to_str(b'abc')
to_str('abc')

def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value # Instance of bytes

to_bytes('abc')

with open('/tmp/random.bin', 'wb') as f: # must open in binary mode
    f.write(os.urandom(10)) # encoding='utf-8'















































