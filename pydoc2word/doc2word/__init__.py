# -*- coding: utf-8 -*-

from doc2word import stock_workers
from doc2word.extractor import doc_extractors
from doc2word.persist.manager import StockMgr
from doc2word.persist.models import Stock

import datetime
import json


class Doc2wordMode(object):
    def __init__(self, func, doc_extractor, worker):
        self._doc_extractor = doc_extractor
        self._worker = worker
        self._func = func

    @property
    def func(self):
        return self._func

    @property
    def doc_extractor(self):
        return self._doc_extractor

    @property
    def worker(self):
        return self._worker


def __doc2word_local(doc2word_mode, num_latest_days, root_path, top_k, allow_pos):
    extract_time = datetime.datetime.now()
    stock_mgr = StockMgr()

    doc_extractor = doc2word_mode.doc_extractor(top_k, allow_pos=allow_pos)
    stock_worker = doc2word_mode.worker(root_path, doc_extractor, num_latest_days)
    stock_tags = stock_worker.work()

    for stock_tag in stock_tags:
        stock = Stock()
        stock.stock_code = stock_tag.stock_code
        stock.stock_keyword_list = ' '.join(t for t, w in stock_tag.tags)
        stock.word_weight_list = ' '.join('%.8f' % w for t, w in stock_tag.tags)
        stock.version = 1
        stock.create_datetime = datetime.datetime.now()
        stock.extract_time = extract_time
        stock.statistics = stock_tag.statistic if stock_tag.statistic is None else json.dumps(stock_tag.statistic)
        stock_mgr.add_stock(stock)


def __doc2word_spark(*args, **kwargs):
    pass


def __doc2word_mr2(*args, **kwargs):
    pass


supported_modes = {
    'local': Doc2wordMode(func=__doc2word_local, doc_extractor=doc_extractors.LocalDocExtractor,
                          worker=stock_workers.LocalStockWorker),
    'spark': Doc2wordMode(func=__doc2word_spark, doc_extractor=doc_extractors.SparkDocExtractor,
                          worker=stock_workers.SparkStockWorker),
    'mr2': Doc2wordMode(func=__doc2word_mr2, doc_extractor=doc_extractors.MR2DocExtractor,
                        worker=stock_workers.MR2StockWorker)
}


def doc2word(mode='local', *args, **kwargs):
    doc2word_mode = supported_modes[mode]
    internal_func = doc2word_mode.func
    internal_func(doc2word_mode=doc2word_mode, *args, **kwargs)
