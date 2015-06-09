# -*- coding: utf-8 -*-

'''Zero-crossing test method module
'''

from __future__ import with_statement, division, absolute_import, print_function

from aorn.methods.antest import ANTest


class ZeroCrossings(ANTest):
    '''Zero-crossings test method class
    '''
    __doc__ = '''Detects audio by thresholding a number of zero-crossings
    in samples set
    Params:
        threshold level - open range: 0.0...1.0
    '''

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        if kwargs.get('dry_run'):
            return
        if not args:
            raise RuntimeError('No threshold value param')
        self.level = float(args[0])
        if not 0.0 < self.level < 1.0:
            raise RuntimeError('Bad threshold value. Got: {!r},' \
                ' valid: (0.0, 1.0)'.format(self.level))


    def analyze(self, samples_store):
        samples_num = 0
        crossings = 0
        prev_smp = 0
        for smp in samples_store.get_samples():
            samples_num += 1
            if smp * prev_smp < 0:
                crossings += 1
            prev_smp = smp
        if crossings < self.level * samples_num:
            return self.set_is_audio()
        self.set_isnt_audio()


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
