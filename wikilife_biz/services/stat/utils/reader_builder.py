# coding=utf-8

from wikilife_biz.services.stat.settings import READERS


class ReaderBuilderException(Exception):
    pass


class ReaderBuilder(object):

    def __init__(self, logger, daos):
        self._logger = logger
        self._daos = daos

    def build_reader(self, reader_class_fullname):
        ReaderClass = self._get_class(reader_class_fullname)
        reader = ReaderClass(self._logger, self._daos)

        return reader

    def build_reader_dict(self, reader_class_fullname_list=READERS):
        readers = {}

        for reader_class_fullname in reader_class_fullname_list:
            reader = self.build_reader(reader_class_fullname[1])
            readers[str(reader_class_fullname[0])] = reader

        return readers

    def _get_class(self, kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)

        for comp in parts[1:]:
            m = getattr(m, comp)

        return m
