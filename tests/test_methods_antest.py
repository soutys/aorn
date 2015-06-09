# -*- coding: utf-8 -*-

'''Samples storage module tests
'''

from __future__ import with_statement, division, absolute_import, print_function

from aorn.methods.antest import ANTest


class SampleTest(ANTest):
    __doc__ = ''
    def analyze(self, _):
        pass


def test_antest_init():
    try:
        ANTest()
        assert False
    except TypeError:
        pass


def test_antest_get_doc():
    assert issubclass(SampleTest, ANTest)
    smp_test = SampleTest()
    doc = smp_test.get_doc()
    assert len(doc) == 0


def test_antest_audio():
    smp_test = SampleTest()
    smp_test.set_is_audio()
    assert smp_test.is_audio()
    assert not smp_test.isnt_audio()


def test_antest_non_audio():
    smp_test = SampleTest()
    smp_test.set_isnt_audio()
    assert smp_test.isnt_audio()
    assert not smp_test.is_audio()


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
