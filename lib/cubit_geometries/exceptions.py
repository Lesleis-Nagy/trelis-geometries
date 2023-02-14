r"""
Program exceptions.
"""

class ParameterMissing(Exception):
    r"""
    An exception that is raised if a named kwargs parameter is missing.
    """
    def __init__(self, parameter):
        r"""
        Constructor, initialise a new ParameterMissing object with the name of the missing parameter.
        :param parameter: the name of the missing parameter.
        """
        self.parameter = parameter
