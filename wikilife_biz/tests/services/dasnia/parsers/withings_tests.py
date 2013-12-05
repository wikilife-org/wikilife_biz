# coding=utf-8

from wikilife_biz.services.dasnia.parsers.withings import Withings
from wikilife_biz.tests.services.dasnia.base_dasnia_test import BaseDasniaTest


class ZeoTests(BaseDasniaTest):

    def test_parse(self):
        parser = Withings(self.get_dao_builder().build_live_meta_dao())
        dto = self._get_test_dto()
        user_id = "TEST123"
        raw_logs = parser.parse(user_id, dto)
        assert len(raw_logs) == 2

        raw_log = raw_logs[0]

        source = raw_log["source"]
        category = raw_log["category"]
        start = raw_log["start"]
        end = raw_log["end"]
        nodes = raw_log["nodes"]
        text = raw_log["text"]

        assert raw_log != None
        assert category == "exercise"
        assert source == "dasnia.singly.withings"
        #assert start == "2012-08-02 14:35:04 +0000"
        #assert end == "2012-08-02 14:35:04 +0000"
        assert text == "Weight, Current 76.75 kg"
        print text
        
        assert len(nodes) == 1

        weight_node = nodes[0]
        assert weight_node["nodeId"] == 1140
        assert weight_node["value"] == 76.75

    """ Helpers """

    def _get_test_dto(self):
        #https://singly.com/docs/withings
        #http://www.withings.com/en/api/wbsapiv2#getmeas
        
        return [
              {
                "idr": "measure:1057610@withings/measures#72449130",
                "id": "f26886baaf9a9453fe1678b7669e0337_567262b67",
                "data": {
                  "grpid": 72449130,
                  "attrib": 0,
                  "date": 1343928904,
                  "category": 1,
                  "measures": [
                    {
                      "value": 76750,
                      "type": 1,
                      "unit": -3
                    },
                    {
                      "value": 64039,
                      "type": 5,
                      "unit": -3
                    },
                    {
                      "value": 16562,
                      "type": 6,
                      "unit": -3
                    },
                    {
                      "value": 12711,
                      "type": 8,
                      "unit": -3
                    }
                  ],
                  "id": 72449130
                },
                "at": 1344970532444,
                "types": {}
              },
              {
                "idr": "measure:1057610@withings/measures#72448559",
                "id": "bb232196cc00bc4e3ccf987ade916961_567262b67",
                "data": {
                  "grpid": 72448559,
                  "attrib": 0,
                  "date": 1343928337,
                  "category": 1,
                  "measures": [
                    {
                      "value": 76900,
                      "type": 1,
                      "unit": -3
                    },
                    {
                      "value": 64025,
                      "type": 5,
                      "unit": -3
                    },
                    {
                      "value": 16743,
                      "type": 6,
                      "unit": -3
                    },
                    {
                      "value": 12875,
                      "type": 8,
                      "unit": -3
                    }
                  ],
                  "id": 72448559
                },
                "at": 1344970532444,
                "types": {}
              },
              {
                "idr": "measure:1057610@withings/measures#72450084",
                "id": "315d775daf46f7c365191d9b6e6907dc_567262b67",
                "data": {
                  "grpid": 72450084,
                  "attrib": 1,
                  "date": 1343929621,
                  "category": 1,
                  "measures": [
                    {
                      "value": 78700,
                      "type": 1,
                      "unit": -3
                    },
                    {
                      "value": 61764,
                      "type": 5,
                      "unit": -3
                    },
                    {
                      "value": 21521,
                      "type": 6,
                      "unit": -3
                    },
                    {
                      "value": 16936,
                      "type": 8,
                      "unit": -3
                    }
                  ],
                  "id": 72450084
                },
                "at": 1344970532444,
                "types": {}
              }            
        ]
