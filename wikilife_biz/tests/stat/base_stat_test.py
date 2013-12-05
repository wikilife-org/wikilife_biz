# coding=utf-8

from wikilife_biz.tests.base_test import BaseTest
from wikilife_biz.services.stat.utils.reader_builder import ReaderBuilder


class BaseStatTest(BaseTest):

    def get_reader_bldr(self):
        return ReaderBuilder(self.get_logger(), SimpleMGRS(self.get_dao_builder().build_aggregation_dao()))
    
    
class SimpleMGRS(object):
    
    aggregation_dao = None
    
    def __init__(self, aggregation_dao):
        self.aggregation_dao = aggregation_dao