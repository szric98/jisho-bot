from dotenv import load_dotenv
import os
from discord.ext import commands
import http3
from bs4 import BeautifulSoup

load_dotenv()
TOKEN = os.getenv('TOKEN')
JISHO_URL = 'https://jisho.org/search/'

client = http3.AsyncClient()

bot = commands.Bot(command_prefix='!')


@bot.command(name='jisho', help='Search jisho.org')
async def search_jisho(ctx, arg):
    response = await client.get(JISHO_URL+arg)
    soup = BeautifulSoup(response.text, 'html.parser')
    readings = soup.select('div.concept_light-representation > span.furigana')
    words = soup.select('div.concept_light-representation > span.text')
    meanings = soup.select('.meanings-wrapper')

    res = []

    for word in words:
        res.append({"word": word.text.strip()})

    for index, reading in enumerate(readings):
        furigana = ''
        for r in reading('span', attrs={'class': "kanji"}):
            furigana += r.text
        res[index].update({"furigana": furigana})

    for index, meaning in enumerate(meanings):
        entry = ''
        for m in meaning('span', attrs={"class": "meaning-meaning"}):
            entry += f'{m.text} '
        res[index].update({"meaning": entry})

    message = ''
    for r in res:
        message += f'{r["word"]}【{r["furigana"]}】: {r["meaning"]}\n'

    await ctx.channel.send(message)


@ bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)
