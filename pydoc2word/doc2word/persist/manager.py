# -*- coding: utf-8 -*-

from doc2word.persist.models import Stock
from doc2word import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import functools

# initialize DB connection
engine = create_engine(settings.DB_CONN_URL)
DBSession = sessionmaker(bind=engine)


def aop_session(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sess = DBSession()
        try:
            kwargs['session'] = sess
            rtn = func(*args, **kwargs)
            sess.commit()
        except Exception, e:
            sess.rollback()
            raise RuntimeError('function error: %s' % func.__name__, e)
        finally:
            sess.close()
        return rtn

    return wrapper


class StockMgr(object):
    @aop_session
    def add_stock(self, stock, session=None):
        if not isinstance(stock, Stock):
            raise TypeError('Invalid Stock parameter: ' + type(stock))
        session.add(stock)
