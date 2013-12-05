# coding=utf-8

from wikilife_biz.services.dasnia.parsers.fitbit import Fitbit
from wikilife_biz.services.dasnia.parsers.run_keeper import RunKeeper
from wikilife_biz.services.dasnia.parsers.withings import Withings
from wikilife_biz.services.dasnia.parsers.zeo import Zeo


class SinglyParsers(object):

    _parsers = None

    def __init__(self, meta_dao):
        self._parsers = {}
        self._parsers["Fitbit"] = Fitbit(meta_dao)
        self._parsers["RunKeeper Health Graph"] = RunKeeper(meta_dao)
        self._parsers["Withings"] = Withings(meta_dao)
        self._parsers["zeo"] = Zeo(meta_dao)

    def get_parser(self, service_name):
        return self._parsers.get(service_name, None)
