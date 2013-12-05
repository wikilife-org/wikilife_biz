# coding=utf-8

from datetime import datetime
from wikilife_biz.tests.services.log.base_log_test import BaseLogTest

TEST_USER_ID = "BMQE9S"


class LogServiceAddTests(BaseLogTest):

    def tearDown(self):
        self.get_log_service()._log_dao._collection.remove({"test": True})

    def test_add_logs(self):
        """
        test LogService insertion in DB and Queue.   
        """
        log_srv = self.get_log_service()
        log_collection = log_srv._log_dao._collection
        #queue = self.get_queue("test_add_logs_queue")
        #queue.open_conn()

        internal_user_id = TEST_USER_ID
        start = self._get_datetime()
        end = start
        log = self._create_log(internal_user_id, start, end)
        inserted_ids = log_srv.add_logs([log])

        assert len(inserted_ids) == 1 
        assert log_collection.find_one({"userId": internal_user_id}) != None
        #assert queue._channel.method.message_count == 1 

    """ Helpers """

    def _create_log(self, internal_user_id, start=None, end=None, nodes=[{"nodeId": 298, "value" : 60}]):
        return {
            "id": 0,
            "origId": 0,
            "source": "log_service.tests",
            "category": "test",
            "userId": "TEST",
            "start": start,
            "end": end,
            "text": "test log",
            "nodes": nodes,
            "test": True
        }

    def _get_datetime(self):
        fmt = "%Y-%m-%d %H:%M:%S"
        datetime_now = datetime.utcnow()
        datetime_now_str = datetime_now.strftime(fmt)
        #TODO
        return datetime_now_str + " +0300"
