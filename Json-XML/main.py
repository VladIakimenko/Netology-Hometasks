import json
import xml.etree.ElementTree as ElTree
import string


def read_json(path, words_length=6):
    with open(path, 'rt', encoding='UTF-8') as filehandle:
        data = json.load(filehandle)

    words = []
    for item in data['rss']['channel']['items']:
        words.extend([word.strip(string.punctuation).split()
                      for word in item['description'].split()
                      if word.isalpha() and len(word) >= words_length])
    return words


def read_xml(path, words_length=6):
    words = []
    parser = ElTree.XMLParser(encoding='UTF-8')
    tree = ElTree.parse(path, parser)

    root = tree.getroot()
    news_texts = root.findall('channel/item/description')
    for el in news_texts:
        words.extend([word.strip(string.punctuation).split()
                      for word in el.text.split()
                      if len(word) >= words_length])
    return words


def find_words(words, top_words=10):
    i = 1
    words.sort()

    while i < len(words) - 1:
        if words[i][-1][:-2] == words[i - 1][-1][:-2]:
            words[i - 1].extend(words.pop(i))
        else:
            i += 1

    return [f'{", ".join(list(set(el)))}: {len(el)}   ' for el
            in sorted(words, key=len, reverse=True)[:top_words]]


if __name__ == '__main__':
    # words = read_json(path='data/newsafr.json')
    words = read_xml(path='data/newsafr.xml')
    print(*find_words(words), sep='\n')
    input()
