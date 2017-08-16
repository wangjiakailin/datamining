# -*- coding: utf-8 -*-

from doc2word.persist.manager import StockMgr
from doc2word.persist.models import Stock

import datetime

stock = Stock()
stock.stock_code = '000001'
stock.stock_url = 'http://stock.000001'
stock.stock_keyword_list = 'Just do IT.'
stock.word_weight_list = '1.2 2.2 0.11'
stock.version = 1
stock.create_datetime = datetime.datetime.now()
stock.extract_time = datetime.datetime.now()

stk_mgr = StockMgr()
stk_mgr.add_stock(stock)
