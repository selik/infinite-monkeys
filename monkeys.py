#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''

Train a Markov chain with a 2-word memory.
Randomly generate a sentence.

    $ python monkeys.py
    Might, by the image of my most painted word: O heavy burthen!

'''

from collections import defaultdict
from itertools import islice
from urllib.request import urlopen
import random, re


def download(url='http://shakespeare.mit.edu/hamlet/full.html'):
    '''
    Download "Hamlet" in HTML-format from MIT's website.
    '''
    with urlopen(url) as response:
        data = response.read()
    return data.decode('utf-8')


def parse_words(html, pattern=r'<A NAME=(\d+)\.(\d+)\.(\d+)>(.*)</A><br>'):
    '''
    Parse words of dialogue from an HTML-formatted play.
    '''
    with open('data/hamlet.html') as f:
        for line in f:
            mo = re.search(pattern, line)
            if mo is not None:
                speech = mo[4]
                for word in speech.split():
                    yield word


def build_chain(words, memory=1):
    '''
    Build a Markov chain from words.
    By default, remember only 1 previous word.
    '''
    chain = defaultdict(list)
    last = tuple(islice(words, memory))
    for term in words:
        chain[last].append(term)
        last = last[1:] + (term,)
    return chain


def sample_chain(chain, start=None):
    '''
    Walk randomly through the chain.
    '''
    if start is None:
        last = random.choice(list(chain))
    else:
        last = start
    while True:
        term = random.choice(chain[last])
        yield term
        last = last[1:] + (term,)


if __name__ == '__main__':
    filename = 'data/hamlet.html'
    try:
        with open(filename) as f:
            html = f.read()
    except FileNotFoundError as e:
        logging.error(f'Did not find "{filename}", downloading...')
        logging.exception(e)
        html = download()
        with open(filename, 'w') as f:
            f.write(html)
        logging.error(f'... Saved HTML file as "{filename}."')

    chain = build_chain(parse_words(html), memory=2)

    capitalized = [words for words in chain if words[0][0].isupper()]
    start = random.choice(capitalized)

    for word in start:
        print(word, end=' ')
    for word in sample_chain(chain, start):
        print(word, end=' ')
        if word[-1] in '.?!':
            print()
            break
