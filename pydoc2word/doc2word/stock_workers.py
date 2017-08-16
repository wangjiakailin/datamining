# -*- coding: utf-8 -*-
import os
import re
import fnmatch
import time


STOCK_CODE_PATTERN = "[0-9][0-9][0-9][0-9][0-9][0-9]"
DATE_PATTERN = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]"
FILENAME_RE = r"^\d{4}-\d{2}-\d{2}_[0-9a-fA-F]+\.txt$"
DATE_MASK = '%Y-%m-%d'
BASE_LINE = time.mktime(time.strptime('2000-01-01', '%Y-%m-%d'))


class StockTags(object):
    def __init__(self, stock_code, tags, statistic=None):
        self._stock_code = stock_code
        self._tags = tags
        self._statistic = statistic

    def __iter__(self):
        return iter((self._stock_code, self._tags))

    def __eq__(self, other):
        return isinstance(other, StockTags) and self._stock_code == other.stock_code and self._tags == other.tags

    def __hash__(self):
        return hash(self._stock_code)

    @property
    def stock_code(self):
        return self._stock_code

    @property
    def tags(self):
        return self._tags

    @property
    def statistic(self):
        return self._statistic


def _file_name_info(file_name):
    date_str, hash_part = file_name.split('_')
    return date_str, hash_part.split('.')[0]


def _doc_filter(title):
    title_utf8 = title.decode('utf-8')
    return re.match(ur'^[\u4e00-\u9fa5]+\(\d{6}\)融资融券信息\(.*\).*$', title_utf8) or \
           re.match(ur'^[\u4e00-\u9fa5]+\(\d{6}\)大宗交易数据一览\(.*\).*$', title_utf8) or \
           re.match(ur'^[\u4e00-\u9fa5]+\(\d{6}\)龙虎榜数据\(.*\).*$', title_utf8) or \
           re.match(ur'^[\u4e00-\u9fa5]+今日超大单流出排名第\d+名\(.*\).*$', title_utf8) or \
           re.match(ur'^[\u4e00-\u9fa5]+今日超大单流入排名第\d+名\(.*\).*$', title_utf8) or \
           re.match(ur'^[\u4e00-\u9fa5]+\(\d{6}\)高管持股数据一览\(.*\).*$', title_utf8)


class StockWorker(object):
    def work(self, *args, **kwargs):
        raise NotImplementedError


class LocalStockWorker(StockWorker):
    def __init__(self, root_path, doc_extractor, num_latest_days=2):
        if not os.path.isdir(root_path):
            raise Exception("doc2word: invalid root path: %s" % root_path)
        if not doc_extractor:
            raise Exception("doc2word: doc_extractor is null!")

        self._root_path = root_path
        self._doc_extractor = doc_extractor
        self._num_latest_days = num_latest_days

    def __do_work(self, stock_code):
        stock_root_path = os.path.join(self._root_path, stock_code)
        if not os.path.isdir(stock_root_path):
            raise Exception("doc2word: invalid stock root path: %s" % stock_root_path)
        listed_days = fnmatch.filter(os.listdir(stock_root_path), DATE_PATTERN)
        listed_days.sort(reverse=True)
        listed_days = listed_days[:self._num_latest_days]
        file_loaded = {}
        # content = ''
        # time_decay_weight-sentence dict
        weight_sentence_dict = {}
        max_timestamp = 0.0
        for day in listed_days:
            path = os.path.join(stock_root_path, day)
            if not os.path.isdir(path):
                continue
            for file_name in os.listdir(path):
                if not re.match(FILENAME_RE, file_name):
                    continue
                date_str, file_name_hash = _file_name_info(file_name)
                # avoid duplicate documents.
                if file_name_hash in file_loaded:
                    continue

                canonical_file_name = os.path.join(path, file_name)
                with open(canonical_file_name, 'rb') as f:
                    title = f.readline()
                    if _doc_filter(title):
                        # TODO add debug log: title
                        continue

                    bytes_read = f.read()
                    # content += bytes_read
                    timestamp = time.mktime(time.strptime(date_str, DATE_MASK))
                    weight_sentence_dict[timestamp] = weight_sentence_dict.get(timestamp, '') + bytes_read
                    file_loaded[file_name_hash] = 1
                    if max_timestamp < timestamp:
                        max_timestamp = timestamp

        # return self._doc_extractor.extract_tags(content=content)
        return self._doc_extractor.extract_tags_with_time_decay(
            weight_sentence_dict={(k - BASE_LINE) / (max_timestamp - BASE_LINE): v for k, v in weight_sentence_dict.iteritems()})

    def work(self):
        listed_stocks = fnmatch.filter(os.listdir(self._root_path), STOCK_CODE_PATTERN)
        for stock_code in listed_stocks:
            statistic, tags = self.__do_work(stock_code)
            yield StockTags(stock_code, tags, statistic=statistic)


class SparkStockWorker(StockWorker):
    def work(self):
        pass


class MR2StockWorker(StockWorker):
    def work(self):
        pass
