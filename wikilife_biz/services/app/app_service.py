# coding=utf-8

from wikilife_utils.hasher import Hasher
import random


class AppServiceException(Exception):
    pass


class AppService(object):

    _logger = None
    _app_dao = None

    def __init__(self, logger, app_dao):
        self._logger = logger
        self._app_dao = app_dao

    def get_apps_by_developer(self, developer_id):
        return self._app_dao.get_apps_by_developer_id(developer_id)

    def get_app_by_client_id(self, client_id):
        return self._app_dao.get_app_by_client_id(client_id)

    def add_app(self, name, callback_url, developer_id):
        self._validate_app_name(name)
        client_id, client_secret = self._get_app_keys(name, developer_id)
        self._app_dao.insert_app(name, callback_url, developer_id, client_id, client_secret)
        return self._app_dao.get_app_by_name(name)

    def update_app(self, app_id, name, callbackUrl, developer_id):
        app = self._app_dao.get_app_by_id(app_id)

        if app == None:
            raise AppServiceException("App not found")

        if app["developerId"] != developer_id:
            raise AppServiceException("Developer ID not match")

        app["name"] = name
        app["callbackUrl"] = callbackUrl

        self._app_dao.update_app(app)

    def remove_app(self, app_id, developer_id):
        self._app_dao.delete_app(app_id, developer_id)

    def _validate_app_name(self, app_name):
        if app_name == None:
            raise AppServiceException("App Name cannot be None")

        if len(app_name) < 4:
            raise AppServiceException("App Name too short. Min 4 chars. %s" % app_name)

        if len(app_name) > 16:
            raise AppServiceException("App Name too long. Max 16 chars. %s" % app_name)

        if self._app_dao.get_app_by_name(app_name) != None:
            raise AppServiceException("App Name not available. %s" % app_name)

    def _get_app_keys(self, app_name, developer_id):
        client_id = Hasher.create_pseudo_unique(16)

        while(self._app_dao.get_app_by_client_id(client_id) != None):
            client_id = Hasher.create_pseudo_unique(16)

        client_secret = Hasher.create_sha256("%s%s%s%s" % (app_name, developer_id, client_id, random.random))
        return client_id, client_secret
