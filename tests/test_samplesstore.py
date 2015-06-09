# -*- coding: utf-8 -*-

'''Samples storage module tests
'''

from __future__ import with_statement, division, absolute_import, print_function

import sys
from tempfile import NamedTemporaryFile
try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

from aorn.samplesstore import STDIN_FILE, SamplesStore

from tests.generators import synth_complex


def test_samplesstore_init():
    samples_store = SamplesStore()
    assert samples_store.get_samples() is None


def test_samplesstore_load_file_empty():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    samples_store = SamplesStore()
    samples_store.load_samples(tmp.name)
    assert samples_store.get_samples() is not None
    assert len(samples_store.get_samples()) == 0


def test_samplesstore_load_stdin_empty():
    old_stdin = sys.stdin
    sys.stdin = StringIO(None)
    samples_store = SamplesStore()
    samples_store.load_samples(STDIN_FILE)
    sys.stdin = old_stdin
    assert samples_store.get_samples() is not None
    assert len(samples_store.get_samples()) == 0


def test_samplesstore_load_file_somedata():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_complex(freqs=[440], coefs=[1], datasize=data_sz, fname=tmp.name)

    samples_store = SamplesStore()
    samples_store.load_samples(tmp.name)
    assert samples_store.get_samples() is not None
    assert len(samples_store.get_samples()) == data_sz


def test_samplesstore_load_stdin_somedata():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_complex(freqs=[440], coefs=[1], datasize=data_sz, fname=tmp.name)

    old_stdin = sys.stdin
    sys.stdin = open(tmp.name, 'rb')
    samples_store = SamplesStore()
    samples_store.load_samples(STDIN_FILE)
    sys.stdin = old_stdin
    assert samples_store.get_samples() is not None
    assert len(samples_store.get_samples()) == data_sz


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
