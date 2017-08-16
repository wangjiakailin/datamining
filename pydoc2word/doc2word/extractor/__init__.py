# -*- coding: utf-8 -*-


class DocExtractor(object):
    def extract_tags(self, *args, **kwargs):
        raise NotImplementedError

    def extract_tags_with_time_decay(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def top_k(self):
        return self._top_k

    @property
    def allow_pos(self):
        return self._allow_pos
