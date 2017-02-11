# -*- coding: utf-8 -*-

'''Test method module: threshold with optional low-pass filtering
'''

from __future__ import with_statement, division, absolute_import, print_function

from aorn.methods.antest import ANTest
from aorn.samplesstore import SAMPLE_MIN, SAMPLE_MAX


THR_MAX = min(abs(SAMPLE_MIN), abs(SAMPLE_MAX))
MIN_WINDOW_SZ = 1


class Threshold(ANTest):
    '''Threshold with optional low-pass filtering test method class
    '''
    __doc__ = '''Detects audio by thresholding (optionally low-passed) samples
    Params:
        threshold level - open range: 1...{} (or 0.0...1.0 as percent values)
        probes number - moving average window size (1...N)
    '''.format(THR_MAX - 1)

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        if kwargs.get('dry_run'):
            return
        if not args:
            raise RuntimeError('No threshold / window size value params')
        self.level = float(args[0])
        if 0.0 < self.level < 1.0:
            self.level *= THR_MAX
        if not 0 < self.level < THR_MAX:
            raise RuntimeError('Bad threshold value. Got: {!r},'
                ' valid: (1, {}) or (0.0, 1.0)'.format(self.level, THR_MAX - 1))
        self.window_sz = MIN_WINDOW_SZ
        self.overlap_sz = 0
        if len(args) > 1:
            self.window_sz = int(args[1])
        if len(args) > 2:
            self.overlap_sz = int(args[2])
        if self.window_sz < MIN_WINDOW_SZ:
            raise RuntimeError('Bad window size value. Got: {!r},'
                ' valid: ({}, <probes #>)'.format(self.window_sz,
                MIN_WINDOW_SZ))
        if not 0 <= self.overlap_sz <= (self.window_sz - 1):
            raise RuntimeError('Bad overlap size value. Got: {!r},'
                ' valid: {}...{}'.format(self.overlap_sz, 0,
                self.window_sz - 1))


    def avg_samples(self, samples):
        '''Iterate over original samples averaged using moving window
        '''
        if self.window_sz == 1:
            for sample in samples:
                yield sample
            return
        samples_num = len(samples)
        for index in range(0, samples_num, self.window_sz - self.overlap_sz):
            if index + self.window_sz <= samples_num:
                part = samples[index:index + self.window_sz]
                yield sum(part) / self.window_sz


    def analyze(self, samples_store):
        if [sample for sample in self.avg_samples(
                samples_store.get_samples()) if abs(sample) >= self.level]:
            return self.set_is_audio()
        self.set_isnt_audio()


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
