# -*- coding: utf-8 -*-

'''Samples generators
'''

from __future__ import with_statement, division, absolute_import, print_function

from array import array
from math import pi, sin
from random import SystemRandom


# http://stackoverflow.com/a/5174008
def synth_complex(freqs=None, coefs=None, datasize=0, fname=''):
    '''Generates sound samples of given frequency/amplitude pattern
    '''
    if not (freqs and coefs and datasize and fname):
        raise ValueError('empty param(s): {!r}'.format(repr((freqs, coefs,
            datasize, fname))))
    if len(freqs) != len(coefs):
        raise ValueError('freqs / coefs number mismatch')
    fc_items = list(zip(freqs, coefs))
    sample_freq = 44100.0
    amplitude = 8000.0
    const = 2 * pi / sample_freq
    boost = amplitude / 2.0
    samples = array('h')
    for sidx in range(datasize):
        sample = 0
        for freq, coef in fc_items:
            sample += coef * sin(sidx * freq * const)
        samples.append(int(sample * boost))
    with open(fname, 'wb') as fd_obj:
        samples.tofile(fd_obj)


def synth_noise(coef=0, datasize=0, fname=''):
    '''Generates noise samples
    '''
    if not (coef and datasize and fname):
        raise ValueError('empty param(s): {!r}'.format(repr((coef, datasize,
            fname))))
    amplitude = 8000.0
    boost = coef * amplitude / 2.0
    samples = array('h')
    rand = SystemRandom()
    for _ in range(datasize):
        samples.append(int(rand.uniform(-1, 1) * boost))
    with open(fname, 'wb') as fd_obj:
        samples.tofile(fd_obj)


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
