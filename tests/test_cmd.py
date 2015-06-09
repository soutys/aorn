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

from aorn.cmd import (
    BUILTIN_METHODS,
    ARGS_SEP,
    METHODS_SEP,
    TEST_AUDIO,
    TEST_NON_AUDIO,
    CODE_PASS,
    CODE_FAIL,
    CODE_ROW,
    CODE_ERR,
    cmd_main,
    main,
)
from aorn.samplesstore import STDIN_FILE, SamplesStore

from tests.generators import synth_complex, synth_noise


def test_no_args():
    try:
        main()
        assert False
    except SystemExit as exc:
        assert exc.args[0] == CODE_ERR

    try:
        cmd_main([])
        assert False
    except SystemExit as exc:
        assert exc.args[0] == CODE_ERR


def test_bad_param():
    try:
        cmd_main(['--nonexistent-param'])
        assert False
    except SystemExit as exc:
        assert exc.args[0] == CODE_ERR


def test_help_only():
    try:
        cmd_main(['--help'])
        assert False
    except SystemExit as exc:
        assert exc.args[0] == CODE_PASS


def test_cmd_methods_info_ok():
    try:
        cmd_main(['--methods', METHODS_SEP.join(BUILTIN_METHODS),
            '--methods-info'])
        assert False
    except SystemExit as exc:
        assert exc.args[0] == CODE_PASS


def test_cmd_methods_info_fail():
    try:
        cmd_main(['--methods', 'nonex_mod.nonex_class', '--methods-info'])
        assert False
    except SystemExit as exc:
        assert exc.args[0] == CODE_ERR


def test_cmd_methods_bad_method_name():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_complex(freqs=[440], coefs=[1], datasize=data_sz, fname=tmp.name)

    try:
        cmd_main(['--methods', 'nonex_mod.nonex_class', '--test-what',
            TEST_AUDIO, '--filename', tmp.name])
        assert False
    except SystemExit as exc:
        assert exc.args[0] == CODE_ERR

    try:
        cmd_main(['--methods', 'aorn.methods.nonex_class', '--test-what',
            TEST_AUDIO, '--filename', tmp.name])
        assert False
    except SystemExit as exc:
        assert exc.args[0] == CODE_ERR


def test_cmd_methods_bad_method_args():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_complex(freqs=[440], coefs=[1], datasize=data_sz, fname=tmp.name)

    try:
        cmd_main(['--methods', 'aorn.methods.thr', '--test-what',
            TEST_AUDIO, '--filename', tmp.name])
        assert False
    except RuntimeError as exc:
        pass

    try:
        cmd_main(['--methods', 'aorn.methods.thr:', '--test-what',
            TEST_AUDIO, '--filename', tmp.name])
        assert False
    except (RuntimeError, ValueError) as exc:
        pass


def test_cmd_method_audio_test_pass():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_complex(freqs=[440], coefs=[1], datasize=data_sz, fname=tmp.name)

    try:
        cmd_main(['--methods', 'aorn.methods.thr:0.1', '--test-what',
            TEST_AUDIO, '--filename', tmp.name])
        assert False
    except SystemExit as exc:
        assert exc.args[0] == CODE_PASS


def test_cmd_method_audio_test_fail():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_complex(freqs=[440], coefs=[1], datasize=data_sz, fname=tmp.name)

    try:
        cmd_main(['--methods', 'aorn.methods.thr:0.9', '--test-what',
            TEST_AUDIO, '--filename', tmp.name])
        assert False
    except SystemExit as exc:
        assert exc.args[0] == CODE_FAIL


def test_cmd_method_non_audio_test_pass():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_noise(coef=2.0, datasize=data_sz, fname=tmp.name)

    try:
        cmd_main(['--methods', 'aorn.methods.zcs:0.2', '--test-what',
            TEST_NON_AUDIO, '--filename', tmp.name])
        assert False
    except SystemExit as exc:
        assert exc.args[0] == CODE_PASS


def test_cmd_method_non_audio_test_fail():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_complex(freqs=[440, 330, 1300, 3000, 300, 120],
        coefs=[1, 1, 1, 1, 1, 1], datasize=data_sz, fname=tmp.name)

    try:
        cmd_main(['--methods', 'aorn.methods.zcs:0.2', '--test-what',
            TEST_NON_AUDIO, '--filename', tmp.name])
        assert False
    except SystemExit as exc:
        assert exc.args[0] == CODE_FAIL


def test_cmd_method_test_row():
    tmp = NamedTemporaryFile(delete=True, prefix='sample_')
    data_sz = 10000
    synth_noise(coef=2.0, datasize=data_sz, fname=tmp.name)

    try:
        cmd_main(['--methods', 'aorn.methods.thr:0.2,aorn.methods.zcs:0.2',
            '--test-what', TEST_NON_AUDIO, '--filename', tmp.name])
        assert False
    except SystemExit as exc:
        assert exc.args[0] == CODE_ROW


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
