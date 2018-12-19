import configparser
from os import path

from appdirs import AppDirs

dirs = AppDirs("umdkb", "UMDPhysicsMakers")

DEFAULT_CONFIG = """
[Serial]
port = /dev/ttyUSB0
baudrate = 115200
"""

config = configparser.ConfigParser()
config.read_string(DEFAULT_STRING)
config.read(path.join(dirs.user_config_dir, "config.ini"))

