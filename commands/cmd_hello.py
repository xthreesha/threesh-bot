from .command import *

cmd_hello = Command()
cmd_hello.name = CMD_HELLO

async def cmd_hello_run(message):
    await message.reply(CMD_HELLO_REPLY)

cmd_hello.run = cmd_hello_run