#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Monkeys (re)writing Shakespeare.

    $ python monkeys.py
    And dull sun not yet drunk a hundred several times.

'''
# The Complete Works of William Shakespeare is available from MIT.
# 'http://shakespeare.mit.edu/'

from collections import defaultdict
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor, as_completed
from gzip import GzipFile
from io import BytesIO
from urllib.request import Request, urlopen
import itertools, random, re, logging


host = 'http://shakespeare.mit.edu/'


class Chain(Mapping):
    '''
    A Markov chain encodes the probabilities of transitions from one
    state to another.
    '''

    def __init__(self, sequence=None, memory=1):
        '''
        The ``memory`` sets the number of states considered in the
        transition to the next state. A "memoryless" chain, that only
        considers the current state, would have a memory of 1.
        '''
        if memory < 1:
            raise ValueError('Memory must be larger than 0.')
        self.chain = defaultdict(list)
        self.memory = memory
        if sequence is not None:
            self.train(sequence)

    def __repr__(self):
        return f'<{self.__class__.__name__} {dict(self.chain)}>'

    def train(self, sequence):
        '''
        Train on a sequence of events.
        '''
        it = iter(sequence)
        if self.memory == 1:
            last = next(it)
            for event in it:
                self.chain[last].append(event)
                last = event
        else: # memory > 1
            history = tuple(itertools.islice(it, self.memory))
            if len(history) < self.memory:
                raise ValueError('Sequence must be longer than memory size')
            for event in it:
                self.chain[history].append(event)
                history = history[1:] + (event,)

    def choice(self, state):
        '''
        Randomly select a transition from a state.
        '''
        if state not in self.chain:
            raise KeyError(state)
        return random.choice(self.chain[state])

    __choice = choice

    def walk(self, start=None):
        '''
        Walk randomly through the chain. This may be infinite if all
        states in the chain have transitions, even if those transitions
        are simply a cycle back to themselves.
        '''
        if self.memory == 1:
            if start is None:
                event = random.choice(list(self.chain))
                yield event
            else:
                event = start
            while True:
                try:
                    event = self.__choice(event)
                except KeyError:
                    break
                yield event
        else: # memory > 1
            if start is None:
                history = random.choice(list(self.chain))
                for event in history:
                    yield event
            else:
                history = start
            while True:
                try:
                    event = self.__choice(history)
                except KeyError:
                    break
                yield event
                history = history[1:] + (event,)

    def __len__(self):
        '''
        Number of states in the chain.
        A state is a tuple the same size as the chain's memory.
        '''
        return len(self.chain)

    def __getitem__(self, state):
        '''
        Get a state's possible transitions.
        A state is a tuple the same size as the chain's memory.
        '''
        if state not in self.chain:
            raise KeyError(state)
        return self.chain[state]

    def __iter__(self):
        '''
        Iterator of the chain's states.
        A state is a tuple the same size as the chain's memory.
        '''
        return iter(self.chain)

    @property
    def randomness(self):
        '''
        Proportion of states that have more than 1 possible transition.
        '''
        count = len([k for k, v in self.chain.items() if len(set(v)) > 1])
        return count / len(self)

    @property
    def events(self):
        '''
        All events in the chain. Some may not be reachable by a walk.
        '''
        states = set(itertools.chain.from_iterable(self.chain))
        states.union(set(itertools.chain.from_iterable(self.chain.values())))
        return states


class WordChain(Chain):
    '''
    A Markov chain of words, suitable for generating novel sentences.
    '''

    def __init__(self, words, memory=1):
        '''
        Train the chain and stash the capitalized words for starting
        sentences.
        '''
        super().__init__(words, memory)
        self.capitalized = [words for words in self.chain
                            if words[0][0].isupper()]

    def sentence(self):
        '''
        Sample a random sentence from the chain.
        '''
        sentence = []
        start = random.choice(self.capitalized)
        rest = self.walk(start)
        if self.memory == 1:
            start = (start,)
        for word in itertools.chain(start, rest):
            sentence.append(word)
            if word[-1] in '.?!':
                return ' '.join(sentence)

    @staticmethod
    def words_from_text(lines):
        '''
        Parse words from lines of text.
        '''
        for line in lines:
            for word in line.split():
                yield word


def fetchone(url):
    '''
    Fetch content of a URL; decompress if needed
    '''
    request = Request(url)
    request.add_header('User-Agent', "infinite-monkeys")
    request.add_header('Accept-Encoding', 'gzip')
    with urlopen(request) as response:
        content = response.read()
    if response.getheader('Content-Encoding') == 'gzip':
        content = GzipFile(fileobj=BytesIO(content), mode='rb').read()
    logging.warning(f'Downloaded {url}')
    return content


def fetchmany(urls, n_threads=10, unordered=False):
    '''
    Fetch the content of many urls
    '''
    with ThreadPoolExecutor(n_threads) as pool:
        if unordered:
            futures = (pool.submit(fetchone, url) for url in urls)
            for future in as_completed(futures):
                content = future.result()
                yield content.decode('utf-8')
        else:
            for content in pool.map(fetchone, urls):
                yield content.decode('utf-8')


def parse_dialogue(html, pattern=r'<A NAME=(\d+)\.(\d+)\.(\d+)>(.*)</A><br>'):
    '''
    Parse words of dialogue from an HTML-formatted play.
    '''
    for mo in re.finditer(pattern, html):
        n_act, n_scene, n_line, speech = mo.groups()
        yield speech


def readlines(datafile='data/combined.html'):
    '''
    Lines of dialogue from the complete works of Shakespeare.
    '''
    try:
        with open(datafile) as f:
            plays = f.read()
    except FileNotFoundError as e:
        logging.error(f'Did not find "{datafile}", downloading...')
        logging.exception(e)
        index = fetchone(host).decode('utf-8')
        links = re.findall(r'<a href="(.*?)/index.html">.*?</a>', index, re.DOTALL)
        urls = (host + href + '/full.html' for href in links)
        plays = '\n'.join(fetchmany(urls, unordered=True))
        with open(datafile, 'w') as f:
            f.write(plays)
        logging.error(f'... Saved data to "{datafile}."')
    return parse_dialogue(plays)


if __name__ == '__main__':
    words = WordChain.words_from_text(readlines('data/combined.html'))
    chain = WordChain(words, memory=2)
    print(chain.sentence())
