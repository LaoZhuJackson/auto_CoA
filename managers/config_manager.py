import logging
import sys

from module.config.config import Config
# sys.path.append("..\\..\\auto_CoA")

from module.save.local_storage import LocalStorageMgr

# VERSION_PATH = "./assets/config/version.txt"
# CONFIG_EXAMPLE_PATH = "./assets/config/config.example.yaml"
# CONFIG_PATH = "./config.yaml"

config = LocalStorageMgr().getLocalStorage()
