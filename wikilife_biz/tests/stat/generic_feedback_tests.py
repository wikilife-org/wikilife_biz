# coding=utf-8

from wikilife_data.tests.base_test import BaseTest
from wikilife_stat_service.stat_readers.generic_feedback import GenericFeedbackReader
from wikilife_stat_service.utils.stats_service_builder import StatsServiceBuilder

import datetime
import json
import sys

TEST_USER_ID = -60


class Test(BaseTest):

    def setUp(self):
        self.mgr = self.get_manager_builder().build_generic_stats_manager()
        self.log_mgr = self.get_manager_builder().build_log_manager()

        self.managers = StatsServiceBuilder().build_manager(self.get_logger(), self.get_db_conn())

        entry1 = json.loads("""
{
   "user_id": "600000",
   "date":"2012-06-21",
   "log_nodes":{
      "log1":{
         "prop1":{
            "node1":{
               "count":3,
               "sum":9
            }
         },
         "prop2":{
            "node2":{
               "count":7,
               "option_sum":[
                  {
                     "opt":"valor",
                     "count":2
                  },
                  {
                     "opt":"otro valor",
                     "count":2
                  }
               ]
            }
         },
         "count":9
      }
   }
}
        """)

        entry2 = json.loads("""
{
   "user_id": "600000",
   "date":"2012-06-22",
   "log_nodes":{
      "log1":{
         "prop1":{
            "node1":{
               "count":9,
               "sum":1
            }
         },
         "prop2":{
            "node2":{
               "count":4,
               "option_sum":[
                  {
                     "opt":"valor",
                     "count":3
                  },
                  {
                     "opt":"blue",
                     "count":7
                  }
               ]
            }
         },
         "count":55
      }
   }
}
        """)

        entry3 = json.loads("""
{
   "user_id": "600000",
   "date":"2012-06-23",
   "log_nodes":{
      "log1":{
         "prop1":{
            "node1":{
               "count":3,
               "sum":9
            }
         },
         "prop2":{
            "node2":{
               "count":7,
               "option_sum":[
                  {
                     "opt":"blue",
                     "count":9
                  },
                  {
                     "opt":"yellow",
                     "count":1
                  }
               ]
            }
         },
         "count":1
      }
   }
}
        """)

        sys.stdout.write("Inserting data into db...")
        self.managers.user_log_stats_mgr.save_user_log_day(entry1)
        self.managers.user_log_stats_mgr.save_user_log_day(entry2)
        self.managers.user_log_stats_mgr.save_user_log_day(entry3)
        print " done."

    def test_get_logs(self):
        expected_result = json.loads("""
        {"14": {"count": 65, "prop1": {"node1": {"count": 15, "sum": 19}}, "prop2": {"node2": {"count": 18, "option_sum": [{"opt": "blue", "count": 16}, {"opt": "otro valor", "count": 2}, {"opt": "yellow", "count": 1}, {"opt": "valor", "count": 5}]}}}, "7": {"count": 65, "prop1": {"node1": {"count": 15, "sum": 19}}, "prop2": {"node2": {"count": 18, "option_sum": [{"opt": "blue", "count": 16}, {"opt": "otro valor", "count": 2}, {"opt": "yellow", "count": 1}, {"opt": "valor", "count": 5}]}}}}
        """)

        date = datetime.datetime.strptime("20120624", "%Y%m%d").date()

        result = GenericFeedbackReader(self.get_logger(), self.managers).read_stat("600000", date, "log1", (7, 14))

        assert expected_result == json.loads(json.dumps(result))

if __name__ == "__main__":
    pass
