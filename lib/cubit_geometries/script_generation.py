r"""
These routines generate cubit scripts.
"""

from abc import ABCMeta, abstractmethod

import os

from cubit_geometries import GLOBALS

from cubit_geometries.logger import get_logger
from cubit_geometries.template import template_loader

from cubit_geometries.exceptions import ParameterMissing


class CubitScriptGenerator(metaclass=ABCMeta):
    r"""
    The parent class of all cubit script generation objects.
    """

    def __init__(self, abs_mesh_file: str):
        r"""
        All cubit scripts must have a cubit mesh file name, which will be the mesh file that is produced as part of the
        output.
        :param abs_mesh_file:
        """
        self.abs_mesh_file = abs_mesh_file

    @abstractmethod
    def __call__(self, temp_dir: str, **kwargs) -> None:
        r"""
        All cubit script generators must implement the __call__ method and pass a temp_dir along with the keyword
        arguments that will be used to generate the mesh, the result of this method MUST be a file called
        GLOBALS.CUBIT_SCRIPT_NAME in the `temp_dir` directory.
        :param temp_dir: the temporary directory in which the cubit script generator works.
        :param kwargs: the keyword arguments that the implementation will use to generate cubit scripts.
        :return: None, but as a side effect a file called GLOBALS.CUBIT_SCRIPT_NAME *MUST* be generated in `temp_dir`.
        """
        pass


class TruncatedOctahedronCubitScriptGenerator(CubitScriptGenerator):
    r"""
    A cubit script generator for truncated octahedra.
    """

    def __init__(self, abs_mesh_file):

        super().__init__(abs_mesh_file)

    def __call__(self, temp_dir, **kwargs):

        logger = get_logger()

        logger.debug(f"Working in directory: '{os.getcwd()}'")
        logger.debug(f"Mesh file absolute path: '{self.abs_mesh_file}'.")

        aspect_ratio = kwargs.get("aspect_ratio")
        if aspect_ratio is None:
            raise ParameterMissing("aspect_ratio")
        logger.debug("Parameter 'aspect_ratio' is present.")

        esvd_size = kwargs.get("esvd_size")
        if esvd_size is None:
            raise ParameterMissing("esvd_size")
        logger.debug("Parameter 'esvd_size' is present.")

        element_size = kwargs.get("element_size")
        if element_size is None:
            raise ParameterMissing("element_size")
        logger.debug("Parameter 'element_size' is present.")

        trunc_factor = kwargs.get("trunc_factor")
        if trunc_factor is None:
            raise ParameterMissing("trunc_factor")
        logger.debug("Parameter 'trunc_factor' is present.")

        abs_exodus_mesh_file = kwargs.get("abs_exodus_mesh_file")
        logger.debug(f"Parameter 'abs_exodus_mesh_file' is {abs_exodus_mesh_file}")

        loader = template_loader()

        if aspect_ratio > 1.0:
            logger.debug("Aspect ratio is greater than 1, using prolate truncated octahedron.")
            elongation = 100.0 * (aspect_ratio - 1)
            template = loader.get_template("truncated_octahedron_prolate.jinja2")
            output = template.render(trunc_factor=trunc_factor,
                                     elongation=elongation,
                                     esvd_size=esvd_size,
                                     element_size=element_size,
                                     abs_mesh_file=self.abs_mesh_file,
                                     abs_exodus_mesh_file=abs_exodus_mesh_file)
        elif aspect_ratio < 1.0:
            logger.debug("Aspect ratio is less than 1, using oblate truncated octahedron.")
            squash = (100.0 * (1 - aspect_ratio)) / aspect_ratio
            template = loader.get_template("truncated_octahedron_oblate.jinja2")
            output = template.render(trunc_factor=trunc_factor,
                                     squash=squash,
                                     esvd_size=esvd_size,
                                     element_size=element_size,
                                     abs_mesh_file=self.abs_mesh_file,
                                     abs_exodus_mesh_file=abs_exodus_mesh_file)
        else:
            logger.debug("Aspect ratio is equal to 1, using equidimensional truncated octahedron.")
            template = loader.get_template("truncated_octahedron_equidimensional.jinja2")
            output = template.render(trunc_factor=trunc_factor,
                                     esvd_size=esvd_size,
                                     element_size=element_size,
                                     abs_mesh_file=self.abs_mesh_file,
                                     abs_exodus_mesh_file=abs_exodus_mesh_file)

        logger.debug(f"Writing cubit script to '{GLOBALS.CUBIT_SCRIPT_NAME}'.")
        with open(GLOBALS.CUBIT_SCRIPT_NAME, "w") as fout:
            fout.write(f"{output}\n")


class EllipsoidCubitScriptGenerator(CubitScriptGenerator):
    r"""
    A cubit script generator for ellipsoids.
    """

    def __init__(self, abs_mesh_file: str):

        super().__init__(abs_mesh_file)

    def __call__(self, temp_dir:str, **kwargs):

        logger = get_logger()

        logger.debug("")

        esvd_size = kwargs.get("esvd_size")
        if esvd_size is None:
            raise ParameterMissing("esvd_size")
        logger.debug("Parameter 'esvd_size' is present.")

        prolateness = kwargs.get("prolateness")
        if prolateness is None:
            raise ParameterMissing("prolateness")
        logger.debug("Parameter 'prolateness' is present.")

        oblateness = kwargs.get("oblateness")
        if oblateness is None:
            raise ParameterMissing("oblateness")
        logger.debug("Parameter 'oblateness' is present.")

        element_size = kwargs.get("element_size")
        if element_size is None:
            raise ParameterMissing("element_size")
        logger.debug("Parameter 'element_size' is present.")

        abs_exodus_mesh_file = kwargs.get("abs_exodus_mesh_file")
        logger.debug(f"Parameter 'abs_exodus_mesh_file' is {abs_exodus_mesh_file}")

        loader = template_loader()

        logger.debug(f"Generating ellipsoid with prolateness: {prolateness} and oblateness {oblateness}.")
        template = loader.get_template("ellipsoid.jinja2")
        output = template.render(esvd_size=esvd_size,
                                 prolateness=prolateness,
                                 oblateness=oblateness,
                                 element_size=element_size,
                                 abs_mesh_file=self.abs_mesh_file,
                                 abs_exodus_mesh_file=abs_exodus_mesh_file)

        logger.debug(f"Writing cubit script to '{GLOBALS.CUBIT_SCRIPT_NAME}'.")
        with open(GLOBALS.CUBIT_SCRIPT_NAME, "w") as fout:
            fout.write(f"{output}\n")
