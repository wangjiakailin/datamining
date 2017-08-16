from doc2word import analyse
from doc2word.extractor import DocExtractor


class LocalDocExtractor(DocExtractor):
    def __init__(self, top_k, allow_pos, **kwargs):
        self._top_k = top_k
        self._allow_pos = allow_pos

    def extract_tags(self, content, *args, **kwargs):
        return analyse.extract_tags(content, top_k=self._top_k, allow_pos=self._allow_pos)

    def extract_tags_with_time_decay(self, weight_sentence_dict, *args, **kwargs):
        return analyse.extract_tags_with_time_decay(weight_sentence_dict, top_k=self._top_k, allow_pos=self._allow_pos)


class SparkDocExtractor(DocExtractor):
    def extract_tags(self, *args, **kwargs):
        pass

    def extract_tags_with_time_decay(self, *args, **kwargs):
        pass


class MR2DocExtractor(DocExtractor):
    def extract_tags(self, *args, **kwargs):
        pass

    def extract_tags_with_time_decay(self, *args, **kwargs):
        pass
