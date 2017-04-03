########################################################################
Infinite Monkeys
########################################################################

The `infinite monkey theorem`_ suggests that a monkey pressing keys
randomly at a keyboard will, eventually, write the complete works of
William Shakespeare.

Simple containers (such as the Python ``list`` and ``dict``) can be
composed to implement complex data structures and algorithms. A classic
example is a Markov Chain that can be trained on a corpus of text to
randomly generate new sentences. Collecting the works of `William
Shakespeare from MIT`_, we can simulate infinite monkeys and create
mildly-realistic Shakespearean verse.


.. _`infinite monkey theorem`: https://en.wikipedia.org/wiki/Infinite_monkey_theorem

.. _`William Shakespeare from MIT`: http://shakespeare.mit.edu/


------------------------------------------------------------------------
The Tragedy of Hamlet
------------------------------------------------------------------------

.. pull-quote::

	"Words, words, words." -- Hamlet_

1. Collect the text of "Hamlet" from MIT's website.
2. Parse dialogue from the HTML-formatted play.
3. Train a Markov chain with a 2-word memory.
4. Randomly generate a sentence.

Comment-out any sections you don't wish to repeat if running this script
multiple times. It's impolite to frequently and repeatedly download the
same file from the MIT website.


.. _Hamlet: http://shakespeare.mit.edu/hamlet/hamlet.2.2.html#speech52

----

Copyright (c) 2017 Michael Selik.
