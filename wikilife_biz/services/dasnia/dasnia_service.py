# coding=utf-8

from wikilife_utils.hasher import Hasher


class DasniaServiceException(Exception):
    pass


class DasniaService(object):

    _dasnia_settings = None
    _singly_delegate = None
    _user_services_dao = None
    _singly_parsers = None
    _log_srv = None

    def __init__(self, logger, dasnia_settings, user_services_dao, singly_delegate, singly_parsers, log_service):
        self._logger = logger
        self._dasnia_settings = dasnia_settings
        self._user_services_dao = user_services_dao
        self._singly_delegate = singly_delegate
        self._singly_parsers = singly_parsers
        self._log_srv = log_service

    def get_available_services(self):
        singly_services = self._singly_delegate.get_available_services()
        available_services = {}
        available_services["zeo"] = self._parse_singly_service(singly_services, "zeo")
        available_services["fitbit"] = self._parse_singly_service(singly_services, "fitbit")
        available_services["runkeeper"] = self._parse_singly_service(singly_services, "runkeeper")
        available_services["withings"] = self._parse_singly_service(singly_services, "withings")
        return available_services

    def _parse_singly_service(self, singly_services, service_id):
        singly_service = singly_services[service_id]
        service = {}
        service["id"] = service_id

        for field in ["name", "desc", "icons"]:
            service[field] = singly_service[field]

        return service

    def get_user_services(self, user_id):
        user_services = {}

        for user_service in self._user_services_dao.get_user_services(user_id):
            user_services[user_service["id"]] = user_service

        return user_services

    def add_service(self, user_id, service_id, auth_code):
        """
        user_id: String. Wikilife user id
        service_id: String.
        auth_code: String. Oauth code
        returns Added service wikilife metadata
        """
        access_token, account = self._singly_delegate.authenticate_service(auth_code)
        user_service_hash = Hasher.create_sha256("%s%s" % (user_id, service_id))
        push_listener_url = self._dasnia_settings["singly"]["push_listener_base_url"] + user_service_hash
        self._singly_delegate.add_push_filter(access_token, service_id, push_listener_url)
        self._user_services_dao.insert_user_service(user_id, service_id, auth_code, access_token, account, user_service_hash)
        #self._retrieve_user_historical_data(user_id, access_token)
        return self._user_services_dao.get_user_service(user_id, service_id)

    def _retrieve_user_historical_data(self, user_id, access_token):
        #TODO use an async queue ?
        historical_data = self._singly_delegate.get_user_historical_data(access_token)
        logs = self._singly_parser.parse_historical_data_to_raw_logs(user_id, historical_data)
        self._log_srv.add_logs(logs)

    def remove_service(self, user_id, service_id):
        #TODO https://singly.com/docs/profiles#Deleting-Profiles
        pass

    def process_singly_push(self, hash_token, dto):
        user_service = self._user_services_dao.get_user_service_by_hash(hash_token)
        user_id = user_service["user_id"]
        service_name = user_service["service_name"]
        parser = self._singly_parsers.get_parser(service_name)
        raw_logs = parser.parse(user_id, dto)
        self._log_srv.add_logs(raw_logs)
