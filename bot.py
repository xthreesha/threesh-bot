from constants import *
from commands import *
from markov import *
import discord
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class ThreeshBot(discord.Client):
    def __init__(self, config):
        self.config = config
        self.markov = MarkovChain(config)
        super().__init__()

    async def on_ready(self):
        logging.log(logging.INFO, f'Бот запущен под именем {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content[0] != self.config.cmd:
            self.markov.add_text(message.content)
            if (random.randint(1, int(1 / float(self.config.generate_msg_chance))) == 1):
                text = self.markov.get_text(random.randint(5, 25))
                await message.channel.send(text)

            return

        cmd_msg = message.content.split()[0].lower()
        cmd_found = False

        cmd_msg = cmd_msg[1:]

        logging.log(logging.INFO, f'Запускаем команду {cmd_msg}')

        for cmd in self.config.commands:
            if cmd.name == cmd_msg:
                cmd_found = True
                await cmd.run(message)
                break
        
        if not cmd_found:
            logging.log(logging.INFO, f'Команда {cmd_msg} не найдена')
            await message.reply(TXT_COMMAND_NOT_FOUND)
            