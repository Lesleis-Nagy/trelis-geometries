r"""
Decorators used in this package.
"""

def static_variables(**kwargs):
    r"""
    Decorate a function with static data members.
    :param kwargs: key value pairs to add as static variables.
    :return: a function with additional static variables.
    """
    def wrap(func):
        for key, value in kwargs.items():
            setattr(func, key, value)
        return func
    return wrap
