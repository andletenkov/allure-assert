from core import _check_func

__all__ = [
    "assert_all"
    "check_that",
    "check_equal",
    # any custom assert method can be implemented
]


@_check_func
def check_that(title, cond):
    assert_that(cond, title).is_true()


@_check_func
def check_equal(title, a, b):
    assert_that(a, title).is_equal_to(b)


@contextlib.contextmanager
def assert_all(title):
    """Assertion method providing 'soft' assertion context.
    All collected failures will be raised at the end of that context.
    More info: https://github.com/assertpy/assertpy/blob/master/assertpy/assertpy.py
    """

    # create allure.step context
    with allure.step(title):

        # init soft ctx
        if assertpy._soft_ctx == 0:
            assertpy._soft_err = []
        assertpy._soft_ctx += 1

        try:
            yield
        finally:
            # reset soft ctx
            assertpy._soft_ctx -= 1

        if assertpy._soft_err and assertpy._soft_ctx == 0:
            out = 'Failed checks:'
            for i, msg in enumerate(assertpy._soft_err):
                out += '\n%d. %s' % (i + 1, msg)
            # reset msg, then raise
            assertpy._soft_err = []
            raise AssertionError(out)
