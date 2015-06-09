# -*- coding: utf-8 -*-

'''Threshold method module tests
'''

from __future__ import with_statement, division, absolute_import, print_function

from tempfile import NamedTemporaryFile

from aorn.methods import thr
from aorn.methods.antest import ANTest
from aorn.samplesstore import SAMPLE_MIN, SAMPLE_MAX, SamplesStore

from tests.generators import synth_complex


def test_methods_thr_init_dry_run():
    assert issubclass(thr, ANTest)
    tester = thr(dry_run=True)
    assert tester.is_audio() is None
    assert tester.isnt_audio() is None


def test_methods_thr_init_no_args():
    try:
        thr()
        assert False
    except RuntimeError:
        pass


def test_methods_thr_init_int_level():
    thr(1)
    thr(int(abs(SAMPLE_MAX) / 2))
    thr(min(abs(SAMPLE_MIN), abs(SAMPLE_MAX)) - 1)


def test_methods_thr_init_float_level():
    thr(0.5)


def test_methods_thr_init_bad_int_level():
    try:
        thr(SAMPLE_MAX * 2)
        assert False
    except RuntimeError:
        pass
    try:
        thr(SAMPLE_MIN * 2)
        assert False
    except RuntimeError:
        pass


def test_methods_thr_init_bad_float_level():
    try:
        thr(0.0)
        assert False
    except RuntimeError:
        pass


def test_methods_thr_analyze_audio_ok():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_complex(freqs=[440], coefs=[4], datasize=data_sz, fname=tmp.name)

    samples_store = SamplesStore()
    samples_store.load_samples(tmp.name)
    assert samples_store.get_samples() is not None
    assert len(samples_store.get_samples()) == data_sz

    tester = thr(0.2)
    tester.analyze(samples_store)
    assert tester.is_audio()


def test_methods_thr_analyze_audio_fail():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_complex(freqs=[440], coefs=[0.1], datasize=data_sz, fname=tmp.name)

    samples_store = SamplesStore()
    samples_store.load_samples(tmp.name)
    assert samples_store.get_samples() is not None
    assert len(samples_store.get_samples()) == data_sz

    tester = thr(0.2)
    tester.analyze(samples_store)
    assert not tester.is_audio()


def test_methods_thr_analyze_non_audio_ok():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_complex(freqs=[440], coefs=[0.1], datasize=data_sz, fname=tmp.name)

    samples_store = SamplesStore()
    samples_store.load_samples(tmp.name)
    assert samples_store.get_samples() is not None
    assert len(samples_store.get_samples()) == data_sz

    tester = thr(0.2)
    tester.analyze(samples_store)
    assert tester.isnt_audio()


def test_methods_thr_analyze_non_audio_fail():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_complex(freqs=[440], coefs=[4], datasize=data_sz, fname=tmp.name)

    samples_store = SamplesStore()
    samples_store.load_samples(tmp.name)
    assert samples_store.get_samples() is not None
    assert len(samples_store.get_samples()) == data_sz

    tester = thr(0.2)
    tester.analyze(samples_store)
    assert not tester.isnt_audio()


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
