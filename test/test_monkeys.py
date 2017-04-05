'''
Tests for the infinite monkeys module.
'''

import unittest
from monkeys import Chain, WordChain, parse_dialogue

import random
from itertools import islice


class Numbers_112_Memory1_TestCase(unittest.TestCase):
    '''
    1: 50% -> 1
       50% -> 2
    2: no transitions
    '''

    seq = [1, 1, 2]

    def setUp(self):
        random.seed(42)

    def test_dict(self):
        chain = Chain(self.seq)
        self.assertEqual(chain, {1: [1, 2]})

    def test_walk_no_start(self):
        chain = Chain(self.seq)
        self.assertEqual(list(islice(chain.walk(), 10)), [1, 1, 2])

    def test_walk_start_1(self):
        chain = Chain(self.seq)
        self.assertEqual(list(islice(chain.walk(start=1), 10)), [1, 1, 2])

    def test_walk_start_2(self):
        chain = Chain(self.seq)
        self.assertEqual(list(islice(chain.walk(start=2), 10)), [])


class Numbers_1121_Memory1_TestCase(unittest.TestCase):
    '''
    1: 50% -> 1
       50% -> 2
    2: 100% -> 1
    '''

    seq = [1, 1, 2, 1]

    def setUp(self):
        random.seed(42)

    def test_dict(self):
        chain = Chain(self.seq)
        self.assertEqual(chain, {1: [1, 2], 2: [1]})

    def test_walk_no_start(self):
        chain = Chain(self.seq)
        self.assertEqual(list(islice(chain.walk(), 10)),
                         [1, 1, 2, 1, 1, 1, 1, 1, 2, 1])

    def test_walk_start_1(self):
        chain = Chain(self.seq)
        self.assertEqual(list(islice(chain.walk(start=1), 10)),
                         [1, 1, 2, 1, 1, 1, 1, 1, 2, 1])

    def test_walk_start_2(self):
        chain = Chain(self.seq)
        self.assertEqual(list(islice(chain.walk(start=2), 10)),
                         [1, 1, 2, 1, 1, 1, 1, 1, 2, 1])


class Numbers_1121_Memory2_TestCase(unittest.TestCase):
    '''
    1: 50% -> 1
       50% -> 2
    2: 100% -> 1
    '''

    seqs = [
        [1, 1, 1],
        [1, 1, 2],

        [1, 2, 2],
        [1, 2, 1],
        [1, 2, 1],
        [1, 2, 1],

        [2, 1, 1],
    ]

    def setUp(self):
        random.seed(42)
        self.chain = Chain(memory=2)
        for seq in self.seqs:
            self.chain.train(seq)

    def test_dict(self):
        self.assertEqual(self.chain,
            {(1, 1): [1, 2],
             (1, 2): [2, 1, 1, 1],
             (2, 1): [1]})

    def test_walk_no_start(self):
        self.assertEqual(list(islice(self.chain.walk(), 10)),
                         [2, 1, 1, 1, 2, 1, 1, 1, 1, 1])

    def test_walk_start_11(self):
        self.assertEqual(list(self.chain.walk(start=(1, 1))),
                         [1, 1, 2, 1, 1, 1, 1, 1, 2, 2])

    def test_walk_start_21(self):
        self.assertEqual(list(self.chain.walk(start=(2, 1))),
                         [1, 1, 2, 1, 1, 1, 1, 1, 2, 2])

    def test_walk_start_12(self):
        self.assertEqual(list(self.chain.walk(start=(1, 2))), [2])

    def test_walk_start_22(self):
        self.assertEqual(list(self.chain.walk(start=(2, 2))), [])


class Polonius_TestCase(unittest.TestCase):
    '''
    '''

    html = '''
<A NAME=speech19><b>LORD POLONIUS</b></a>
<blockquote>
<A NAME=2.2.91>                  This business is well ended.</A><br>
<A NAME=2.2.92>My liege, and madam, to expostulate</A><br>
<A NAME=2.2.93>What majesty should be, what duty is,</A><br>
<A NAME=2.2.94>Why day is day, night night, and time is time,</A><br>
<A NAME=2.2.95>Were nothing but to waste night, day and time.</A><br>
<A NAME=2.2.96>Therefore, since brevity is the soul of wit,</A><br>
<A NAME=2.2.97>And tediousness the limbs and outward flourishes,</A><br>
<A NAME=2.2.98>I will be brief: your noble son is mad:</A><br>
<A NAME=2.2.99>Mad call I it; for, to define true madness,</A><br>
<A NAME=2.2.100>What is't but to be nothing else but mad?</A><br>
<A NAME=2.2.101>But let that go.</A><br>
</blockquote>
    '''

    dialogue = '''\
                  This business is well ended.
My liege, and madam, to expostulate
What majesty should be, what duty is,
Why day is day, night night, and time is time,
Were nothing but to waste night, day and time.
Therefore, since brevity is the soul of wit,
And tediousness the limbs and outward flourishes,
I will be brief: your noble son is mad:
Mad call I it; for, to define true madness,
What is't but to be nothing else but mad?
But let that go.'''

    words = ['This', 'business', 'is', 'well', 'ended.',
        'My', 'liege,', 'and', 'madam,', 'to', 'expostulate',
        'What', 'majesty', 'should', 'be,', 'what', 'duty', 'is,',
        'Why', 'day', 'is', 'day,', 'night', 'night,', 'and', 'time', 'is', 'time,',
        'Were', 'nothing', 'but', 'to', 'waste', 'night,', 'day', 'and', 'time.',
        'Therefore,', 'since', 'brevity', 'is', 'the', 'soul', 'of', 'wit,',
        'And', 'tediousness', 'the', 'limbs', 'and', 'outward', 'flourishes,',
        'I', 'will', 'be', 'brief:', 'your', 'noble', 'son', 'is', 'mad:',
        'Mad', 'call', 'I', 'it;', 'for,', 'to', 'define', 'true', 'madness,',
        'What', "is't", 'but', 'to', 'be', 'nothing', 'else', 'but', 'mad?',
        'But', 'let', 'that', 'go.']

    def setUp(self):
        random.seed(42)

    def test_parse_dialogue(self):
        lines = self.dialogue.splitlines()
        self.assertEqual(list(parse_dialogue(self.html)), lines)

    def test_words_from_text(self):
        lines = self.dialogue.splitlines()
        self.assertEqual(list(WordChain.words_from_text(lines)), self.words)

    def test_sentence(self):
        lines = parse_dialogue(self.html)
        words = WordChain.words_from_text(lines)
        chain = WordChain(words)
        self.assertTrue(chain.sentence()[-1] in '.?!')


if __name__ == '__main__':
    unittest.main()
