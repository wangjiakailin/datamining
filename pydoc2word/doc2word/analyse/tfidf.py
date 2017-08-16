# -*- coding: utf-8 -*-

from jieba.analyse.tfidf import TFIDF
from operator import itemgetter


class TFIDFP(TFIDF):
    def __init__(self, idf_path=None, debug=False):
        super(TFIDFP, self).__init__(idf_path=idf_path)
        self._debug = debug

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, debug):
        self._debug = debug

    def extract_tags_with_time_decay(self, weight_sentence_dict, topK=20, withWeight=False, allowPOS=(),
                                     withFlag=False):
        """
        Extract keywords from time_decay_weight-sentence dict using TF-IDF algorithm.
        Parameter:
            - weight_sentence_dict: time_decay_weight-sentence dict.
            - topK: return how many top keywords. `None` for all possible words.
            - withWeight: if True, return a list of (word, weight);
                          if False, return a list of words.
            - allowPOS: the allowed POS list eg. ['ns', 'n', 'vn', 'v','nr'].
                        if the POS of w is not in this list,it will be filtered.
            - withFlag: only work with allowPOS is not empty.
                        if True, return a list of pair(word, weight) like posseg.cut
                        if False, return a list of words
        """

        if allowPOS:
            allowPOS = frozenset(allowPOS)
            tokenizer_cutter = self.postokenizer
        else:
            tokenizer_cutter = self.tokenizer

        print("----> debug", self._debug)

        debug_dict = None
        if self._debug:
            debug_dict = {'wordStatistic': {}, 'allowPOS': list(allowPOS), 'topK': topK}

        freq = {}
        for time_decay_weight, sentence in weight_sentence_dict.iteritems():
            words = tokenizer_cutter.cut(sentence)
            for w in words:
                if allowPOS:
                    if w.flag not in allowPOS:
                        continue
                    elif not withFlag:
                        w = w.word
                wc = w.word if allowPOS and withFlag else w
                if len(wc.strip()) < 2 or wc.lower() in self.stop_words:
                    continue
                freq[w] = freq.get(w, 0.0) + time_decay_weight
                if self._debug:
                    debug_word_statistic = debug_dict['wordStatistic']
                    debug_word_statistic[wc] = debug_statistic = debug_word_statistic.get(wc, {})
                    debug_statistic['decay_tc'] = debug_statistic.get('decay_tc', 0.0) + time_decay_weight
                    debug_statistic['tc'] = debug_statistic.get('tc', 0.0) + 1.0
                    if 'idf' not in debug_statistic:
                        debug_statistic['idf'] = debug_statistic.get('idf', self.idf_freq.get(wc, self.median_idf))
                    if 'w' not in debug_statistic:
                        debug_statistic['w'] = wc

        total = sum(freq.values())

        if self._debug:
            debug_dict['total'] = sum(
                [debug_statistic['tc'] for debug_statistic in debug_dict['wordStatistic'].itervalues()])
            debug_dict['total_decay'] = total
            debug_dict['median_idf'] = self.median_idf

        for k in freq:
            kw = k.word if allowPOS and withFlag else k
            freq[k] *= self.idf_freq.get(kw, self.median_idf) / total

            if self._debug:
                debug_word_statistic = debug_dict['wordStatistic']
                debug_statistic = debug_word_statistic[kw]
                debug_statistic['decay_tfidf'] = freq[k]
                debug_statistic['tfidf'] = debug_statistic['tc'] * debug_statistic['idf'] / debug_dict['total']

        if withWeight:
            tags = sorted(freq.items(), key=itemgetter(1), reverse=True)
        else:
            tags = sorted(freq, key=freq.__getitem__, reverse=True)

        if self._debug:
            debug_dict['wordStatistic'] = sorted(debug_dict['wordStatistic'].iteritems(),
                                                 key=lambda t: t[1]['decay_tfidf'], reverse=True)

        if topK:
            if self._debug:
                debug_dict['wordStatistic'] = [v for (k, v) in debug_dict['wordStatistic'][:int(topK * 1.2)]]

            return debug_dict, tags[:topK]
        else:
            return debug_dict, tags
