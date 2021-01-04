from dotenv import load_dotenv
import os
from discord.ext import commands
import http3
from jisho import jisho_query, parse_result

load_dotenv()

TOKEN = os.getenv('TOKEN')
JISHO_URL = 'https://jisho.org/search/'

client = http3.AsyncClient()
bot = commands.Bot(command_prefix='!')


@bot.command(name='jisho', help='Search jisho.org')
async def search_jisho(ctx, arg):
    response = await client.get(JISHO_URL + arg)
    result = jisho_query(response)
    message = parse_result(result)

    await ctx.channel.send(message)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)
