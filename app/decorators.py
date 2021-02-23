import inspect
import traceback
from functools import wraps
from logging import getLogger
from psycopg2 import Error, OperationalError


def ErrorDefender(func):
    logger = getLogger('error')

    @wraps(func)
    def wrapper(*a, **kw):
        class_method = str(func)
        try:
            return func(*a, **kw)
        except NotImplementedError as e:
            raise e
        except OperationalError as e:
            error = repr(e)
            logger.error(f"An error occurred in {class_method}: {error}")
            logger.error(traceback.format_exc())
            return {
                'class_method': class_method,
                'error': error
            }
        except Error as e:
            error = repr(e)
            a[0].rollback()
            logger.error(f"An error occurred in {class_method}: {error}")
            logger.error(traceback.format_exc())
            return {
                'class_method': class_method,
                'error': error
            }
        except BaseException as e:
            error = repr(e)
            args = ()
            logger.error(f"An error occurred in {class_method}: {error}", *args)
            logger.error(traceback.format_exc())
            return {
                'class_method': class_method,
                'error': error
            }
    return wrapper


def decorate_all_methods(decorator, exclude=None):
    if exclude is None:
        exclude = ['__init__']

    def apply_decorator(cls):
        for k, f in cls.__dict__.items():
            if inspect.isfunction(f) and k not in exclude:
                setattr(cls, k, decorator(f))
        return cls
    return apply_decorator
