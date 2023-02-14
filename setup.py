#!/usr/scripts/env python

from setuptools import setup, find_packages

setup(
    name="cubit-geometries",
    version="0.1.0",
    packages=find_packages(
        where="lib",
        include="cubit_geometries/*",
    ),
    package_dir={"": "lib"},
    install_requires=[
        "typer",
        "rich",
        "pyyaml",
        "jinja2",
        "schematics"
    ],
    include_package_data=True,
    entry_points="""
    [console_scripts]
    gen-geometry=cubit_geometries.entry_point:main
    """
)