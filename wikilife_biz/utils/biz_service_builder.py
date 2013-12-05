# coding=utf-8

from wikilife_biz.services.app.utils.app_service_builder import \
    AppServiceBuilder
from wikilife_biz.services.dasnia.utils.dasnia_service_builder import \
    DasniaServiceBuilder
from wikilife_biz.services.location.location_service import LocationService
from wikilife_biz.services.log.utils.log_service_builder import \
    LogServiceBuilder
from wikilife_biz.services.meta.utils.meta_service_builder import \
    MetaServiceBuilder
from wikilife_biz.services.notification.utils.notification_service_builder import \
    NotificationServiceBuilder
from wikilife_biz.services.stat.utils.stat_service_builder import \
    StatServiceBuilder
from wikilife_biz.services.user.utils.user_service_builder import \
    UserServiceBuilder
from wikilife_biz.utils.base_service_builder import BaseServiceBuilder


class BizServiceBuilder(BaseServiceBuilder):

    _app_srv_bldr = None
    _dasnia_srv_bldr = None
    _log_srv_bldr = None
    _meta_srv_bldr = None
    _notification_srv_bldr = None
    _stat_srv_bldr = None
    _question_srv_bldr = None
    _user_srv_bldr = None

    def initialize(self):
        self._app_srv_bldr = AppServiceBuilder(self._settings, self._logger, self._dao_bldr)
        self._dasnia_srv_bldr = DasniaServiceBuilder(self._settings, self._logger, self._dao_bldr)
        self._log_srv_bldr = LogServiceBuilder(self._settings, self._logger, self._dao_bldr)
        self._meta_srv_bldr = MetaServiceBuilder(self._settings, self._logger, self._dao_bldr)
        self._notification_srv_bldr = NotificationServiceBuilder(self._settings, self._logger, self._dao_bldr)
        #self._question_srv_bldr = QuestionServiceBuilder(self._settings, self._logger, self._dao_bldr)
        self._stat_srv_bldr = StatServiceBuilder(self._settings, self._logger, self._dao_bldr)
        self._user_srv_bldr = UserServiceBuilder(self._settings, self._logger, self._dao_bldr)

    #app
    def build_app_service(self):
        return self._app_srv_bldr.build_app_service()

    def build_oauth_service(self):
        return self._app_srv_bldr.build_oauth_service()

    def build_developer_service(self):
        return self._app_srv_bldr.build_developer_service()

    #dasnia
    def build_dasnia_service(self):
        log_srv = self.build_log_service()
        return self._dasnia_srv_bldr.build_dasnia_service(log_srv)

    #location
    def build_location_service(self):
        location_dao = self._dao_bldr.build_location_dao()
        return LocationService(self._logger, location_dao)

    #log
    def build_log_service(self):
        user_srv = self._user_srv_bldr.build_user_service()
        return self._log_srv_bldr.build_log_service(user_srv)

    def build_gs_service(self):
        return self._log_srv_bldr.build_gs_service()

    #meta
    def build_meta_service(self):
        return self._meta_srv_bldr.build_meta_service()

    def build_tag_service(self):
        return self._meta_srv_bldr.build_tag_service()

    #notification
    def build_notification_service(self):
        return self._notification_srv_bldr.build_notification_service()

    #question
    def build_question_service(self):
        log_srv = self.build_log_service()
        stat_srv = self.build_stat_service()
        return self._question_srv_bldr.build_question_service(log_srv, stat_srv)

    #stat
    def build_stat_service(self):
        return self._stat_srv_bldr.build_stat_service()

    #user
    def build_user_service(self):
        return self._user_srv_bldr.build_user_service()

    def build_twitter_user_service(self):
        log_srv = self.build_log_service()
        return self._user_srv_bldr.build_twitter_user_service(log_srv)

    def build_profile_service(self):
        log_srv = self.build_log_service()
        return self._user_srv_bldr.build_profile_service(log_srv)

    def build_account_service(self):
        log_srv = self.build_log_service()
        return self._user_srv_bldr.build_account_service(log_srv)

    def build_timeline_service(self):
        return self._user_srv_bldr.build_timeline_service()

    def build_security_question_service(self):
        return self._user_srv_bldr.build_security_question_service()
