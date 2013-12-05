# coding=utf-8

from wikilife_biz.tests.base_test import BaseTest
from wikilife_biz.services.log.log_service import LogService

class BaseLogTest(BaseTest):

    def get_log_service(self):
        return LogService(self.get_logger(), self.get_dao_builder().build_log_dao(), MockUserService(), MockQueuePublisher())


class MockUserService(object):
    
    def is_valid_user(self, user_id):
        return user_id != None


class MockQueuePublisher(object):

    def publish(self, log):
        print "MockQueuePublisher publish(%s)" %log
