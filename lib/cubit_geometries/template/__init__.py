r"""
Package level utility function for templates.
"""

import jinja2

from cubit_geometries.decorator import static_variables

@static_variables(loader=None)
def template_loader():
    r"""
    Retrieve the template loader for all geometry templates.
    :return: the geometry template loader.
    """
    if template_loader.loader is None:
        template_loader.loader = jinja2.Environment(
            loader=jinja2.PackageLoader("cubit_geometries", "template"),
            autoescape=jinja2.select_autoescape(["jinja2"])
        )

    return template_loader.loader
