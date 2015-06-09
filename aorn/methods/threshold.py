# -*- coding: utf-8 -*-

'''Threshold test method module
'''

from __future__ import with_statement, division, absolute_import, print_function

from aorn.methods.antest import ANTest
from aorn.samplesstore import SAMPLE_MIN, SAMPLE_MAX


THR_MAX = min(abs(SAMPLE_MIN), abs(SAMPLE_MAX))


class Threshold(ANTest):
    '''Threshold test method class
    '''
    __doc__ = '''Detects audio by thresholding samples
    Params:
        threshold level - open range: 1...{} (or 0.0...1.0 as percent values)
    '''.format(THR_MAX - 1)

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        if kwargs.get('dry_run'):
            return
        if not args:
            raise RuntimeError('No threshold value param')
        self.level = float(args[0])
        if 0.0 < self.level < 1.0:
            self.level *= THR_MAX
        if not 0 < self.level < THR_MAX:
            raise RuntimeError('Bad threshold value. Got: {!r},' \
                ' valid: (1, {}) or (0.0, 1.0)'.format(self.level, THR_MAX - 1))


    def analyze(self, samples_store):
        '''
        '''
        if [sample for sample in samples_store.get_samples()
                if abs(sample) >= self.level]:
            return self.set_is_audio()
        self.set_isnt_audio()


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
