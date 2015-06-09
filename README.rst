AorN
====

.. image:: https://api.travis-ci.org/soutys/aorn.png?branch=master
    :target: http://travis-ci.org/soutys/aorn
.. image:: https://coveralls.io/repos/soutys/aorn/badge.png?branch=master
    :target: https://coveralls.io/r/soutys/aorn
.. image:: https://pypip.in/v/python-aorn/badge.png
    :target: https://pypi.python.org/pypi/python-aorn/
.. image:: https://pypip.in/d/python-aorn/badge.png
    :target: https://pypi.python.org/pypi/python-aorn/
.. image:: https://pypip.in/wheel/python-aorn/badge.png
    :target: https://pypi.python.org/pypi/python-aorn/

Extendable "audio or not" testing toolkit.


Usage
=====

General help::

    aorn --help

Sample threshold test (20% level)::

    avconv -i ... -f s16le -acodec pcm_s16le -ac 1 -t 00:00:10.000 -y - | \
        aorn -f - -m aorn.methods.thr:0.2 -t audio

or::

    aorn -f test.pcm -m aorn.methods.thr:0.2 -t audio


License
=======

MIT


TODO
====

- better algos/methods;
- in-tests package builder (see `vaab/colour <https://github.com/vaab/colour/blob/master/.travis.yml>`);

