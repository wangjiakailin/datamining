# -*- coding: utf-8 -*-

import os
import fnmatch
import jieba
import jieba.analyse
from jieba.analyse.tfidf import IDFLoader

try:
    from jieba.analyse.analyzer import ChineseAnalyzer
except ImportError:
    pass

from doc2word import settings
from doc2word.analyse.tfidf import TFIDFP

IDFLoader = IDFLoader
default_tfidf = TFIDFP()


def cut(sentence, cut_all=False, hmm=True):
    return jieba.cut(sentence, cut_all=cut_all, HMM=hmm)


def extract_tags(content, top_k, allow_pos=('ns', 'n', 'vn', 'v', 'nr')):
    return default_tfidf.extract_tags(content, topK=top_k, allowPOS=allow_pos, withWeight=True, withFlag=False)


def extract_tags_with_time_decay(weight_sentence_dict, top_k, allow_pos=('ns', 'n', 'vn', 'v', 'nr')):
    return default_tfidf.extract_tags_with_time_decay(weight_sentence_dict, topK=top_k, allowPOS=allow_pos,
                                                      withWeight=True, withFlag=False)


def set_stop_words(path):
    default_tfidf.set_stop_words(path)


def set_idf_path(path):
    default_tfidf.set_idf_path(path)


def enable_parallel(n):
    jieba.disable_parallel()
    #jieba.enable_parallel(n)


def load_userdict(path):
    jieba.load_userdict(path)


def find_latest_dict(dict_prefix):
    base_dir = os.path.dirname(dict_prefix)
    dict_name = os.path.basename(dict_prefix)
    listed_dict = fnmatch.filter(os.listdir(base_dir), "%s*" % dict_name)
    listed_dict.sort(reverse=True)
    return os.path.join(base_dir, listed_dict[0])


def use_default_analyse_settings():
    # Default DICT settings
    enable_parallel(settings.DEFAULT_PARALLEL)
    # if main dict set, use it, if not, use jieba default dict.
    if settings.DEFAULT_MAIN_DICT:
        jieba.set_dictionary(settings.DEFAULT_MAIN_DICT)

    load_userdict(settings.DEFAULT_USER_DICT)
    set_idf_path(find_latest_dict(settings.DEFAULT_EXTRA_IDF))
    set_stop_words(settings.DEFAULT_EXTRA_STOP_WORDS)
