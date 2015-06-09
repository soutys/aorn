# -*- coding: utf-8 -*-

'''Generic test method module
'''

from __future__ import with_statement, division, absolute_import, print_function

from abc import ABCMeta, abstractmethod

import six


@six.add_metaclass(ABCMeta)
class ANTest(object):
    '''Generic test method class
    '''
    __doc__ = ''

    def __init__(self, *args, **kwargs):
        self._is_audio = None
        self._isnt_audio = None


    def get_doc(self):
        '''Returns method documentation (info)
        '''
        return self.__doc__


    def is_audio(self):
        '''Returns analyze result of audio-test
        '''
        if self._is_audio is not None:
            return self._is_audio
        if self._isnt_audio is not None:
            return not self._isnt_audio


    def isnt_audio(self):
        '''Returns analyze result of non-audio-test
        '''
        is_audio = self.is_audio()
        if is_audio is not None:
            return not is_audio


    def set_is_audio(self):
        '''Sets analyze result of audio-test
        '''
        self._is_audio = True


    def set_isnt_audio(self):
        '''Sets analyze result of non-audio-test
        '''
        self._isnt_audio = True


    @abstractmethod
    def analyze(self, samples_store):
        '''Analyzes samples
        '''
        raise NotImplementedError('Abstract method not overridden!')


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
