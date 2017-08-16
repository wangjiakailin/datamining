# -*- coding: utf-8 -*-

from doc2word.analyse import default_tfidf


class Debug(object):

    _debug = False

    @staticmethod
    def debug(debug_flag=None):
        if debug_flag is None:
            return Debug._debug
        else:
            if debug_flag in (True, False):
                Debug._debug = debug_flag
                default_tfidf.debug = Debug._debug
                return Debug._debug
            else:
                return Debug._debug
