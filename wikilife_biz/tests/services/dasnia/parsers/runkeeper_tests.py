# coding=utf-8

from wikilife_biz.services.dasnia.parsers.run_keeper import RunKeeper
from wikilife_biz.tests.services.dasnia.base_dasnia_test import BaseDasniaTest


class RunkeeperTests(BaseDasniaTest):

    def test_parse(self):
        parser = RunKeeper(self.get_dao_builder().build_live_meta_dao())
        dto = self._get_test_dto()
        user_id = "TEST123"
        raw_logs = parser.parse(user_id, dto)
        assert len(raw_logs) == 4 

        raw_log = raw_logs[0]

        source = raw_log["source"]
        category = raw_log["category"]
        start = raw_log["start"]
        end = raw_log["end"]
        nodes = raw_log["nodes"]
        text = raw_log["text"]

        assert raw_log != None
        assert category == "exercise"
        assert source == "dasnia.singly.runkeeper"
        assert start == "2011-03-01 07:00:00 +0000"
        assert end == "2011-03-01 07:15:00 +0000"
        assert text == "Running, Distance 3.0 km" 
        assert len(nodes) == 1

        distance_node = nodes[0]
        assert distance_node["nodeId"] == 241561
        assert distance_node["value"] == 3

    """ Helpers """

    def _get_test_dto(self):
        return [       
            {
            "size": 40,
            "items": [
                {
                   "type": "Running",
                   "start_time": "Tue, 1 Mar 2011 07:00:00",
                   "total_distance": 3000,
                   "duration": 900,
                   "uri": "/activities/40"
                },
                {
                   "type": "Running",
                   "start_time": "Thu, 3 Mar 2011 07:00:00",
                   "total_distance": 70,
                   "duration": 10,
                   "uri": "/activities/39"
                },
                {
                   "type": "Running",
                   "start_time": "Sat, 5 Mar 2011 11:00:00",
                   "total_distance": 70,
                   "duration": 10,
                   "uri": "/activities/38"
                },
                {
                   "type": "Running",
                   "start_time": "Mon, 7 Mar 2011 07:00:00",
                   "total_distance": 70,
                   "duration": 10,
                   "uri": "/activities/37"
                }
            ],
            "previous": "https://api.runkeeper.com/user/1234567890/activities?page=2"
            }
        ]
