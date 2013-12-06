# coding=utf-8

from wikilife_biz.services.stat.stat_service import StatService
from wikilife_biz.services.stat.utils.biz_daos import BizDAOs


class StatServiceBuilder(object):

    _settings = None
    _logger = None
    _dao_bldr = None

    def __init__(self, settings, logger, dao_builder):
        self._settings = settings
        self._logger = logger
        self._dao_bldr = dao_builder

    def _build_daos(self):
        daos = BizDAOs()
        daos.meta_dao = self._dao_bldr.build_live_meta_dao()
        daos.user_dao = self._dao_bldr.build_user_dao()
        daos.profile_dao = self._dao_bldr.build_profile_dao()
        daos.log_dao = self._dao_bldr.build_log_dao()
        daos.generic_dao = self._dao_bldr.build_generic_dao()
        daos.aggregation_dao = self._dao_bldr.build_aggregation_dao()
        daos.aggregation_node_dao = self._dao_bldr.build_aggregation_node_dao()
        daos.user_option_last_log_dao = self._dao_bldr.build_user_option_last_log_dao()
        return daos

    def build_stat_service(self):
        daos = self._build_daos()
        return StatService(self._logger, daos)
