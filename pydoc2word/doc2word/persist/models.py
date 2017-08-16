# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Time, Text
from sqlalchemy.ext.declarative import declarative_base

# create base class
Base = declarative_base()


# create Stock class
class Stock(Base):
    # table name
    __tablename__ = 'tbl_stock'

    # table schema
    id = Column(Integer(), primary_key=True, autoincrement=True)
    stock_code = Column(String(11), nullable=False)
    stock_url = Column(String(200))
    stock_keyword_list = Column(String(4000))
    word_weight_list = Column(String(4000))
    version = Column(Integer())
    create_datetime = Column(Time(), nullable=False)
    extract_time = Column(Time(), nullable=False)
    statistics = Column(Text())
