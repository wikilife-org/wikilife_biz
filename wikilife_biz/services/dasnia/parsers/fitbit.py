# coding=utf-8

from wikilife_biz.services.dasnia.parsers.base_parser import BaseParser
from wikilife_utils.parsers.date_parser import DateParser


class Fitbit(BaseParser):

    def parse(self, user_id, dto):
        raw_logs = []
        root_slug = "exercise"
        source = "dasnia.singly.fitbit"

        for item in dto:
            start = DateParser.from_datetime("%s 12:00:00 +0000" % item["data"]["id"])
            end = start
            steps_node = {"nodeId": 398}
            steps_node["value"] = item["data"]["summary"]["steps"]
            distance_node = {"nodeId": 400}
            #TODO is order ensured ?
            distance_node["value"] = item["data"]["summary"]["distances"][0]["distance"]
            log_nodes = [steps_node, distance_node]
            text = self._create_text(log_nodes)
            raw_log = self._create_log(user_id, text, root_slug, log_nodes, source, start, end)
            raw_logs.append(raw_log)

        return raw_logs
