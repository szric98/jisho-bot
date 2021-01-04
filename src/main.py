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

    # print(meanings)

    results = ''

    for i in range(len(readings)):
        furigana = ''
        for r in readings[i].descendants:
            if not str(r).replace(' ', '').startswith('<') and str(r) != '\n':
                furigana += r

        word = words[i].getText().replace(' ', '').replace('\n', '')

        meaning = ''

        for m in meanings[i].find_all('span', attrs={"class": "meaning-meaning"}):
            meaning += m.getText()+' '

        results += f'{word}【{furigana}】: {meaning}\n'

    await ctx.channel.send(results)


@ bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)
