# coding=utf-8


class BaseServiceBuilder(object):

    _settings = None
    _logger = None
    _dao_bldr = None

    def __init__(self, settings, logger, dao_builder):
        self._settings = settings
        self._logger = logger
        self._dao_bldr = dao_builder
        self.initialize()

    def initialize(self):
        pass
