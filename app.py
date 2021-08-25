from bot import *
from config import *

config = Config()

client = ThreeshBot(config)
client.run(config.token)
