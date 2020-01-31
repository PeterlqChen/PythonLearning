import this

# =============================================================================
# Item 1: Know Which Version of Python You’re Using
# =============================================================================

import sys
print(sys.version_info)
print(sys.version)

# =============================================================================
# Item 2: Follow the PEP 8 Style Guide
# =============================================================================

# =============================================================================
# Item 3: Know the Differences Between bytes, str, and unicode
# =============================================================================

# =============================================================================
# Item 4: Write Helper Functions Instead of Complex Expressions
# =============================================================================

# =============================================================================
# Item 5: Know How to Slice Sequences
# =============================================================================

# =============================================================================
# Item 22: Prefer Helper Classes Over Bookkeeping with Dictionaries and Tuples
# =============================================================================

class SimpleGradebook(object):
    
    def __init__(self):
        self._grades = {}
        
    def add_student(self, name):
        self._grades[name] = []
        
    def report_grade(self, name, score):
        self._grades[name].append(score)
        
    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)
book = SimpleGradebook()
book.add_student('Isaac Newton')
book.report_grade('Isaac Newton', 90)
print(book.average_grade('Isaac Newton'))

import collections
Grade = collections.namedtuple('Grade', ('score', 'weight'))

class Subject(object):
    def __init__(self):
        self._grades = []
    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))
    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight

class Student(object):
    def __init__(self):
        self._subjects = {}
    def subject(self, name):
        if name not in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]
    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count

class Gradebook(object):
    def __init__(self):
        self._students = {}
    def student(self, name):
        if name not in self._students:
            self._students[name] = Student()
        return self._students[name]

book = Gradebook()
albert = book.student('Albert Einstein')
math = albert.subject('Math')
math.report_grade(80, 0.10)
print(albert.average_grade())

# =============================================================================
# Item 23: Accept Functions for Simple Interfaces Instead of Classes
# =============================================================================

from collections import defaultdict
current = {'green': 12, 'blue': 3}
increments = [
        ('red', 5),
        ('blue', 17),
        ('orange', 9),
    ] 
def log_missing(): # good practice
    print('Key added')
    return 0
result = defaultdict(log_missing, current)
for key, amount in increments:
    result[key] += amount

def increment_with_report(current, increments): # less readable
    added_count = 0
    def missing():
        nonlocal added_count # Stateful closure
        added_count += 1
        return 0
    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount
    return result, added_count

result, count = increment_with_report(current, increments)

class CountMissing(object): # confusing
    def __init__(self):
        self.added = 0
    def missing(self):
        self.added += 1
        return 0
counter = CountMissing()
result = defaultdict(counter.missing, current)
for key, amount in increments:
    result[key] += amount
assert counter.added == 2

class BetterCountMissing(object): # good practice
    def __init__(self):
        self.added = 0
    def __call__(self):
        self.added += 1
        return 0
counter = BetterCountMissing()
counter()
assert callable(counter)
counter.added

counter = BetterCountMissing()
result = defaultdict(counter, current) # Relies on __call__
for key, amount in increments:
    result[key] += amount
assert counter.added == 2

# =============================================================================
# Item 24: Use @classmethod Polymorphism to Construct Objects Generically
# =============================================================================

import os
class InputData(object):
    def read(self):
        raise NotImplementedError

class PathInputData(InputData):
    def __init__(self, path):
        super().__init__()
        self.path = path
    def read(self):
        return open(self.path).read()

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

def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))

def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers

def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result

def mapreduce(data_dir): # not generic at all
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)

# a much better solution    
class GenericInputData(object):
    def read(self):
        raise NotImplementedError
    @classmethod
    def generate_inputs(cls, config):
        # config is a dict up to subclassed to interpret
        raise NotImplementedError

class PathInputData(GenericInputData):
    def __init__(self, path):
        super().__init__()
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
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers

class LineCountWorker(Worker):
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')
    def reduce(self, other):
        self.result += other.result

def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)

with TemporaryDirectory() as tmpdir:
    write_test_files(tmpdir)
    config = {'data_dir': tmpdir}
    result = mapreduce(LineCountWorker, PathInputData, config)

# =============================================================================
# Item 25: Initialize Parent Classes with super
# =============================================================================

class MyBaseClass(object):
    def __init__(self, value):
        self.value = value

class Explicit(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value * 2)

class Implicit(MyBaseClass):
    def __init__(self, value):
        super().__init__(value * 2) # always use super()
assert Explicit(10).value == Implicit(10).value

# =============================================================================
# Item 26: Use Multiple Inheritance Only for Mix-in Utility Classes
# =============================================================================

# simpler example
#https://riptutorial.com/python/example/15228/mixin

# =============================================================================
# Item 27: Prefer Public Attributes Over Private Ones
# =============================================================================

class MyObject(object):
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10
        self._hi = 7
    def get_private_field(self):
        return self.__private_field
foo = MyObject()
foo.public_field 
foo.__private_field # AttributeError:
foo._hi

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
        self.__private_field = 71
class MyChildObject(MyParentObject):
    def get_private_field(self):
        return self.__private_field
baz = MyChildObject()
baz.get_private_field() # AttributeError
baz._MyParentObject__private_field

"""
The only time to seriously consider using 
private attributes is when you’re worried about
naming conflicts with subclasses.
"""

class ApiClass(object):
    def __init__(self):
        self.__value = 5
    def get(self):
        return self.__value
class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello' # OK!
a = Child()
print(a.get(), 'and', a._value, 'are different')

# =============================================================================
# Item 28: Inherit from collections.abc for Custom Container Types
# =============================================================================

from collections.abc import Sequence
class BadType(Sequence):
    pass
foo = BadType()

# =============================================================================
# Item 29: Use Plain Attributes Instead of Get and Set Methods
# =============================================================================

class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        #self._voltage = 0
    @property
    def voltage(self):
        return self._voltage
    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms
r2 = VoltageResistance(1e3)
r2.voltage = 10

class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
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
BoundedResistance(-5)

class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
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
# Item 30: Consider @property Instead of Refactoring Attributes
# =============================================================================

class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0
    @property
    def quota(self):
        # Make incremental progress toward better data models by @property.
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
            self.quota_consumed += delta
    def __repr__(self):
        return ('Bucket(max_quota=%d, quota_consumed=%d)' %
                (self.max_quota, self.quota_consumed))

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
print(bucket)

# =============================================================================
# Item 31: Use Descriptors for Reusable @property Methods
# =============================================================================

class Homework(object):
    def __init__(self):
        #self._grade = 0
        ''
    @property
    def grade(self):
        return self._grade
    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._grade = value
galileo = Homework()
galileo.grade = 95
galileo._grade

class Exam(object):
    # too many properties
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

class Grade(object):
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

Exam.__dict__
exam = Exam()
exam.writing_grade = 40 # Exam.__dict__['writing_grade'].__set__(exam, 40)
print(exam.writing_grade) # print(Exam.__dict__['writing_grade'].__get__(exam, Exam))

first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
first_exam.writing_grade # wrong
second_exam.writing_grade

from weakref import WeakKeyDictionary
class Grade(object):
    '''
    Reuse the behavior and validation of @property methods by 
    defining your own descriptor classes.
    '''
    def __init__(self):
        '''
        Use WeakKeyDictionary to ensure that your descriptor 
        classes don’t cause memory leaks.
        '''
        self._values = WeakKeyDictionary() # self._values = {}
    def __get__(self, instance, instance_type):
        if instance is None: return self
        return self._values.get(instance, 0)
    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value
class Exam(object):
    # Class attributes
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()
first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
first_exam.writing_grade # wrong
second_exam.writing_grade

# =============================================================================
# Item 32: Use __getattr__, __getattribute__, __setattr__ for Lazy Attributes
# =============================================================================

class LazyDB(object):
    def __init__(self):
        self.exists = 5
    def __getattr__(self, name):
        '''
        called every time an attribute can’t be found 
        in an object’s instance dictionary.
        '''
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value
data = LazyDB()
print('Before:', data.__dict__)
print('foo: ', data.foo)
print('After: ', data.__dict__)
data.exists

class LoggingLazyDB(LazyDB):
    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        return super().__getattr__(name)
data = LoggingLazyDB()
data.__dict__
hasattr(data, 'foo')
print('exists:', data.exists)
print('foo: ', data.foo)
print('foo: ', data.foo)

class ValidatingDB(object):
    def __init__(self):
        self.exists = 5
    def __getattribute__(self, name):
        # called every time an attribute is accessed on an object
        print('Called __getattribute__(%s)' % name)
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value
    def __setattr__(self, name, value):
        super().__setattr__(name, value) # avoid recursion
data = ValidatingDB()
print('exists:', data.exists)
print('foo: ', data.foo)
print('foo: ', data.foo)

class DictionaryDB(object):
    def __init__(self, data):
        self._data = data
    def __getattribute__(self, name):
        # self._data will cause recursion
        data_dict = super().__getattribute__('_data')
        return data_dict[name]

# =============================================================================
# Item 33: Validate Subclasses with Metaclasses
# =============================================================================

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        print((meta, name, bases, class_dict))
        return type.__new__(meta, name, bases, class_dict)
class MyClass(object, metaclass=Meta):
    stuff = 123
    def foo(self):
        pass

class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        print((meta, name, bases, class_dict))
        # Don’t validate the abstract Polygon class
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

print('Before class')
class Line(Polygon):
    print('Before sides')
    sides = 1
    print('After sides')
print('After class')

# =============================================================================
# Item 34: Register Class Existence with Metaclasses
# =============================================================================

import json
class Serializable(object):
    def __init__(self, *args):
        self.args = args
    def serialize(self):
        return json.dumps({'args': self.args})
s1 = Serializable(1, 2, 3)
s1.args
s1.serialize()
class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)
point = Point2D(5, 3)
point.serialize()

class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])
class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)
point = BetterPoint2D(5, 3)
data = point.serialize()
after = BetterPoint2D.deserialize(data)

class BetterSerializable(object):
    def __init__(self, *args):
        self.args = args
    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
        })
       
registry = {}
def register_class(target_class):
    registry[target_class.__name__] = target_class
def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])
class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
register_class(EvenBetterPoint2D)
point = EvenBetterPoint2D(5, 3)
data = point.serialize()
after = deserialize(data)

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        print(cls)
        register_class(cls)
        return cls
class RegisteredSerializable(BetterSerializable,
                             metaclass=Meta):
    pass
class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z
v3 = Vector3D(10, -7, 3)
data = v3.serialize()
deserialize(data)

# =============================================================================
# Item 35: Annotate Class Attributes with Metaclasses
# =============================================================================


# =============================================================================
# Item 49: Write Docstrings for Every Function, Class, and Module
# =============================================================================

def palindrome(word):
    """Return True if the given word is a palindrome."""
    return word == word[::-1]
palindrome.__doc__
help(palindrome)

# =============================================================================
# Item 56: Test Everything with unittest
# =============================================================================




globals()

















































