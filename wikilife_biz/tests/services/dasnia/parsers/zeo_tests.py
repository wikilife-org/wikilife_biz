# coding=utf-8

from wikilife_biz.services.dasnia.parsers.zeo import Zeo
from wikilife_biz.tests.services.dasnia.base_dasnia_test import BaseDasniaTest


class ZeoTests(BaseDasniaTest):

    def test_parse(self):
        parser = Zeo(self.get_dao_builder().build_live_meta_dao())
        dto = self._get_test_dto()
        user_id = "TEST123"
        raw_logs = parser.parse(user_id, dto)
        assert len(raw_logs) == 3

        raw_log = raw_logs[0]

        source = raw_log["source"]
        category = raw_log["category"]
        start = raw_log["start"]
        end = raw_log["end"]
        nodes = raw_log["nodes"]
        text = raw_log["text"]

        assert raw_log != None
        assert category == "exercise"
        assert source == "dasnia.singly.zeo"
        #assert start == "2012-08-22 01:13:51 +0000"
        #assert end == "2012-08-22 09:30:51 +0000"
        #assert text == "Sleep, Light 257 minutes, Deep 83 minutes, Rem 158 minutes, Awake 6 minutes"
        print text
        
        assert len(nodes) == 4

        """
        light_node = nodes[0]
        assert light_node["node_id"] == 0
        assert light_node["value"] == 257
        """

        deep_node = nodes[1]
        assert deep_node["nodeId"] == 241563
        assert deep_node["value"] == 83

        rem_node = nodes[2]
        assert rem_node["nodeId"] == 241565
        assert rem_node["value"] == 158

        awake_node = nodes[3]
        assert awake_node["nodeId"] == 241567
        assert awake_node["value"] == 6

    """ Helpers """

    def _get_test_dto(self):
        #https://singly.com/docs/zeo
        #https://api.singly.com/services/zeo/sleep_stats
        return [
          {
            "idr": "sleepstat:13375@zeo/sleep_stats#221138512012",
            "id": "8ecac0103c325d2d4ef23c3c3c45d656_cc8d0ed10",
            "data": {
              "awakenings": 5,
              "awakeningsZqPoints": -3,
              "bedTime": {
                "day": 22,
                "hour": 1,
                "minute": 13,
                "month": 8,
                "second": 51,
                "year": 2012
              },
              "grouping": "DAILY",
              "morningFeel": 2,
              "riseTime": {
                "day": 22,
                "hour": 9,
                "minute": 35,
                "month": 8,
                "second": 0,
                "year": 2012
              },
              "startDate": {
                "day": 21,
                "month": 8,
                "year": 2012
              },
              "timeInDeep": 83,
              "timeInDeepPercentage": 16,
              "timeInDeepZqPoints": 18,
              "timeInLight": 257,
              "timeInLightPercentage": 52,
              "timeInRem": 158,
              "timeInRemPercentage": 31,
              "timeInRemZqPoints": 11,
              "timeInWake": 6,
              "timeInWakePercentage": 1,
              "timeInWakeZqPoints": 0,
              "timeToZ": 4,
              "totalZ": 497,
              "totalZZqPoints": 70,
              "zq": 96
            },
            "at": 1347403210845,
            "map": {
              "id": "221138512012"
            },
            "types": {}
          },
          {
            "idr": "sleepstat:13375@zeo/sleep_stats#2416872012",
            "id": "853c566b49943b51d6ea3d7566d9a1de_cc8d0ed10",
            "data": {
              "awakenings": 4,
              "awakeningsZqPoints": -2,
              "bedTime": {
                "day": 24,
                "hour": 1,
                "minute": 6,
                "month": 8,
                "second": 7,
                "year": 2012
              },
              "grouping": "DAILY",
              "morningFeel": 2,
              "riseTime": {
                "day": 24,
                "hour": 9,
                "minute": 40,
                "month": 8,
                "second": 0,
                "year": 2012
              },
              "startDate": {
                "day": 23,
                "month": 8,
                "year": 2012
              },
              "timeInDeep": 81,
              "timeInDeepPercentage": 17,
              "timeInDeepZqPoints": 17,
              "timeInLight": 248,
              "timeInLightPercentage": 53,
              "timeInRem": 142,
              "timeInRemPercentage": 29,
              "timeInRemZqPoints": 10,
              "timeInWake": 6,
              "timeInWakePercentage": 1,
              "timeInWakeZqPoints": 0,
              "timeToZ": 44,
              "totalZ": 470,
              "totalZZqPoints": 66,
              "zq": 91
            },
            "at": 1347403210845,
            "map": {
              "id": "2416872012"
            },
            "types": {}
          },
          {
            "idr": "sleepstat:13375@zeo/sleep_stats#23347892012",
            "id": "76ae0a6964e6df161ec057517bd5b751_cc8d0ed10",
            "data": {
              "awakenings": 4,
              "awakeningsZqPoints": -2,
              "bedTime": {
                "day": 23,
                "hour": 3,
                "minute": 47,
                "month": 8,
                "second": 9,
                "year": 2012
              },
              "grouping": "DAILY",
              "morningFeel": 0,
              "riseTime": {
                "day": 23,
                "hour": 10,
                "minute": 20,
                "month": 8,
                "second": 0,
                "year": 2012
              },
              "startDate": {
                "day": 22,
                "month": 8,
                "year": 2012
              },
              "timeInDeep": 64,
              "timeInDeepPercentage": 19,
              "timeInDeepZqPoints": 13,
              "timeInLight": 158,
              "timeInLightPercentage": 51,
              "timeInRem": 71,
              "timeInRemPercentage": 22,
              "timeInRemZqPoints": 5,
              "timeInWake": 26,
              "timeInWakePercentage": 8,
              "timeInWakeZqPoints": -2,
              "timeToZ": 101,
              "totalZ": 292,
              "totalZZqPoints": 42,
              "zq": 56
            },
            "at": 1347403210845,
            "map": {
              "id": "23347892012"
            },
            "types": {}
          }
        ]