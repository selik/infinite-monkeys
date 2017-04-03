#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Collect the text of "Hamlet" from MIT's website.
Parse dialogue from the HTML-formatted play.
Train a Markov chain with a 2-word memory.
Randomly generate a sentence.

    $ python monkeys.py
    This spirit, dumb to us, will speak With most miraculous organ.

'''

# Comment-out any sections you don't wish to repeat if running this
# script multiple times. It's impolite to frequently and repeatedly
# download the same file from the MIT website.


########################################################################
### Collect: gather the data from original(ish) source

from urllib.request import urlopen

url = 'http://shakespeare.mit.edu/hamlet/full.html'

with urlopen(url) as response:
    data = response.read()

html = data.decode('utf-8')

with open('data/hamlet.html', 'w') as f:
    f.write(html)


########################################################################
### Wrangle: transform, filter, combine, aggregate to a clean format

import re

pattern = r'<A NAME=(\d+)\.(\d+)\.(\d+)>(.*)</A><br>'

dialogue = []
with open('data/hamlet.html') as f:
    for line in f:
        mo = re.search(pattern, line)
        if mo is not None:
            act, scene, line, text = mo.groups()
            dialogue.append(text)

with open('data/dialogue.txt', 'w') as f:
    f.write('\n'.join(dialogue))


########################################################################
### Analyze: make a useful generalization

from collections import defaultdict
import pickle

chain = defaultdict(list)
size = 2

last = (None,) * size
with open('data/dialogue.txt') as f:
    for line in f:
        for word in line.split():
            chain[last].append(word)
            last = last[1:] + (word,)

# Discard any keys with a None
chain = {k: v for k, v in chain.items() if None not in k}

# Stash the trained Markov chain in a pickle file.
with open('data/chain.pickle', 'wb') as f:
    pickle.dump(chain, f)


########################################################################
### Report: an application, for varying definitions of the term

import pickle
import random

with open('data/chain.pickle', 'rb') as f:
    chain = pickle.load(f)

sentence = []

capitalized = [words for words in chain if words[0][0].isupper()]
last = random.choice(capitalized)
for word in last:
    sentence.append(word)

while word[-1] not in '.?!':
    word = random.choice(chain[last])
    sentence.append(word)
    last = last[1:] + (word,)

print(' '.join(sentence))
