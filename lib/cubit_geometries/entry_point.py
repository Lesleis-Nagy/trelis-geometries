r"""
CLI program entry point.
"""
import os
from typer import Typer

from cubit_geometries.script_generation import TruncatedOctahedronCubitScriptGenerator
from cubit_geometries.script_generation import EllipsoidCubitScriptGenerator
from cubit_geometries.mesh_generation import CubitMeshGenerator

from cubit_geometries.logger import setup_logger

app = Typer()


@app.command()
def truncated_octahedron(mesh_file: str, aspect_ratio: float, esvd_size: float, element_size: float,
                         trunc_factor: float = 0.7,
                         cubit_script_file: str = None, cubit_stdout: str = None, cubit_stderr: str = None,
                         log_file: str = None, log_level: str = "ERROR", log_to_stdout: bool = False,
                         exodus_mesh_file: str = None):
    r"""
    Produce a truncated octahedron with a given aspect ratio, size, element size and truncation factor (0.7 is the
    default).

    :param mesh_file: the output patran mesh file.
    :param aspect_ratio: the aspect ratio of the truncated octahedron, values less than zero are oblate, values greater than zero are prolate and a value exactly zero is equidimensional.
    :param esvd_size: the size of the geometry, in micron, of equivalent spherical volume diameter.
    :param element_size: the size of the geometry mesh elements, in micron.
    :param trunc_factor: the truncation factor - *MUST* be between 1.0 (for a true cub-octahedron) and 0.5.
    :param cubit_script_file: if specified, the cubit script will be written here.
    :param cubit_stdout: if specified, the standard output of cubit will be written here.
    :param cubit_stderr: if specified, the standard error of cubit will be written here.
    :param log_file: if specified a detailed run log is produced.
    :param log_level: if specified used the given log level.
    :param log_to_stdout: if specified send logging information to standard output.
    :param exodus_mesh_file: optional exodus II mesh file generation.
    :return:
    """

    # Set up our logger.
    setup_logger(log_file=log_file, log_level=log_level, log_to_stdout=log_to_stdout)

    # Create a mesh generator with a TruncatedTetrahedronCubitScriptGenerator object.
    cubit_mesh_generator = CubitMeshGenerator(TruncatedOctahedronCubitScriptGenerator(os.path.abspath(mesh_file)),
                                              cubit_script_file=cubit_script_file,
                                              cubit_stdout=cubit_stdout,
                                              cubit_stderr=cubit_stderr)

    # Execute the generator.
    abs_exodus_mesh_file = os.path.abspath(exodus_mesh_file) if exodus_mesh_file is not None else None
    cubit_mesh_generator(aspect_ratio=aspect_ratio,
                         esvd_size=esvd_size,
                         element_size=element_size,
                         trunc_factor=trunc_factor,
                         abs_exodus_mesh_file=abs_exodus_mesh_file)


@app.command()
def ellipsoid(mesh_file: str, esvd_size: float, element_size: float, prolateness: float = 1.0, oblateness: float = 1.0,
              cubit_script_file: str = None, cubit_stdout: str = None, cubit_stderr: str = None,
              log_file: str = None, log_level: str = "ERROR", log_to_stdout: bool = False,
              exodus_mesh_file: str = None):
    r"""
    Produce an ellipsoid with given prolateness and oblateness, element size. By default, both prolateness and
    oblateness are set to unity - resulting in a sphere.

    :param mesh_file: the output patran mesh file.
    :param esvd_size: the size of the geometry, in micron, of equivalent spherical volume diameter.
    :param element_size: the size of the geometry mesh elements, in micron.
    :param prolateness: with respect to Cartesian axes, this is the ratio of the length in x to the length in y.
    :param oblateness: with respect to Cartesian axes, this is the ratio of the length in y to the length in z.
    :param cubit_script_file: if specified, the cubit script will be written here.
    :param cubit_stdout: if specified, the standard output of cubit will be written here.
    :param cubit_stderr: if specified, the standard error of cubit will be written here.
    :param log_file: if specified a detailed run log is produced.
    :param log_level: if specified used the given log level.
    :param log_to_stdout: if specified send logging information to standard output.
    :param exodus_mesh_file: optional exodus II mesh file generation.
    :return:
    """

    # Set up our logger
    # Set up our logger.
    setup_logger(log_file=log_file, log_level=log_level, log_to_stdout=log_to_stdout)

    # Create a mesh generator with a TruncatedTetrahedronCubitScriptGenerator object.
    cubit_mesh_generator = CubitMeshGenerator(EllipsoidCubitScriptGenerator(os.path.abspath(mesh_file)),
                                              cubit_script_file=cubit_script_file,
                                              cubit_stdout=cubit_stdout,
                                              cubit_stderr=cubit_stderr)

    # Execute the generator.
    abs_exodus_mesh_file = os.path.abspath(exodus_mesh_file) if exodus_mesh_file is not None else None
    cubit_mesh_generator(esvd_size=esvd_size,
                         element_size=element_size,
                         prolateness=prolateness,
                         oblateness=oblateness,
                         abs_exodus_mesh_file=abs_exodus_mesh_file)


def main():
    app()


if __name__ == "__main__":
    main()
