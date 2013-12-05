# coding=utf-8

from wikilife_biz.services.stat.utils.reader_builder import ReaderBuilder
import sys
import traceback


class StatServiceException(Exception):
    pass


class StatService(object):

    """
    Public Business Service
    """

    _logger = None
    _user_srv = None

    def __init__(self, logger, daos):
        self._logger = logger
        self.readers = ReaderBuilder(logger, daos).build_reader_dict()

    def get_stat_by_id(self, stat_id, **kwargs):

        try:
            stat_reader = self.readers[str(stat_id)]
            return stat_reader.read_stat(**kwargs)
        except Exception, e:
            exc_traceback = sys.exc_info()[2]
            traceback.print_tb(exc_traceback, limit=3, file=sys.stdout)
            raise StatServiceException(e)
