from dotenv import load_dotenv
import os
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')
JISHO_URL = 'https://jisho.org/search/'

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith(bot.command_prefix):
        await message.channel.send('Hi')

bot.run(TOKEN)
