r"""
Globals object
"""

class GLOBALS:

    # The global logger name.
    LOGGER_NAME = "cubit_geometries_logger"

    # The format used for logging.
    LOGGER_FORMAT = "%(asctime)s — %(levelname)s — %(pathname)s:%(funcName)s:%(lineno)d — %(message)s"

    # The temporary name of the cubit script when we're generating meshes.
    CUBIT_SCRIPT_NAME = "temporary.cubit"
