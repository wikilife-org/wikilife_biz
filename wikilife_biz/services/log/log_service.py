# coding=utf-8

from wikilife_data.dao.logs.log_dao import CREATE_UTC_FIELD
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.validators.date_validator import DateValidator

OPER_INSERT = "i"
OPER_UPDATE = "u"
OPER_DELETE = "d"


class LogServiceException(Exception):
    pass


class LogService(object):
    """
    Public Business Service
    """

    _logger = None
    _user_srv = None
    _log_dao = None
    _queue_publisher = None

    def __init__(self, logger, log_dao, user_service, queue_publisher):
        """
        logger: logger impl
        log_dao: wikilife_data.dao.logs.log_dao.LogDAO
        user_service: wikilife_user_service.user_service.UserService
        queue_publisher: wikilife_utils.queue_publisher.QueuePublisher instance ready to push
        """
        self._logger = logger
        self._log_dao = log_dao
        self._user_srv = user_service
        self._queue_publisher = queue_publisher

    def add_logs_validate_all_first(self, logs, on_before_publish=None):
        """
        logs: List<log>
        on_before_publish: Closure. Args: inserted_raw_log_id
        Returns: raw logs inserted log_id list
        Raises: LogServiceException
        """
        ids = []

        for log in logs:
            self._validate_add_log(log)

        for log in logs:
            log_id = self._add_log(log, OPER_INSERT, on_before_publish)
            ids.append(log_id)

        return ids

    def add_logs(self, logs, on_before_publish=None):
        """
        logs: List<log>
        on_before_publish: Closure. Args: inserted_raw_log_id
        Returns: raw logs inserted log_id list
        Raises: LogServiceException
        """
        ids = []

        for log in logs:
            try:
                self._validate_add_log(log)
                log_id = self._add_log(log, OPER_INSERT, on_before_publish)
                ids.append(log_id)

            except LogServiceException, e:
                self._logger.error(e)

        return ids

    def edit_logs(self, logs, on_before_publish=None):
        """
        logs: List<log>
        on_before_publish: Closure. Args: inserted_raw_log_id
        Returns: raw logs inserted log_id list
        Raises: LogServiceException
        """
        ids = []
        for log in logs:
            try:
                self._validate_update_log(log)
                log_id = self._add_log(log, OPER_UPDATE, on_before_publish)
                ids.append(log_id)
            except LogServiceException, e:
                self._logger.error(e)

        return ids

    def delete_logs(self, logs, on_before_publish=None):
        """
        logs: List<log>
        on_before_publish: Closure. Args: inserted_raw_log_id
        Returns: raw logs inserted log_id list
        Raises: LogServiceException
        """
        ids = []

        for log in logs:
            try:
                self._validate_delete_log(log)

                log["start"] = "1970-01-01 00:00:00 -0000"
                log["end"] = "1970-01-01 00:00:00 -0000"
                log["nodes"] = []

                log_id = self._add_log(log, OPER_DELETE, on_before_publish)
                ids.append(log_id)
            except LogServiceException, e:
                self._logger.error(e)

        return ids

    def _add_log(self, log, oper, on_before_publish=None):
        """
        log: Dictionary
        on_before_publish: Closure. Args: inserted_raw_log_id
        Returns: raw log inserted id
        Raises: LogServiceException
        """
        log["oper"] = oper
        log["origId"] = int(log["id"]) if oper!=OPER_INSERT else 0

        log[CREATE_UTC_FIELD] = DateUtils.get_datetime_utc()
        #log["start"] = DateParser.from_datetime(log["start"])
        #if log["end"] != None:
        #    log["end"] = DateParser.from_datetime(log["end"])

        #log["start_str"] = DateFormatter.to_datetime(log["start"])
        
        inserted_id = self._log_dao.add_log(log)
        log["id"] = inserted_id  # to avoid retrieving the inserted log

        if on_before_publish != None:
            on_before_publish(log["id"])

        self._queue_publisher.publish(log)

        return inserted_id

    def _validate_add_log(self, log):
        """
        Raises: LogServiceException
        """

        if log == None:
            raise LogServiceException("Log cannot be None")

        if not "id" in log or \
           not "userId" in log or \
           not "start" in log or \
           not "end" in log or \
           not "source" in log or \
           not "nodes" in log:
            raise LogServiceException("Invalid log schema %s" % log)

        if not DateValidator.validate_datetimetz(log["start"]):
            raise LogServiceException("Invalid log start time format")

        if log["end"] != None and not DateValidator.validate_datetimetz(log["end"]):
            raise LogServiceException("Invalid log end time format")

        for log_node in log["nodes"]:
            if not "nodeId" in log_node or not "metricId" in log_node or not "value" in log_node:
                raise LogServiceException("Invalid log node schema")
            if log_node["value"] == None or log_node["value"] == "":
                raise LogServiceException("Invalid log node value")

        if not self._user_srv.is_valid_user(log["userId"]):
            raise LogServiceException("User ID not found")

        #TODO validate ranges

        """
        start_utc = DateUtils.to_datetime_utc(DateParser.from_datetime(log["start"]))
        today_utc = DateUtils.get_datetime_utc()

        if DateUtils.create_datetime(start_utc.year, start_utc.month, start_utc.day) > DateUtils.create_datetime(today_utc.year, today_utc.month, today_utc.day):
            raise LogServiceException("Logs with future date not allowed. %s" % log["start"])
        """

    def _validate_update_log(self, log):
        self._validate_add_log(log)

    def _validate_delete_log(self, log):
        """
        Raises: LogServiceException
        """

        if log == None:
            raise LogServiceException("Log cannot be None")

        if not "id" in log or \
           not "userId" in log or \
           not "source" in log:
            raise LogServiceException("Invalid log schema")

        if not self._user_srv.is_valid_user(log["userId"]):
            raise LogServiceException("User ID not found")
