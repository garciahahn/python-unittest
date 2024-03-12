
def func(arg1):
    """Simple function to print the argument passed to it.

    Args:
        arg1 (any): variable to be printed
    """
    logging(f"Function {__name__} called with arg1: {arg1}")

def logging(arg):
    """Simple function to log the argument passed to it.

    Args:
        arg (any): variable to be logged
    """
    print(f"{arg}")