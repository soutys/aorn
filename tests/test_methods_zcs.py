# -*- coding: utf-8 -*-

'''Zero-crossings method module tests
'''

from __future__ import with_statement, division, absolute_import, print_function

from tempfile import NamedTemporaryFile

from aorn.methods import zcs
from aorn.methods.antest import ANTest
from aorn.samplesstore import SamplesStore

from tests.generators import synth_complex, synth_noise


def test_methods_zcs_init_dry_run():
    assert issubclass(zcs, ANTest)
    tester = zcs(dry_run=True)
    assert tester.is_audio() is None
    assert tester.isnt_audio() is None


def test_methods_zcs_init_no_args():
    try:
        zcs()
        assert False
    except RuntimeError:
        pass


def test_methods_zcs_init_float_level():
    zcs(0.5)


def test_methods_zcs_init_bad_float_level():
    try:
        zcs(0.0)
        assert False
    except RuntimeError:
        pass
    try:
        zcs(1.0)
        assert False
    except RuntimeError:
        pass


def test_methods_zcs_analyze_audio_ok():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_complex(freqs=[440, 330, 1300, 3000, 300, 120],
        coefs=[1, 1, 1, 1, 1, 1], datasize=data_sz, fname=tmp.name)

    samples_store = SamplesStore()
    samples_store.load_samples(tmp.name)
    assert samples_store.get_samples() is not None
    assert len(samples_store.get_samples()) == data_sz

    tester = zcs(0.2)
    tester.analyze(samples_store)
    assert tester.is_audio()


def test_methods_zcs_analyze_audio_fail():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_noise(coef=2.0, datasize=data_sz, fname=tmp.name)

    samples_store = SamplesStore()
    samples_store.load_samples(tmp.name)
    assert samples_store.get_samples() is not None
    assert len(samples_store.get_samples()) == data_sz

    tester = zcs(0.2)
    tester.analyze(samples_store)
    assert not tester.is_audio()


def test_methods_zcs_analyze_non_audio_ok():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_noise(coef=2.0, datasize=data_sz, fname=tmp.name)

    samples_store = SamplesStore()
    samples_store.load_samples(tmp.name)
    assert samples_store.get_samples() is not None
    assert len(samples_store.get_samples()) == data_sz

    tester = zcs(0.2)
    tester.analyze(samples_store)
    assert tester.isnt_audio()


def test_methods_zcs_analyze_non_audio_fail():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_complex(freqs=[440, 330, 1300, 3000, 300, 120],
        coefs=[1, 1, 1, 1, 1, 1], datasize=data_sz, fname=tmp.name)

    samples_store = SamplesStore()
    samples_store.load_samples(tmp.name)
    assert samples_store.get_samples() is not None
    assert len(samples_store.get_samples()) == data_sz

    tester = zcs(0.2)
    tester.analyze(samples_store)
    assert not tester.isnt_audio()


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
