
from collections import namedtuple, defaultdict
from threading import Thread
import os
import json
from datetime import datetime, timedelta

# scopes
def scope_test():
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print("After local assignment:", spam)
    do_nonlocal()
    print("After nonlocal assignment:", spam)
    do_global()
    print("After global assignment:", spam)

scope_test()
print("In global scope:", spam)

class MyClass:
    """A simple example class"""
    """test"""
    i = 12345 # class variable shared by all instances

    def f(self):
        return 'hello world'
    
MyClass.i 
MyClass.i = 0
MyClass.i
myobj = MyClass()   
myobj
MyClass.f(myobj) # equivalent to myobj.f()
MyClass.__doc__

myobj.counter = 1 # adding new attribute
MyClass.__dict__
myobj.__dict__
MyClass.i
myobj.i
myobj.i = 3
MyClass.i
myobj.__class__


# only serves to confuse the reader
# Function defined outside the class
def f1(self, x, y):
    return min(x, x + y)
class C:
    f = f1
    def g(self):
        return 'hello world'
    h = g
C.g == C.h

isinstance(3, int)
issubclass(bool, int)
issubclass(float, int)


class Mapping:
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable)

    def update(self, iterable):
        for item in iterable:
            self.items_list.append(item)

    __update = update   # private copy of original update() method

class MappingSubclass(Mapping):

    def update(self, keys, values):
        # provides new signature for update()
        # but does not break __init__()
        for item in zip(keys, values):
            self.items_list.append(item)

s = 'abc'
it = iter(s)
it
next(it)

class Reverse:
    """Iterator for looping over a sequence backwards."""
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]
rev = Reverse('spam')
iter(rev)
for char in rev:
    print(char)

# generator, more concise & automated
def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index]

# generator expressions, more memory friendly
sum(i*i for i in range(10))     
data = 'golf'
list(data[i] for i in range(len(data)-1, -1, -1))

# =============================================================================
# E.P.1 i22: Prefer Helper Classes Over Bookkeeping with Dictionaries and Tuples
# =============================================================================

class SimpleGradeBook(object):    
    def __init__(self):
        self._grades = {}   
    
    def add_student(self, name):
        self._grades[name] = []
        
    def report_grade(self, name, grade):
        self._grades[name].append(grade)
        
    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades)/len(grades)

class BySubjectGradeBook(object):    
    def __init__(self):
        self._grades = {}   
    
    def add_student(self, name):
        # nexted dict is a sign of using hierachy of classes
        self._grades[name] = {} 
        
    def report_grade(self, name, subject, grade):
        grades = self._grades[name]
        grade_list = grades.setdefault(subject, [])
        grade_list.append(grade)
        
    def average_grade(self, name):
        # still manageable
        grades = self._grades[name]
        total_grade, cnt_grade = 0, 0
        for grade_list in grades.values():
            total_grade += sum(grade_list)
            cnt_grade += len(grade_list)
        return total_grade/cnt_grade


class WeightedGradeBook(object):
    # better to switch to hierachy of classes
    def __init__(self):
        self._grades = {}   
    
    def add_student(self, name):
        self._grades[name] = {}
        
    def report_grade(self, name, subject, score, weight):
        # arg list becomes longer
        grades = self._grades[name]
        grade_list = grades.setdefault(subject, [])
        grade_list.append((score, weight))
        
    def average_grade(self, name):
        # becomes difficult to read
        grades = self._grades[name]
        total_grade, cnt_grade = 0, 0
        for grade_by_sub in grades.values():
            sub_total, sub_count = 0, 0
            for score, weight in grade_by_sub:
                sub_total += score*weight
                sub_count += weight
            total_grade += sub_total
            cnt_grade += sub_count
        return total_grade/cnt_grade

# construct class from the bottom up
grades = []
grades.append((95, 0.45, 'Great job')) # avoid long tuples

# easily define tiny, immutable data classes using namedtuple
# start with namedtuple before classes
# but can’t specify default argument values
Grade = namedtuple('Grade', ('score', 'weight'))
type(Grade)
grade = Grade(score=99, weight=0.3)
grade
type(grade)
grade.score
grade.weight
grade[0]
grade[1]

class Subject(object):
    def __init__(self):
        self._grades = []
    
    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))
    
    def average_grade(self):
        total_grade, total_weight = 0, 0
        for grade in self._grades:
            total_grade += grade.score*grade.weight
            total_weight += grade.weight
        return total_grade/total_weight

class Student(object):
    def __init__(self):
        self._subject = {}
    
    def subject(self, name):
        if name not in self._subject:
            self._subject[name] = Subject()
        return self._subject[name]
    
    def average_grade(self):
        total, count = 0, 0
        for subject in self._subject.values():
            total += subject.average_grade()
            count += 1
        return total/count

class Gradebook(object):
    def __init__(self):
        self._student = {}
    
    def student(self, name):
        if name not in self._student:
            self._student[name] = Student()
        return self._student[name]

book = Gradebook()
albert = book.student('Albert Einstein')
math = albert.subject('Math')
math.report_grade(80, 0.10)
albert.average_grade()

# =============================================================================
# E.P.1 i23: Accept Functions for Simple Interfaces Instead of Classes
# =============================================================================

names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key=lambda x: len(x))

def log_missing():
    print('Key added')
    return 0

current = {'green': 12, 'blue': 3}
result = defaultdict(log_missing, current)
result['purple']
result
result['yellow'] = 10
result
result['brown'] += 3
result

class CountMissing(object):
    # look mystery until we see defaultdict below
    def __init__(self):
        self.count = 0
    
    def missing(self):
        self.count += 1
        return 0
    
counter = CountMissing()
result = defaultdict(counter.missing, current)
counter.count
callable(counter)

class BetterCountMissing(object):
    def __init__(self):
        self.count = 0
    
    def __call__(self):
        # indicates the object will be used as an API hook
        # strong hint that the goal is to act as a stateful closure
        self.count += 1
        return 0

counter = BetterCountMissing()
result = defaultdict(counter, current)
counter.count
callable(counter)

# =============================================================================
# E.P.1 i24: Use @classmethod Polymorphism to Construct Objects Generically
# =============================================================================

class InputData(object):
    def read(self):
        raise NotImplementedError

class PathInputData(InputData):
    def __init__(self, path):
        super.__init__()
        self.path = path
    
    def read(self):
        open(self.path).read()

class Worker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None
        
    def map(self):
        raise NotImplementedError
        
    def reduce(self, other):
        raise NotImplementedError

class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')
    
    def reduce(self, other):
        self.result += other.result

# simplest approach for building the objects and orchestrating the MapReduce
def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))

def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers

def execute(workers):
    # this function is generic, which is good
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result

def mapreduce(data_dir):
    # not generic at all
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)

# a more generic approach
class GenericInputData(object):
    def read(self):
        raise NotImplementedError
    
    # define alternative constructors
    @classmethod
    def generate_inputs(cls, config):
        # a set of configuration parameters
        raise NotImplementedError

class PathInputData(GenericInputData):
    def __init__(self, path):
        super.__init__()
        self.path = path
    
    def read(self):
        return open(self.path).read()
    
    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))

class GenericWorker(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None
        
    def map(self):
        raise NotImplementedError
        
    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        # class polymorphism
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers

class LineCountWorker(GenericWorker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')
    
    def reduce(self, other):
        self.result += other.result

def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)

# =============================================================================
# E.P.1 i25: Initialize Parent Classes with super
# =============================================================================

class MyBaseClass(object):
    def __init__(self, value):
        self.value = value

class TimesFiveCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value *= 5

class PlusTwoCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value)
        self.value += 2

class GoodWay(TimesFiveCorrect, PlusTwoCorrect):
    def __init__(self, value):
        # only call __init__ once, order based on argument list now
        super().__init__(value)

GoodWay.mro() # __init__ functions are called in reverse order
"""
[__main__.GoodWay,
 __main__.TimesFiveCorrect,
 __main__.PlusTwoCorrect,
 __main__.MyBaseClass,
 object]
"""

foo = GoodWay(5)
foo.value

# =============================================================================
# E.P.1 i26: Use Multiple Inheritance Only for Mix-in Utility Classes
# =============================================================================

"""
to convert a Python object from its in-memory representation to 
a dictionary that's ready for serialization
"""

class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output
    
    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict() # value can be of inherited class of self
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value

class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

tree = BinaryTree(10,
    left=BinaryTree(7, right=BinaryTree(9)),
    right=BinaryTree(13, left=BinaryTree(11)))

tree.value
tree.right.left.value
tree.__dict__
#tree.__class__.__dict__
#BinaryTree.__dict__

tree.to_dict()

class BinaryTreeWithParent(BinaryTree):
    def __init__(self, value, left=None, 
                 right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent # incurs infinite loop for to_dict
        
    # Use pluggable behaviors at the instance level
    def _traverse(self, key, value):
        if (isinstance(value, BinaryTreeWithParent) and key == 'parent'):
            return value.value # Prevent cycles
        else:
            return super()._traverse(key, value)

root = BinaryTreeWithParent(10)
root.left = BinaryTreeWithParent(7, parent=root)
root.left.right = BinaryTreeWithParent(9, parent=root.left)
root.to_dict()

class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent
        
my_tree = NamedSubTree('foobar', root.left.right)
my_tree.to_dict() # No infinite loop

"""
want a mix-in that provides generic JSON serialization for any class
"""
class JsonMixin(object):    
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)
    
    def to_json(self):
        return json.dumps(self.to_dict())

# Compose mix-ins to create complex functionality from simple behaviors
class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [
                Machine(**kwargs) for kwargs in machines]

class Switch(ToDictMixin, JsonMixin):
    def __init__(self, **kwarg):
        self.ports = kwarg['ports']
        self.speed = kwarg['speed']

class Machine(ToDictMixin, JsonMixin):
    def __init__(self, **kwarg):
        self.cores = kwarg['cores']
        self.ram = kwarg['ram']
        self.disk = kwarg['disk']

serialized = """{
    "switch": {"ports": 5, "speed": 1e9},
    "machines": [
        {"cores": 8, "ram": 32e9, "disk": 5e12},
        {"cores": 4, "ram": 16e9, "disk": 1e12},
        {"cores": 2, "ram": 4e9, "disk": 500e9}
    ]
}"""
deserialized = DatacenterRack.from_json(serialized)
roundtrip = deserialized.to_json()
assert json.loads(serialized) == json.loads(roundtrip)

# =============================================================================
# E.P.1 i27: Prefer Public Attributes Over Private Ones
# =============================================================================

class MyObject(object):
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10
        
    def get_private_field(self):
        return self.__private_field

foo = MyObject()
foo.public_field 
foo.__private_field # exception
foo.get_private_field()
foo.__dict__

class MyOtherObject(object):
    def __init__(self):
        self.__private_field = 71
        
    @classmethod
    def get_private_field_of_instance(cls, instance):
        return instance.__private_field

bar = MyOtherObject()
MyOtherObject.get_private_field_of_instance(bar) 

class MyParentObject(object):
    def __init__(self):
        self.__private_field = 71 # _MyParentObject__private_field

class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field 

baz = MyChildObject()
baz.get_private_field() # exception
baz.__dict__

# Use documentation of protected fields to guide subclasses
class MyClass(object):
    def __init__(self, value):
        # This stores the user-supplied value for the object.
        # It should be coercible to a string. Once assigned for
        # the object it should be treated as immutable.
        self._value = value

# Only consider using private attributes to avoid naming conflicts 
# with subclasses that are out of your control
class ApiClass(object):
    def __init__(self):
        self._value = 5 
    def get(self):
        return self._value
    
class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' # conflicts!

a = Child()
a.get()
a._value

class ApiClass(object):
    def __init__(self):
        self.__value = 5 # to avoid name conflicts
    def get(self):
        return self.__value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' # OK!
        
a = Child()
a.get()
a._value

# =============================================================================
# E.P.1 i28: Inherit from collections.abc for Custom Container Types
# =============================================================================

""" Inherit directly from Python’s container types (like list or dict) 
for simple use cases.
"""
class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)
        
    def frequency(self):
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1
        return counts

list([3, 4, 5])
foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
foo.frequency()
len(foo)
foo.pop()
foo.frequency()
foo[2]
foo.count('a')

bar = [0, 1, 2]
bar[1]
bar.__getitem__(1)

# to provide sequence semantics (like list or tuple) for a binary tree class
class BinaryNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

# defining your own container types is much harder than it looks
class IndexableNode(BinaryNode):
    def _search(self, count, index):
        # …
        # Returns (found, count)
        pass
        
    def __getitem__(self, index):
        found, _ = self._search(0, index)
        if not found:
            raise IndexError('Index out of range')
        return found.value
    
class SequenceNode(IndexableNode):
    def __len__(self):
        _, count = self._search(0, None)
        return count
    
    # Also missing are the count and index methods, etc.

"""
the module defines a set of abstract base classes that provide all 
of the typical methods for each container type
"""
from collections.abc import Sequence

class BadType(Sequence):
    pass

foo = BadType() # exception

"""
When you do implement all of the methods required by an abstract base class, 
it will provide all of the additional methods like index and count for free
"""
class BetterNode(SequenceNode, Sequence):
    pass


# =============================================================================
# E.P.1 i29: Use Plain Attributes Instead of Get and Set Methods
# =============================================================================

# avoid set and get methods
class OldResistor(object):
    def __init__(self, ohms):
        self._ohms = ohms
    
    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms

r0 = OldResistor(50e3)
r0.set_ohms(r0.get_ohms() + 5e3) # clumsy

# prefer simple public attributes
class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
r1.ohms += 5e3 # much clearer

class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0
        
    @property
    def voltage(self):
        return self._voltage
    
    # mean to be easy and fast
    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

r2 = VoltageResistance(1e3)
r2.current
r2.voltage = 10
r2.current

class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms) # self.ohms = ohms
        
    @property
    def ohms(self):
        return self._ohms
    
    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms

r3 = BoundedResistance(1e3)
r3.ohms = 0
r3._ohms
type(r3.ohms)
BoundedResistance(-5) # self.ohms in Resistor.__init__ triggers ohms.setter
r3._ohms
r3._ohms = -1
r3.ohms
r3.ohms *= 2

hasattr(r3, '_ohms')

class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms) # self.ohms = ohms

    @property
    def ohms(self):
        return self._ohms
    
    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribute")
        self._ohms = ohms

r4 = FixedResistance(1e3)
r4.ohms = 2e3

# =============================================================================
# E.P.1 i30: Consider @property Instead of Refactoring Attributes
# =============================================================================

class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0
    
    def __repr__(self):
        return 'Bucket(quota=%d)' % self.quota

def fill(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount

def deduct(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True

bucket = Bucket(60)
fill(bucket, 100)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')

class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0
        
    def __repr__(self):
        return ('Bucket(max_quota=%d, quota_consumed=%d)' %
                (self.max_quota, self.quota_consumed))
        
    # to give existing instance attributes new functionality
    # make incremental progress toward better data models
    @property
    def quota(self):
        return self.max_quota - self.quota_consumed
    
    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # Quota being reset for a new period
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # Quota being filled for the new period
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            # Quota being consumed during the period
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed = delta

bucket = Bucket(60)
print('Initial', bucket)
fill(bucket, 100)
print('Filled', bucket)
if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print('Now', bucket)
if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print('Still', bucket)

fill(bucket, 100)
deduct(bucket, 10)
bucket

"""
Consider refactoring a class and all call sites when 
@property is used too heavily.
"""

# =============================================================================
# E.P.1 i31: Use Descriptors for Reusable @property Methods
# =============================================================================

class Homework(object):
    def __init__(self):
        self._grade = 0
        
    @property
    def grade(self):
        return self._grade
    
    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._grade = value

class Exam(object):
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0
        
    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
    
    @property
    def writing_grade(self):
        return self._writing_grade
    
    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value
    
    @property
    def math_grade(self):
        return self._math_grade
    
    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value

# better approach with descriptor class, less repetition
class Grade(object):
    """
    reuse the behavior and validation of @property methods by 
    defining your own descriptor class
    """
    def __init__(self):
        self._value = 0
    
    def __get__(self, instance, instance_type):
        return self._value
    
    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value = value

class Exam(object):
    # Class attributes
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()
    
#    def __init__(self):
#        self.math_grade = Grade()
#        self.writing_grade = Grade()
#        self.science_grade = Grade()

exam = Exam()
exam.writing_grade = 40 # Exam.__dict__['writing_grade'].__set__(exam, 40)
exam.writing_grade # Exam.__dict__['writing_grade'].__get__(exam, Exam)

first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
first_exam.writing_grade # incorrect
second_exam.writing_grade

# correct version
from weakref import WeakKeyDictionary
class Grade(object):
    def __init__(self):
        """causes instances to never have their reference count go to zero, 
        preventing cleanup by the garbage collector, causes memory leaks
        """
        #self._values = {}
        
        """
        remove Exam instances from its set of keys when the runtime knows it’s 
        holding the instance’s last remaining reference in the program
        """
        self._values = WeakKeyDictionary()
   
    def __get__(self, instance, instance_type):
        if instance is None: return self
        return self._values.get(instance, 0)
   
    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value
    
first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
first_exam.writing_grade
second_exam.writing_grade

# =============================================================================
# E.P.1 i32: Use __getattr__, __getattribute__, and __setattr__ for Lazy Attributes
# =============================================================================

class LazyDB(object):
    def __init__(self):
        self.exists = 5
    
    def __getattr__(self, name):
        #print('within __getattr__')
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value

LazyDB.__dict__
data = LazyDB()
data.__dict__
data.foo
data.__dict__
data.foo

class LoggingLazyDB(LazyDB):
    def __getattr__(self, name):
        # called once when accessing missing attribute
        print('Called __getattr__(%s)' % name)
        return super().__getattr__(name)

class ValidatingDB(object):
    def __init__(self):
        self.exists = 5
  
    def __getattribute__(self, name):
        # called every time
        print('Called __getattribute__(%s)' % name)
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value

data = ValidatingDB()
data.exists
data.foo
hasattr(data, 'foo')

class DictionaryDB(object):
    def __init__(self, data):
        self._data = data
    def __getattribute__(self, name):
        # Avoid infinite recursion by using super()
        data_dict = super().__getattribute__('_data')
        return data_dict[name]

# =============================================================================
# E.P.1 i33: Validate Subclasses with Metaclasses
# =============================================================================

type(object)
type(type)

# create a class Apple
Apple = type.__new__(type, 'Apple', (object,), {'is_fruit': True})
apple = Apple()
apple.__dict__
Apple.__dict__

class Meta(type):
    """
    A metaclass is defined by inheriting from type.
    """
    def __new__(meta, name, bases, class_dict):
        """
        you can modify the class information before the
        type is actually constructed.
        run after the associated class statement's body has been processed.
        inputs:
            meta: metaclass
            name: the name of the class
            bases: parent classes it inherits from
            class_dict: all class attributes defined in the class's body
        """
        print((meta, name, bases, class_dict))
        return type.__new__(meta, name, bases, class_dict)

Meta.__dict__

class MyClass(object, metaclass=Meta):
    stuff = 123
    def foo(self):
        pass

class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        """
        Use metaclasses to ensure that subclasses are well formed at the time 
        they are defined, before objects of their type are constructed
        """
        print((meta, name, bases, class_dict))
        # Don't validate the abstract Polygon class
        if bases != (object,):
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(object, metaclass=ValidatePolygon):
    sides = None # Specified by subclasses
    
    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Triangle(Polygon):
    sides = 3

Triangle.interior_angles()

print('Before class')
class Line(Polygon):
    print('Before sides')
    sides = 1
    print('After sides')
print('After class')

# =============================================================================
# E.P.1 i34: Register Class Existence with Metaclasses
# =============================================================================

"""
to implement your own serialized representation of a Python
object using JSON
"""

class Serializable(object):
    def __init__(self, *args):
        self.args = args
        
    def serialize(self):
        return json.dumps({'args': self.args})

class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])

class Point2D(Deserializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
    
    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)

point = Point2D(5, 3)
point
type(point.serialize())
serialized_data = point.serialize()
serialized_data
deserialized_point = Point2D.deserialize(serialized_data)
deserialized_point

"""
Ideally, you’d have a large number of classes serializing to JSON and 
one common function that could deserialize any of them back to a 
corresponding Python object
"""

class BetterSerializable(object):
    def __init__(self, *args):
        self.args = args
    
    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
        })
    
    def __repr__(self):
        pass

# class registration is a helpful pattern for building modular Python programs
registry = {}
def register_class(target_class):
    registry[target_class.__name__] = target_class
    
def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])

class Point2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
    
    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)

register_class(Point2D)
point = Point2D(5, 3)
point
type(point.serialize())
serialized_data = point.serialize()
serialized_data
deserialized_point = deserialize(serialized_data)
deserialized_point

# even better 
class Meta(type):
    """
    run registration code automatically
    """
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls

class RegisteredSerializable(BetterSerializable, metaclass=Meta):
    pass

class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z
    
    def __repr__(self):
        return 'Vector3D(%d, %d, %d)' % (self.x, self.y, self.z)

v3 = Vector3D(5, 3, -7)
type(v3.serialize())
serialized_data = v3.serialize()
serialized_data
deserialized_v3 = deserialize(serialized_data)
deserialized_v3

# =============================================================================
# E.P.1 i35: Annotate Class Attributes with Metaclasses
# =============================================================================

"""
to define a new class that represents a row in your customer database.
need a corresponding property on the class for each column.
"""

class Field(object):
    # descriptor
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name
  
    def __get__(self, instance, instance_type):
        if instance is None: return self
        return getattr(instance, self.internal_name, '')
  
    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

class Customer(object):
    # represent a row
    first_name = Field('first_name') # a bit redundant
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')

foo = Customer()
foo.first_name
foo.__dict__
foo.first_name = 'Euclid'
foo.first_name
foo.__dict__

foo2 = Customer()
foo2.first_name = 'Peter'
foo2.__dict__

# better approach with metaclass

class Meta(type):
    """
    Metaclasses enable you to modify a class’s attributes before 
    the class is fully defined.
    """
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        return type.__new__(meta, name, bases, class_dict)

class DatabaseRow(object, metaclass=Meta):
    """
    All classes representing database rows should inherit from this class 
    to ensure that they use the metaclass
    """
    pass

class Field(object):
    # descriptor
    def __init__(self):
        self.name = None
        self.internal_name = None
  
    def __get__(self, instance, instance_type):
        if instance is None: return self
        return getattr(instance, self.internal_name, '')
  
    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

""" 
Descriptors and metaclasses make a powerful combination for 
declarative behavior and runtime introspection.
can avoid both memory leaks and the weakref module by using 
metaclasses along with descriptors.
"""
class BetterCustomer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()

foo = BetterCustomer()
foo.first_name
foo.__dict__
foo.first_name = 'Euler'
foo.first_name
foo.__dict__

















































































































