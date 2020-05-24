import contextlib
import allure
from functools import wraps
from assertpy import assertpy, assert_that


def _fake_err():
    """Mocks python exception object"""
    try:
        raise AssertionError
    except Exception as e:
        return e


def _check_func(func):
    """Assertion method decorator"""

    @wraps(func)
    def wrapper(*a, **kw):
        try:
            title = kw["title"]
        except:
            title = a[0]
        step_ctx = allure.step(f"Check: {title}")
        step_ctx.__enter__()

        err_num = len(assertpy._soft_err)

        func(*a, **kw)

        if len(assertpy._soft_err) > err_num:

            # create fake exception object to explicitly fail allure step
            fe = _fake_err()

            step_ctx.__exit__(exc_type=type(fe), exc_val=fe, exc_tb=fe.__traceback__)
        else:
            step_ctx.__exit__(exc_type=None, exc_val=None, exc_tb=None)

    return wrapper
