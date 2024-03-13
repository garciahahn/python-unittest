# Auto speccing creates a mock object that has the same attributes and methods
# as the object that you are trying to mock. Any functions and methods that are
# copied will have the same signature as the original object.

# This is supposed to ensure that your mocks will fail in the same way that
# code in production will fail, assuring that no functions or methods are
# called with the wrong arguments.

# As an example:

from unittest.mock import create_autospec, patch
def function(a, b, c):
    pass

mock_function = create_autospec(function, return_value='touchy')
print(mock_function(1, 2, 3))

try:
    mock_function(1, 2)
except TypeError as e:
    print(e)

try:
    mock_function.assert_called_with(1, 2, 3, 4)
except AssertionError as e:
    print(f"Assertion error!")
    print(e)

mock_function.assert_called_once_with(1, 2, 3)

# Autospec can also be created by passing the autospec argument to the
# patch decorator or the patch function. Example:
with patch('auto_speccing.function', autospec=True) as mock_func:
    try:
        function(1, 2, 3, 4) # <- This will raise a TypeError because the specced
        # function only accepts 3 arguments.
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
    
    try:
        mock_func(1, 2, 3) # <- This will not raise a TypeError because the mock
        # function was created with the same signature as the original function.
    except Exception as e:
        print(f"{type(e).__name__}: {e}")