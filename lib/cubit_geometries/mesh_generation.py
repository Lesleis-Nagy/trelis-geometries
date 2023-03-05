r"""
These routines will generate cubit meshes.
"""

from subprocess import Popen, PIPE

import os
import shutil
import tempfile

from cubit_geometries.logger import get_logger

from cubit_geometries import GLOBALS

from cubit_geometries.configuration import load_configuration

from cubit_geometries.script_generation import CubitScriptGenerator

# Flags required for CUBIT
CUBIT_FLAGS = [
    "-batch",
    "-nographics",
    "-nojournal",
]


class CubitMeshGenerator:
    r"""
    A class that will generate cubit meshes by calling a CubitScriptGenerator.
    """

    def __init__(self, script_generator: CubitScriptGenerator, cubit_script_file: str = None, cubit_stdout: str = None,
                 cubit_stderr: str = None):
        r"""
        Create a new object that will generate meshes.

        :param script_generator: a CubitScriptGenerator subclass that knows how to generate cubit scripts for the
                                 mesh that we're interested in generating.
        :param cubit_script_file: if this is not empty, the cubit script file used to generate the mesh will be stored
                                  here.
        :param cubit_stdout: if this is not empty, the cubit standard output produced while generating the mesh will
                             be stored here.
        :param cubit_stderr: if this is not empty, the cubit standard error output produced while generating the mesh
                             will be stored here.
        """

        self.script_generator = script_generator

        logger = get_logger()

        logger.debug(f"Checking for optional parameters.")

        if cubit_script_file is not None:
            self.abs_cubit_script_file = os.path.abspath(cubit_script_file)
        else:
            self.abs_cubit_script_file = None
        logger.debug(f"Setting cubit script file: '{self.abs_cubit_script_file}'")

        if cubit_stdout is not None:
            self.abs_cubit_script_stdout = os.path.abspath(cubit_stdout)
        else:
            self.abs_cubit_script_stdout = None
        logger.debug(f"Setting cubit stdout file: '{self.abs_cubit_script_stdout}'")

        if cubit_stderr is not None:
            self.abs_cubit_script_stderr = os.path.abspath(cubit_stderr)
        else:
            self.abs_cubit_script_stderr = None
        logger.debug(f"Setting cubit stderr file: '{self.abs_cubit_script_stderr}")

    def __call__(self, **kwargs):
        r"""
        Call the mesh generator with the given keyword argument.
        :param kwargs: the values specific for each geometry.
        :return:
        """

        logger = get_logger()

        with tempfile.TemporaryDirectory() as temp_dir:

            logger.debug(f"Changing in to temporary directory '{temp_dir}'")
            os.chdir(temp_dir)
            logger.debug("Done!")

            logger.debug("Calling generator routine.")
            self.script_generator(temp_dir, **kwargs)
            logger.debug("Done!")

            logger.debug("Running cubit script.")
            result = run_cubit(GLOBALS.CUBIT_SCRIPT_NAME)
            logger.debug("Done!")

            if self.abs_cubit_script_file is not None:
                logger.debug(f"Creating cubit script file: '{self.abs_cubit_script_file}'.")
                shutil.copyfile(GLOBALS.CUBIT_SCRIPT_NAME, self.abs_cubit_script_file)

            if self.abs_cubit_script_stdout is not None:
                with open(self.abs_cubit_script_stdout, "w") as fout:
                    logger.debug(f"Creating cubit stdout file: '{self.abs_cubit_script_stdout}'.")
                    fout.write(f"{result.stdout}\n")

            if self.abs_cubit_script_stderr is not None:
                with open(self.abs_cubit_script_stderr, "w") as fout:
                    logger.debug(f"Creating cubit stderr file: '{self.abs_cubit_script_stderr}'.")
                    fout.write(f"{result.stderr}\n")

            if result.success:
                # Check that the file exists.
                if not os.path.isfile(self.script_generator.abs_mesh_file):
                    print("Run was successful but the mesh could *NOT* be generated (see the standard output using "
                          "the --cubit-stdout option for more details).")
                else:
                    print("Run was successful")
            else:
                print("Run failed for some reason (use --cubit-stdout, --cubit-stderr and --log flags for diagnostics.")


class CubitRunResult:
    r"""
    Class to capture the result of a cubit/trelis run.
    """

    def __init__(self, stdout, stderr, success):
        r"""
        Constructor create a new CubitRunResult object.
        :param stdout: the standard output produced by cubit/trelis.
        :param stderr: the standard error produced by cubit/trelis.
        :param success: boolean flag to indicate if the generation was successful.
        """
        self.stdout = stdout
        self.stderr = stderr
        self.success = success


def run_cubit(cubit_script_file: str, directory: str = None) -> CubitRunResult:
    r"""
    Utility function to run the cubit/trelis script on the input script.
    :param cubit_script_file: the name of the input cubit/trelis script file.
    :param directory: the directory in which the script should be run.
    :return:
    """
    config = load_configuration()
    logger = get_logger()

    cwd = os.getcwd()

    try:

        if directory is not None:
            logger.debug(f"Current working directory is: '{cwd}'.")
            os.chdir(directory)
            logger.debug(f"Changed directory to: '{directory}'.")

        command = f"{config.cubit_executable} {' '.join(CUBIT_FLAGS)} {cubit_script_file}"

        logger.debug(f"Executing cubit command: '{command}'.")
        proc = Popen(command, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)

        logger.debug(f"Retrieving stderr, and stdout.")
        stdout, stderr = proc.communicate()

        if len(stderr) == 0:
            success = True
        else:
            success = False

        logger.debug("Finished executing cubit.")
        return CubitRunResult(stdout, stderr, success)

    finally:

        if directory is not None:
            logger.debug(f"Changing directory back to '{cwd}'.")
            os.chdir(cwd)
