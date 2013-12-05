# coding=utf-8

from wikilife_biz.services.log.log_service import LogService
from wikilife_biz.services.log.global_stream_service import GlobalStreamService
from wikilife_utils.queue_publisher import QueuePublisher
from wikilife_biz.utils.base_service_builder import BaseServiceBuilder


class LogServiceBuilder(BaseServiceBuilder):

    def build_log_service(self, user_srv):
        log_dao = self._dao_bldr.build_log_dao()
        logs_queue_publisher = QueuePublisher(self._settings["QUEUE_LOGS"])
        logs_queue_publisher.open_conn()
        return LogService(self._logger, log_dao, user_srv, logs_queue_publisher)

    def build_gs_service(self):
        """
        final_log_dao = self._dao_bldr.build_final_log_dao()
        meta_dao = self._dao_bldr.build_live_meta_dao()
        profile_dao = self._dao_bldr.build_profile_dao()
        question_dao = self._dao_bldr.build_live_question_dao()
        return GlobalStreamService(self._logger, final_log_dao, meta_dao, profile_dao, question_dao)
        """
        return None
