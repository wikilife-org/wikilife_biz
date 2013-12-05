# coding=utf-8

from wikilife_biz.tests.stat.base_stat_test import BaseStatTest


READER_ID = "wikilife_biz.services.stat.stat_readers.aggregated_logs_reader.AggregatedLogsReader"

class AggregatedLogsTests(BaseStatTest):

    def test_read_stat(self):
        reader = self.get_reader_bldr().build_reader(READER_ID)

        summary_id = None 

        #Sleep deep
        #loggable_id = 3
        #propperty_id = 241562

        #Running distance
        loggable_id = 296
        propperty_id = 241560

        age = "16-20"
        #age = "36-40"

        #gender = "Male"
        gender = "Female"
        #gender = ".*"

        #sleep = "6-7"
        sleep = ".*"


        result = reader.read_stat(loggable_id, propperty_id, summary_id, age, gender, sleep)

        print result

        for item in result["data"]:
            print item

        print "Total: %s"  %(len(result["data"]))
        