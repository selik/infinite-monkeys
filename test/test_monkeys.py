'''
Tests for the infinite monkeys module.
'''

import unittest
from monkeys import Chain, WordChain

import random
from itertools import islice


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

dialogue = '''
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
But let that go.
'''

class Numbers_1121_Memory1_TestCase(unittest.TestCase):
    '''
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


if __name__ == '__main__':
    unittest.main()
