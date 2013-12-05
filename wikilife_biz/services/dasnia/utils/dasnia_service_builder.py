# coding=utf-8

from wikilife_biz.services.dasnia.dasnia_service import DasniaService
from wikilife_biz.services.dasnia.singly.singly_delegate import SinglyDelegate
from wikilife_biz.services.dasnia.singly.singly_parsers import SinglyParsers
from wikilife_biz.utils.base_service_builder import BaseServiceBuilder


class DasniaServiceBuilder(BaseServiceBuilder):

    def build_dasnia_service(self, log_service):
        user_services_dao = self._dao_bldr.build_user_services_dao()
        dasnia_settings = self._settings["DASNIA_SETTINGS"]
        singly_delegate = SinglyDelegate(self._logger, dasnia_settings["singly"])
        meta_dao = self._dao_bldr.build_live_meta_dao()
        singly_parsers = SinglyParsers(meta_dao)
        return DasniaService(self._logger, dasnia_settings, user_services_dao, singly_delegate, singly_parsers, log_service)
