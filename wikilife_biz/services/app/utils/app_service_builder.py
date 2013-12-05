# coding=utf-8

from wikilife_biz.services.app.app_service import AppService
from wikilife_biz.services.app.developer_service import DeveloperService
from wikilife_biz.services.app.oauth_service import OAuthService
from wikilife_biz.utils.base_service_builder import BaseServiceBuilder


class AppServiceBuilder(BaseServiceBuilder):

    def build_app_service(self):
        app_dao = self._dao_bldr.build_app_dao()
        return AppService(self._logger, app_dao)

    def build_oauth_service(self):
        user_dao = self._dao_bldr.build_user_dao()
        oauth_token_dao = self._dao_bldr.build_oauth_token_dao()
        oauth_client_dao = self._dao_bldr.build_oauth_client_dao()
        return OAuthService(self._logger, user_dao, oauth_token_dao, oauth_client_dao)

    def build_developer_service(self):
        developers_dao = self._dao_bldr.build_developers_dao()
        return DeveloperService(self._logger, developers_dao)
