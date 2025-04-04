from functools import wraps
from typing import Callable, Optional, Any, Union, Tuple, Type

def catch_exception(
    exception_types: Union[Type[Exception], Tuple[Type[Exception], ...]],
    handler: Optional[Callable[[Exception], None]] = None,
    default: Any = None
):
    """
    Decorator to catch one or more specified exception types in a function.

    Args:
        exception_types (Exception or tuple): Exception class or tuple of classes to catch.
        handler (callable, optional): A function to handle the exception.
        default (Any, optional): A value to return if exception is caught.

    Returns:
        The decorated function, returning `default` on exception.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_types as e:
                if handler:
                    handler(e)
                return default
        return wrapper
    return decorator