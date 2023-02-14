r"""
Configuration file.
"""

import os
import yaml

from schematics.models import Model
from schematics.types import StringType

from cubit_geometries.logger import get_logger
from cubit_geometries.decorator import static_variables

# The root configuration file name.
CONFIG_FILE_NAME = os.path.join(os.path.expanduser("~"), ".cubit-geometries.yaml")

@static_variables(configuration=None)
def load_configuration(reload=False):
    r"""
    Function to retrieve a configuration object.
    :param reload: force cache to reload configuration (by default this is false).
    :return: a Configuration object.
    """
    logger = get_logger()
    logger.debug("Retrieving configuration.")
    self = load_configuration
    if self.configuration is not None and not reload:
        logger.debug("Sending pre-cached configuration.")
        return self.configuration
    else:
        if os.path.isfile(CONFIG_FILE_NAME):
            logger.debug("Reloading configuration from file.")
            with open(CONFIG_FILE_NAME, "r") as fin:
                config_data = yaml.safe_load(fin)
                self.configuration = Configuration(config_data)
        else:
            logger.debug("No configuration found, generating default configuration.")
            self.configuration = Configuration()
            self.configuration.cubit_executable = "/Applications/Coreform-Cubit-2022.4.app/Contents/MacOS/Coreform-Cubit-2022.4"
            with open(CONFIG_FILE_NAME, "w") as fout:
                config_data = self.configuration.to_primitive()
                yaml.safe_dump(config_data, fout)

    # Return configuration.
    return self.configuration

class Configuration(Model):
    r"""
    Class to hold configuration debugrmation.
    """
    cubit_executable = StringType()
