# coding=utf-8

from wikilife_biz.services.log.log_service import LogServiceException
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_utils.logs.log_creator import LogCreator


class ProfileServiceException(Exception):
    pass


class ProfileService(object):
    _meta_dao = None
    _profile_dao = None
    _user_srv = None
    _log_srv = None
    _lvs = None

    def __init__(self, logger, meta_dao, profile_dao, user_service, log_service):
        self._logger = logger
        self._meta_dao = meta_dao
        self._profile_dao = profile_dao
        self._user_srv = user_service
        self._log_srv = log_service

        try:
            self._lvs = self._profile_dao.get_profile_items()

            for k in self._lvs:
                meta_node = self._meta_dao.get_node_by_id(self._lvs[k]["nodeId"])
                self._lvs[k]["node_name"] = meta_node.name
        except Exception, e:
            raise ProfileServiceException("Initialization error: %s" %e)

    def add_profile(self, user_id, user_tz_name, source, birthdate, height, weight, gender=None, country=None, region=None, city=None):
        """
        Async
        """
        logs = []

        if not birthdate:
            raise ProfileServiceException("Birthdate is mandatory")

        if not user_tz_name:
            raise ProfileServiceException("user_tz_name is mandatory")

        if source == None:
            raise ProfileServiceException("source cannot be None")

        if gender != None:
            logs.append(self._create_log(self._lvs["gender"], user_id, user_tz_name, gender, source))

        #logs.append(self._create_log(self._lvs["birthdate"], user_id, user_tz_name, birthdate, source))
        logs.append(self._create_log(self._lvs["height"], user_id, user_tz_name, height, source))
        logs.append(self._create_log(self._lvs["weight"], user_id, user_tz_name, weight, source))

        if country:
            logs.append(self._create_log(self._lvs["country"], user_id, user_tz_name, country, source))

        if region:
            logs.append(self._create_log(self._lvs["region"], user_id, user_tz_name, region, source))

        if city:
            logs.append(self._create_log(self._lvs["city"], user_id, user_tz_name, city, source))

        try:
            self._log_srv.add_logs(logs)

        except LogServiceException, e: 
            raise ProfileServiceException(e)

    def update_profile(self, user_id, user_tz_name, source, country=None, region=None, city=None):
        """
        Async
        """
        logs = []

        if country:
            logs.append(self._create_log(self._lvs["country"], user_id, user_tz_name, country, source))

        if region:
            logs.append(self._create_log(self._lvs["region"], user_id, user_tz_name, region, source))

        if city:
            logs.append(self._create_log(self._lvs["city"], user_id, user_tz_name, city, source))

        try:
            self._log_srv.add_logs(logs)

        except LogServiceException, e: 
            raise ProfileServiceException(e)
    
    def get_profiles_with_no_location(self, limit=300):
        return self._profile_dao.get_profiles_with_no_location(limit)

    def get_profile_by_user_id(self, user_id):
        return self._profile_dao.get_profile_by_user_id(user_id)

    def remove_profile_by_user_id(self, user_id):
        self._profile_dao.remove_profile_by_user_id(user_id)

    def _create_log(self, lv, user_id, user_tz_name, log_value, source):
        dt = DateUtils.get_datetime_local(user_tz_name)
        dt = DateUtils.add_seconds(dt, -60 * 5)
        start = DateFormatter.to_datetime(dt)
        end = start
        text = "%s  %s" % (lv["node_name"], log_value)
        log_node = LogCreator.create_log_node(lv["nodeId"], lv["metricId"], log_value)
        nodes = [log_node]
        log = LogCreator.create_log(user_id, start, end, text, source, nodes)
        return log
