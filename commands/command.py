import logging
from constants import *
class Command:
    def run(message):
        logging.log(logging.WARNING, 'UNDEFINED RUN')

    def __init__(self):
        self.name = 'undefined'