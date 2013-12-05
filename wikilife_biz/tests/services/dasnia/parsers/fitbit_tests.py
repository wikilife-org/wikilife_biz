# coding=utf-8

from wikilife_biz.services.dasnia.parsers.fitbit import Fitbit
from wikilife_biz.tests.services.dasnia.base_dasnia_test import BaseDasniaTest


class FitbitTests(BaseDasniaTest):

    def test_parse(self):
        parser = Fitbit(self.get_dao_builder().build_live_meta_dao())
        dto = self._get_test_dto()
        user_id = "TEST123"
        raw_logs = parser.parse(user_id, dto)
        raw_log = raw_logs[0]

        source = raw_log["source"]
        category = raw_log["category"]
        start = raw_log["start"]
        end = raw_log["end"]
        nodes = raw_log["nodes"]
        text = raw_log["text"]

        assert raw_log != None
        assert category == "exercise"
        assert source == "dasnia.singly.fitbit"
        assert start == "2012-05-30 12:00:00 +0000"
        assert end == "2012-05-30 12:00:00 +0000"
        assert text == "Walking, Step 4580 steps, Distance 5.34 kilometres" 
        assert len(nodes) == 2

        steps_node = nodes[0]
        assert steps_node["nodeId"] == 398
        assert steps_node["value"] == 4580

        distance_node = nodes[1]
        assert distance_node["nodeId"] == 400
        assert distance_node["value"] == 5.34

    """ Helpers """

    def _get_test_dto(self):
        return [
            {
            "idr": "activity:229RTD@fitbit/activities#2012-05-30",
            "id": "368e0d5a3568bb182e27e5d2bd0acaa2_7c006449b",
            "data": {
              "activities": [],
              "goals": {
                "activeScore": 1000,
                "caloriesOut": 2929,
                "distance": 8.05,
                "floors": 10,
                "steps": 10000
              },
              "summary": {
                "activeScore": 449,
                "activityCalories": 719,
                "caloriesOut": 2323,
                "distances": [
                  {
                    "activity": "total",
                    "distance": 5.34
                  },
                  {
                    "activity": "tracker",
                    "distance": 5.34
                  },
                  {
                    "activity": "loggedActivities",
                    "distance": 0
                  },
                  {
                    "activity": "veryActive",
                    "distance": 4.37
                  },
                  {
                    "activity": "moderatelyActive",
                    "distance": 0.5
                  },
                  {
                    "activity": "lightlyActive",
                    "distance": 0.46
                  },
                  {
                    "activity": "sedentaryActive",
                    "distance": 0
                  }
                ],
                "elevation": 36.58,
                "fairlyActiveMinutes": 19,
                "floors": 12,
                "lightlyActiveMinutes": 83,
                "marginalCalories": 514,
                "sedentaryMinutes": 938,
                "steps": 4580,
                "veryActiveMinutes": 31
              },
              "id": "2012-05-30",
              "at": 1338336000000
            },
            "at": 1338336000000,
            "map": {}
          }
        ]
