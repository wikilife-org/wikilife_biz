# coding=utf-8

from wikilife_biz.services.user.account_service import AccountService
from wikilife_biz.services.user.profile_service import ProfileService
from wikilife_biz.services.user.security_question_service import \
    SecurityQuestionsService
from wikilife_biz.services.user.timeline_service import TimelineService
from wikilife_biz.services.user.twitter_user_service import TwitterUserService
from wikilife_biz.services.user.user_service import UserService
from wikilife_utils.queue_publisher import QueuePublisher
from wikilife_biz.services.twitter.delegates.twitter_search_user_delegate import TwitterUserLocation


class UserServiceBuilder(object):

    _settings = None
    _logger = None
    _dao_bldr = None

    def __init__(self, settings, logger, dao_builder):
        self._settings = settings
        self._logger = logger
        self._dao_bldr = dao_builder

    def build_user_service(self):
        user_dao = self._dao_bldr.build_user_dao()
        return UserService(self._logger, user_dao)

    def build_twitter_user_service(self, log_srv):
        twitter_user_dao = self._dao_bldr.build_twitter_user_dao()
        #twitter_config_dao = self._dao_bldr.build_twitter_configuration_dao()
        twitter_config_dao = None
        log_dao = self._dao_bldr.build_log_dao()
        final_log_dao = self._dao_bldr.build_final_log_dao()
        account_srv = self.build_account_service(log_srv)
        oper_queue_publisher = QueuePublisher(self._settings["QUEUE_OPERS"])
        oper_queue_publisher.open_conn()
        profile_dao = self._dao_bldr.build_profile_dao()
        twitter_search_location= TwitterUserLocation()
        user_dao = self._dao_bldr.build_user_dao()
        return TwitterUserService(self._logger, twitter_user_dao, twitter_config_dao, log_dao, final_log_dao, profile_dao, account_srv, twitter_search_location, user_dao, oper_queue_publisher)

    def build_account_service(self, log_srv):
        user_srv = self.build_user_service()
        profile_srv = self.build_profile_service(log_srv)
        return AccountService(self._logger, user_srv, profile_srv)

    def build_profile_service(self, log_srv):
        meta_dao = self._dao_bldr.build_live_meta_dao()
        profile_dao = self._dao_bldr.build_profile_dao()
        user_srv = self.build_user_service()
        return ProfileService(self._logger, meta_dao, profile_dao, user_srv, log_srv)

    def build_timeline_service(self):
        timeline_dao = self._dao_bldr.build_timeline_dao()
        reports_dao = self._dao_bldr.build_reports_dao()
        return TimelineService(self._logger, timeline_dao, reports_dao)

    def build_security_question_service(self):
        sq_dao = self._dao_bldr.build_live_security_question_dao()
        user_dao = self._dao_bldr.build_user_dao()
        user_token_dao = self._dao_bldr.build_user_token_dao()
        recovery_info_dao = self._dao_bldr.build_recovery_information_dao()
        profile_dao = self._dao_bldr.build_profile_dao()
        return SecurityQuestionsService(self._logger, user_dao, sq_dao, recovery_info_dao, user_token_dao, profile_dao)
