# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

from doc2word import settings
from doc2word import analyse

import sys
import os
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')


def train_idf(root_path_list, target=None):
    _check_root_path_list(root_path_list)

    idf_loader = analyse.IDFLoader(settings.DEFAULT_EXTRA_IDF)
    idf_freq, median_idf = idf_loader.get_idf()

    # Document-term matrix, element [i, j], frequency of term j in document i
    count_vectorizer = CountVectorizer()
    tfidf_transformer = TfidfTransformer()

    dt_mat = count_vectorizer.fit_transform(_do_cut(root_path_list))
    tfidf_transformer.fit(dt_mat)
    term = count_vectorizer.get_feature_names()
    for i in range(len(term)):
        idf_freq[term[i]] = tfidf_transformer.idf_[i] - 1

    if target is None:
        target = '%s.%s' % (settings.DEFAULT_EXTRA_IDF, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))

    with open(target, 'w') as f:
        for k, v in idf_freq.iteritems():
            f.write('%s %s\n' % (k, v))


def _check_root_path_list(root_path_list):
    if not isinstance(root_path_list, list) or not root_path_list:
        raise TypeError("empty list of root path is not allowed!")

    for root_path in root_path_list:
        if not os.path.isdir(root_path):
            raise ValueError("root path [%s] is not directory!" % root_path)

    list_len = len(root_path_list)
    for i in range(list_len):
        curr_path = root_path_list[i]
        for j in range(i + 1, list_len):
            path = root_path_list[j]
            if curr_path in path or path in curr_path:
                raise ValueError("there is inclusive relationship between root path [%s] and [%s]."
                                 % (curr_path, root_path))


def _do_cut(root_path_list):
    for root_path in root_path_list:
        for dir_path, _, filenames in os.walk(root_path):
            for filename in filenames:
                canonical_filename = os.path.join(dir_path, filename)
                with open(canonical_filename, 'rb') as f:
                    seg_list = analyse.cut(f.read())
                    if seg_list:
                        yield " ".join(seg_list)
