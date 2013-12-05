# coding=utf-8

from wikilife_biz.services.log.log_service import LogServiceException
from wikilife_biz.tests.services.log.base_log_test import BaseLogTest


class LogServiceValidateTests(BaseLogTest):

    _log_srv = None

    def setUp(self):
        self._log_srv = self.get_log_service()

    def test__validate_add_log(self):
        valid_log = self._create_log("2012-01-15 10:30:45 -0300", "2012-01-15 10:30:45 -0300")

        try:
            self._log_srv._validate_add_log(valid_log)
            assert True

        except LogServiceException:
            assert False
    
    def test__validate_add_log_bad_schema(self):
        bad_schema_log = {}

        try:
            self._log_srv._validate_add_log(bad_schema_log)
            assert False

        except LogServiceException, e:
            assert e.message == "Invalid log schema" or e.message == "Invalid log execute_time format" or e.message == "User ID not found"

    def test__validate_add_log_future_execute_time(self):
        future_execute_time_log = self._create_log("2015-01-01 00:00:00 -0300", "2015-01-01 00:00:00 -0300")
        
        try:
            self._log_srv._validate_add_log(future_execute_time_log)
            assert False

        except LogServiceException, e:
            assert e.message.startswith("Logs with future date not allowed") 

        
    """ Helpers """
    
    """
    def _create_log(self, execute_time):
        return {
            "test": True,
            "pk" : 1, 
            "model" : "LogEntry",
            "fields" : {
                "original_entry" : 0,
                "root_slug" : "exercise",
                "source" : "log_service_tests",
                "status" : 1,
                "text" : "Running  60 minutes",
                "user_id" : "TEST",
                "execute_time" : execute_time,
                "nodes" : [
                    {
                        "node_id" : 298,
                        "value" : 60
                    }
                ]
            }
        }
    """
    def _create_log(self, start=None, end=None, nodes=[{"nodeId": 298, "value" : 60}]):
        return {
            "id": 0,
            "origId": 0,
            "oper": "i",
            "source": "log_service.tests",
            "category": "test",
            "userId": "TEST",
            "start": start,
            "end": end,
            "text": "test log id=%s" %id,
            "nodes": nodes,
            "test": True
        }
