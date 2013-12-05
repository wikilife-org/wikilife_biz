# coding=utf-8

from wikilife_utils.http_service import HTTPService
from wikilife_utils.parsers.json_parser import JSONParser
import urllib


class SinglyDelegateException(Exception):
    pass


class SinglyDelegate(object):
    """
    Singly Business Delegate
    """
    _singly_settings = None

    def __init__(self, logger, singly_settings):
        self._logger = logger
        self._singly_settings = singly_settings

    def get_available_services(self):
        url = self._singly_settings["api_services_url"]
        return HTTPService().request_get(url)

    def authenticate_service(self, authorization_code):
        """
        authorization_code: String
        returns tupple (access_token: String, account: String)
        """
        url = self._singly_settings["api_access_token_url"]
        post_params = {
            'client_id': self._singly_settings["client_id"],
            'client_secret': self._singly_settings["client_secret"],
            'code': authorization_code
        }

        body = urllib.urlencode(post_params)
        #body = "client_id="+self._singly_settings["client_id"]+"&client_secret="+self._singly_settings["client_secret"]+"&code="+authorization_code
        response = HTTPService().request_post(url, None, body, None)
        access_token = response["access_token"]
        account = response["account"]
        return access_token, account

    def add_push_filter(self, access_token, service_id, wikilife_push_listener_url):
        url = self._singly_settings["api_push_url"]
        singly_service_url = self._get_service_url_by_service_id(service_id)
        body = {singly_service_url: {
            "url": wikilife_push_listener_url
            }
        }
        params = {"access_token": access_token}
        body = JSONParser.to_json(body)
        return HTTPService().request_post(url, params, body)

    def _get_service_url_by_service_id(self, service_id):
        if service_id in self._singly_settings["api_services_urls"]:
            return self._singly_settings["api_services_urls"][service_id]

        else:
            raise SinglyDelegateException("Unknown service %s" % service_id)
