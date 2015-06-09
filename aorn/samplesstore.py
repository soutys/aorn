# -*- coding: utf-8 -*-

'''Samples storage module
'''

from __future__ import with_statement, division, absolute_import, print_function

import sys
from array import array


STDIN_FILE = '-'
BUF_SZ = 8192
SAMPLE_WIDTH = 2
SAMPLE_MIN = - (2 ** 15)
SAMPLE_MAX = 2 ** 15 - 1
SAMPLES_NUM = 1024 ** 2


class SamplesStore(object):
    '''Samples storage class
    '''

    def __init__(self):
        self._samples = None


    def load_samples(self, filename):
        '''Loads samples from file or STDIN
        '''
        self._samples = array('h')
        if filename and filename != STDIN_FILE:
            fd_obj = open(filename, 'rb')
            try:
                self._samples.fromfile(fd_obj, SAMPLES_NUM)
            except EOFError:
                pass
            if fd_obj and hasattr(fd_obj, 'close'):
                fd_obj.close()
        else:
            fd_obj = sys.stdin
            if hasattr(fd_obj, 'buffer'): # pragma: no cover
                fd_obj = fd_obj.buffer
            str_obj = True
            while str_obj:
                str_obj = fd_obj.read(BUF_SZ)
                self._samples.fromstring(str_obj)


    def get_samples(self):
        '''Returns samples
        '''
        return self._samples


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
