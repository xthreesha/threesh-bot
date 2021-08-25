from configparser import Error
import random
import psycopg2 as psql
import logging
import re
from constants import *

class MarkovChain:
    def __init__(self, config):
        self.config = config
        self.psql = psql.connect(**config.psql_info)
        self.psql_cur = self.psql.cursor()
        self.psql_cur.execute("create table if not exists data (word text, other text[]);")

    def add_pair(self, pair):
        try:
            self.psql_cur.execute(f"select word from data where word = '{pair[0]}';")
            found = self.psql_cur.fetchone()

        except Error as err:
            logging.log(logging.WARNING, err)
            found = False
        
        if not found:
            logging.log(logging.INFO, f"Couldn't find word {pair[0]}, creating new row")
            self.psql_cur.execute(f"insert into data (word, other) values ('{pair[0]}', '{{\"{pair[1]}\"}}');")
            self.psql_cur.execute(f"insert into data (word, other) values ('{pair[1]}', '{{\"{pair[0]}\"}}');")
        else:
            self.psql_cur.execute(f"update data set other = array_append(other, '{pair[1]}') where word = '{pair[0]}';")
            self.psql_cur.execute(f"update data set other = array_append(other, '{pair[0]}') where word = '{pair[1]}';")

    def add_text(self, text):
        logging.log(logging.INFO, f"Markov chain: Adding text {text[:min(20,len(text))]}...")

        words = re.sub("[^\w\s]", "", text).split()

        for i in range(len(words) - 1):
            self.add_pair([words[i], words[i + 1]])

    def get_next_word(self, word):
        logging.log(logging.INFO, f"get_next_word: {word}")
        if (word == ""):
            self.psql_cur.execute(f"select word from data;")
            words = self.psql_cur.fetchone()
            logging.log(logging.INFO, words)
            return random.choice(words)

        self.psql_cur.execute(f"select other from data where word = '{word}';")
        next_words = self.psql_cur.fetchone()[0]
        logging.log(logging.INFO, next_words)
        return random.choice(next_words)

    def get_text(self, n_words):
        text = ""
        word = ""
        for i in range(n_words):
            word = self.get_next_word(word)
            text += " " + word

        return text
