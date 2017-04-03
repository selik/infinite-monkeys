########################################################################
Infinite Monkeys
########################################################################

The `infinite monkey theorem`_ suggests that a monkey pressing keys
randomly at a keyboard will, eventually, write the `Complete Works of
William Shakespeare`_.

.. pull-quote::

   "Words, words, words." -- Hamlet_

We can simulate infinite monkeys as a Markov chain and create mildly
realistic Shakespearean verse. To increase the realism, you can increase
the ``WordChain``'s ``memory``. On relatively small datasets like
Shakespeare's, the chain rapidly becomes a random quote selector rather
than a simulator.

============  ==========  ======================================================
Memory        Randomness  Example generated sentence
============  ==========  ======================================================
Last word     44.65%      Yea and could meet him I am your valour preys on you.
Last 2 words  17.08%      Hath raised in me But as the day of doom.
Last 3 words  5.03%       Which of you saw Sir Eglamour of late?
Last 4 words  0.88%       We have not spoke us yet of torchbearers.
============  ==========  ======================================================

"Randomness" is the percent of states in the chain with more than 1 transition.


.. _`infinite monkey theorem`: https://en.wikipedia.org/wiki/Infinite_monkey_theorem

.. _`Complete Works of William Shakespeare`: http://shakespeare.mit.edu/

.. _Hamlet: http://shakespeare.mit.edu/hamlet/hamlet.2.2.html#speech52

----

Copyright (c) 2017 Michael Selik.
