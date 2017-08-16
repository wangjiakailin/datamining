# -*- coding: utf-8 -*-

from doc2word.stock_workers import LocalStockWorker
from doc2word.extractor.doc_extractors import LocalDocExtractor
from doc2word.debug import Debug
from doc2word import settings
from doc2word import analyse

import json

Debug.debug(debug_flag=True)

analyse.use_default_analyse_settings()

doc_extractor = LocalDocExtractor(top_k=100, allow_pos=('ns', 'n', 'vn', 'v', 'nr'))
stock_worker = LocalStockWorker(settings.DEFAULT_ROOT, doc_extractor=doc_extractor, num_latest_days=2)

stock_tags = stock_worker.work()

for stock_tag in stock_tags:
    print("stock code: %s" % stock_tag.stock_code)
    for tag, weight in stock_tag.tags:
        print(" |- %s %.8f" % (tag, weight))

    if stock_tag.statistic:
        print('--- JSON:\n')
        print(json.dumps(stock_tag.statistic))
