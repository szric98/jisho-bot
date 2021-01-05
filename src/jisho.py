from bs4 import BeautifulSoup


def parse_result(result):
    # if we get an empty list,
    if not result:
        return '```Not found```'

    # display only the first 10
    display = result[:10]

    message = '```md\n'
    for d in display:
        if not d["furigana"]:
            message += f'# {d["word"]}\n{d["meaning"]}'
        else:
            message += f'# {d["word"]}【{d["furigana"]}】\n{d["meaning"]}'
    message += '```'
    return message


def span_is_empty(span):
    return not span.text


def furigana_is_provided(reading):
    return reading.text.strip()


def jisho_query(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    readings = soup.select('div.concept_light-representation > span.furigana')
    words = soup.select('div.concept_light-representation > span.text')
    meanings = soup.select(
        'div.exact_block > div.concept_light > div.concept_light-meanings > div.meanings-wrapper, div.concepts > div.concept_light > div.concept_light-meanings > div.meanings-wrapper')

    result = []

    for word in words:
        result.append({"word": word.text.strip()})

    for index, reading in enumerate(readings):
        furigana = ''
        if furigana_is_provided(reading):
            spans = reading.find_all('span')
            for i in range(len(spans)):
                if span_is_empty(spans[i]):
                    furigana += result[index]["word"][i]
                else:
                    furigana += spans[i].text
        result[index].update({"furigana": furigana})

    for index, meaning in enumerate(meanings):
        entry = ''
        for i, m in enumerate(meaning.find_all('span', attrs={"class": "meaning-meaning"})):
            # if it contains any kanji, it's the "other forms" column, so it should be skipped
            if m.text.isascii():
                no = (str(i+1) + '.').rjust(3)
                entry += f'\t{no} {m.text}\n'
        result[index].update({"meaning": entry})

    return result
