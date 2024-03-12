from unittest.mock import MagicMock
import inspect

class ProductionClass():
    def __init__(self) -> None:
        pass
    def method(self) -> None:
        print('Eureka~!')

thing = ProductionClass()
# MagicMock sits in for the method 'method' of the class 'ProductionClass'
# The MagicMock object is a mock object that can be used to replace the method 'method' of the class 'ProductionClass'
# The MagicMock object will take all the calls to 'method' and return 3
thing.method = MagicMock(return_value=3)
# It does not matter which arguments are passed to 'method' of the class 'ProductionClass'
# it will always return 3 as it is configured now.
thing.method(3, 4, 5, key='value')

# side_effect can be used to raise an exception or to perform the so-called side effect
from unittest.mock import Mock
mock = Mock(side_effect=KeyError('foo'))
try:
    mock()
except KeyError as e:
    print(f"KeyError in file {__file__}:")

values = {'a': 1, 'b': 2, 'c': 3}
def side_effect(arg):
    return values[arg]
# Change the side_effect of the mock object I can control the returned value
# of the mock object.
mock.side_effect = side_effect
print(mock('a'), mock('b'), mock('c'))
print(mock('b'))

mock.side_effect = [5, 4, 3, 2, 1]
print(mock(), mock(), mock(), mock(), mock('whatever'))

# Using the spec parameter of the MagicMock object I can create a mock object
# that has the same attributes as the class 'ProductionClass'
# If I try to access an attribute that does not exist in the class 'ProductionClass'
# I will get an AttributeError
mock = MagicMock(spec=ProductionClass)
print(mock.method())
try:
    print(mock.method2())
except AttributeError as e:
    print(f"AttributeError in file {__file__}:", e)
    
# Using the patch decorator/context manager I can replace the method 'method' of the class 'ProductionClass'
# with a MagicMock object. This will allow me to replace the method or function that I want to test with a MagicMock.

# This means that you will control the class that you are patching completely. There will be no
# inheritance of the class that you are patching. This is important to remember because if you are
# patching a class that is used in a method of another class, you will not be able to control the
# method of the class that you are patching. You will only control the class that you are patching.
from unittest.mock import patch
import example_scripts
@patch('example_scripts.ProductionClass')
def test(mock_class):
    a = example_scripts.ProductionClass()
    assert mock_class is example_scripts.ProductionClass
    assert mock_class.called
    a.method() # <- This will not call the method of the class 'ProductionClass' since we mocked the entire class.

def non_test():
    a = example_scripts.ProductionClass()
    a.method() # <- This will call the method of the class 'ProductionClass'

# test()
# non_test()

# Also the patch decorator can be used as a context manager in a with statement
with patch.object(ProductionClass, 'method', return_value=None) as mock_method:
    a = ProductionClass()
    a.method()
    mock_method()

# Surprisingly, here I found that the return values from context managers can be
# used outside of the with statement.
print("Was the mock_method called? ", mock_method.called)
print("How many times was the mock_method called? ", mock_method.call_count)

# I can  use patch.dict for patching a dictionary during the execution of a test
foo = {'key': 'value'}
original = foo.copy()
# The assert would fail if the dictionary was not patched
with patch.dict(foo, {'newkey': 'newvalue'}, clear=True):
    assert foo == {'newkey': 'newvalue'}

assert foo == original

# Mock also supports the mocking of Python magic methods by using the MagicMock decorator.
# For example, if I don't use it, this will happen:
try:
    mock = Mock()
    print(mock + 1) # <- This will raise a TypeError where it says that
                    # the mock object does not support the addition operation.
    
except Exception as e:
    print(f"Error {type(e).__name__} occurred: {e}")
    
try:
    mock = MagicMock()
    print(mock + 1) # <- This will not raise a TypeError since the MagicMock object
                    # implements a default behavior for the addition operation.
    
except Exception as e:
    print(f"Error {type(e).__name__} occurred: {e}")


mock = Mock()
# mock.__str__.return_value = 'foobarbaz' <- this wouldn't work since the __str__ method
# is not implemented in the Mock object.
print("mock.__str__():", mock.__str__())
mock = MagicMock()
mock.__str__.return_value = 'foobarbaz' # <- This will work since the MagicMock object
                                        # implements a default behavior for the __str__ method.
print("mock.__str__():", mock.__str__())

# Auto-speccing feature
