from module.config.config import Config
import os

VERSION_PATH = "./assets/config/version.txt"
CONFIG_EXAMPLE_PATH = "./assets/config/config.example.yaml"
CONFIG_PATH = "./config.yaml"

config = Config(VERSION_PATH, CONFIG_EXAMPLE_PATH, CONFIG_PATH)
