# -*- coding: utf-8 -*-

VERSION = '0.6.0'

DB_HOST = '10.25.24.52'
DB_PORT = 3306
DB_USER = 'nlp'
DB_PASS = '123456'
DB_NAME = 'nlp'
# DB driver: MySQL-python
DB_CONN_URL = 'mysql+mysqldb://%s:%s@%s:%d/%s?charset=utf8' % (DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)

DEFAULT_PARALLEL = 4

DEFAULT_USER_DICT = r'C:\work\stock_news\datamining\nlp_strategy\pydoc2word\extra_dict\user_dict.txt'

DEFAULT_EXTRA_STOP_WORDS =r'C:\work\stock_news\datamining\nlp_strategy\pydoc2word\extra_dict\stop_words.txt'

DEFAULT_EXTRA_IDF = r'C:\work\stock_news\datamining\nlp_strategy\pydoc2word\extra_dict\idf.txt.big'

DEFAULT_MODE = 'local'
#DEFAULT_ROOT = '/home/nlp/nlp/pydoc2word/test/stocks'
DEFAULT_ROOT = r'C:\work\stock_news\datamining\nlp_strategy\data\output_stock\stockInfo'

DEFAULT_MAIN_DICT = r'C:\work\stock_news\datamining\nlp_strategy\pydoc2word\extra_dict\dict.txt.big'

DEFAULT_TOP_K = 200
DEFAULT_ALLOW_POS = ('ns', 'n', 'vn', 'v', 'nr')
DEFAULT_NUM_LATEST_DAYS = 365
# DEFAULT_MIN_BYTES = '50k'

DEFAULT_REST_API_APP_PORT = 18080

