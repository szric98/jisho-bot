from bs4 import BeautifulSoup
from utils import latin_char_only


def parse_result(result):
    message = ''
    for r in result:
        message += f'{r["word"]}【{r["furigana"]}】: {r["meaning"]}\n'
    return message


def jisho_query(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    readings = soup.select('div.concept_light-representation > span.furigana')
    words = soup.select('div.concept_light-representation > span.text')
    meanings = soup.select('.meanings-wrapper')

    result = []

    for word in words:
        result.append({"word": word.text.strip()})

    for index, reading in enumerate(readings):
        furigana = ''
        for r in reading.find_all('span', attrs={'class': "kanji"}):
            furigana += r.text
        result[index].update({"furigana": furigana})

    for index, meaning in enumerate(meanings):
        entry = ''
        for m in meaning.find_all('span', attrs={"class": "meaning-meaning"}):
            # if it contains any kanji, it's the "other forms" column, so it should be skipped
            if latin_char_only(m.text):
                entry += f'{m.text} '
        result[index].update({"meaning": entry})

    return result
