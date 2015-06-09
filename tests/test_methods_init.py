# -*- coding: utf-8 -*-

'''Samples storage module tests
'''

from __future__ import with_statement, division, absolute_import, print_function

from aorn.methods import thr, zcs
from aorn.methods.antest import ANTest


def test_methods():
    modules = [thr, zcs]
    for mod in modules:
        assert issubclass(mod, ANTest)


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
