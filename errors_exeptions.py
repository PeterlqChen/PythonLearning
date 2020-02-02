
import sys
import json

# =============================================================================
# https://docs.python.org/3/library/exceptions.html#bltin-exceptions
# =============================================================================


10 * (1/0) # ZeroDivisionError
4 + spam*3 # NameError
'2' + 2 # TypeError

while True:
    try:
        x = int(input("Please enter a number: "))
        break
    except ValueError as err:
        print("Oops!  That was no valid number.  Try again...")
        print(err)
    except (RuntimeError, TypeError, NameError):
        pass
x

class B(Exception):
    pass
class C(B):
    pass
class D(C):
    pass
for cls in [B, C, D]:
    try:
        raise cls()
    except D:
        print("D")
    except C:
        print("C")
    except B:
        print("B")

import sys
try:
    f = open('myfile.txt')
    s = f.readline()
    i = int(s.strip())
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError:
    print("Could not convert data to an integer.")
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

for arg in sys.argv[1:]:
    try:
        f = open(arg, 'r')
    except OSError:
        print('cannot open', arg)
    else: # get executed if no exeption got raised
        print(arg, 'has', len(f.readlines()), 'lines')
        f.close()

try:
    # The presence and type of the argument depend on the exception type
    raise Exception('spam', 'eggs')
except Exception as inst:
    print(type(inst))    # the exception instance
    print(inst.args)     # arguments stored in .args
    print(inst)          # __str__ allows args to be printed directly

def this_fails():
    x = 1/0
try:
    this_fails()
except ZeroDivisionError as err:
    print('Handling run-time error:', err)

raise NameError('HiThere')
raise NameError
raise NameError()

try:
    raise NameError('HiThere')
except NameError:
    print('An exception flew by!')
    raise # don't intend to handle it

"""
 When creating a module that can raise several distinct errors, 
 a common practice is to create a base class for exceptions defined by that module, 
 and subclass that to create specific exception classes for different error conditions:
"""

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class TransitionError(Error):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        previous -- state at beginning of transition
        next -- attempted new state
        message -- explanation of why the specific transition is not allowed
    """

    def __init__(self, previous, next, message):
        self.previous = previous
        self.next = next
        self.message = message

try:
    raise KeyboardInterrupt
except KeyboardInterrupt as err:
    print('KeyboardInterrupt!')
    print(err)
    raise err
finally:
    print('Goodbye, world!')

def bool_return():
    try:
        return True
    finally:
        return False
bool_return()

# http://docs.python.org/3/library/exceptions.html#bltin-exceptions

# =============================================================================
# E.P.1 i13: Take Advantage of Each Block in try/except/else/finally
# =============================================================================

# Use try/finally when you want exceptions to propagate up, 
# but you also want to run cleanup code
handle = open('/tmp/random_data.txt') # May raise IOError, must be before try
try:
    data = handle.read() # May raise UnicodeDecodeError
finally:
    handle.close() # Always runs after try:

# The else block minimizes the amount of code in try blocks and visually
# distinguish the success case from the try/except blocks.

def load_json_key(data, key):
    try:
        result_dict = json.loads(data) # May raise ValueError
    except ValueError as e:
        raise KeyError from e
    else:
        return result_dict[key] # May raise KeyError

UNDEFINED = object()
def divide_json(path):
    handle = open(path, 'r+') # May raise IOError
    try:
        data = handle.read() # May raise UnicodeDecodeError
        op = json.loads(data) # May raise ValueError
        value = (
            op['numerator'] /
            op['denominator']) # May raise ZeroDivisionError
    except ZeroDivisionError as e:
        return UNDEFINED
    else:
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)
        handle.write(result) # May raise IOError
        return value
    finally:
        handle.close() # Always runs

# =============================================================================
# E.P.1 i43: Consider contextlib and with Statements for Reusable try/finally Behavior
# =============================================================================

"""
A simple example where with-statement is equivalent to try-finally block:
    
lock = Lock()
with lock:
    print('Lock is held')

>>>

lock.acquire()
try:
    print('Lock is held')
finally:
    lock.release()
"""

# to make your objects and functions capable of use in with statements
import contextlib
from contextlib import contextmanager

import logging

def my_function():
    logging.debug('Some debug data')
    logging.error('Error log here')
    logging.debug('More debug data')

my_function() # the default log level for my program is WARNING

@contextmanager
def debug_logging(level):
    """
    for the with statement
    """
    logger = logging.getLogger()
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        """
        a coroutine related technique
        Any exceptions that happen in the with block will be re-raised 
        by the yield expression for you to catch in the helper function
        """
        yield
    finally:
        logger.setLevel(old_level)

help(debug_logging)

with debug_logging(logging.DEBUG):
    my_function()
my_function()

def my_function():
    logging.debug('Some debug data')
    logging.error('Error log here')
    logging.debug('More debug data')

@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)

with log_level(logging.DEBUG, 'my-log') as logger:
    logger.debug('This is my message!')
    logging.debug('This will not print')



















































