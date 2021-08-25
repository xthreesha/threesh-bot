import logging
import os
from re import S
from constants import *
from commands import *
import configparser

class Config:
    """ A class that holds config information """
    def __init__(self):
        config = configparser.ConfigParser()

        # Мы не хотим показывать токен, читаем из файла
        config_file_path = \
            os.path.join(os.path.dirname(__file__), CONFIG_FILE_NAME)
        with open(config_file_path, "r") as config_file:
            logging.log(logging.INFO, f'Читаем конфиг из файла {config_file_path}')
            config.read_file(config_file)

            self.token = config[CFG_GENERAL][CFG_TOKEN]
            self.cmd = config[CFG_GENERAL][CFG_COMMAND_START]
            self.generate_msg_chance = config[CFG_GENERAL][CFG_GENERATE_MSG_CHANCE]

            self.psql_info = config[CFG_POSTGRESQL]

            self.commands = commands
