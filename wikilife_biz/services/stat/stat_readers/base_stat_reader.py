# coding=utf-8


class BaseStatReader(object):
    """
    Base Stat Reader
    """
    _logger = None
    _daos = None

    def __init__(self, logger, daos):
        self._logger = logger
        self._daos = daos

    def read_stat(self, **kwargs):
        raise NotImplementedError()
