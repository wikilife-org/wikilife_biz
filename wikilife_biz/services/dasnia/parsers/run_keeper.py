# coding=utf-8

from wikilife_biz.services.dasnia.parsers.base_parser import BaseParser
from wikilife_utils.parsers.date_parser import DateParser
from wikilife_utils.date_utils import DateUtils


class RunKeeper(BaseParser):

    #type: (distance, duration)
    _activity_node_id_map = {
        "Running": 241561,
        "Cycling": 250039,
        "Mountain Biking": 250034,
        "Walking": 400,
        "Hiking": 250025,
        "Downhill Skiing": 250028,
        "Cross-Country Skiing": 250031,
        "Snowboarding": 250043,
        "Skating": 406674,
        "Swimming": 250019,
        "Wheelchair": 250037,
        "Elliptical": 250022
        }

    def parse(self, user_id, dto):
        raw_logs = []
        root_slug = "exercise"
        source = "dasnia.singly.runkeeper"

        for singly_item in dto:
            for item in singly_item["items"]:
                start = DateParser.from_datetime(item["start_time"] + " +0000")
                end = DateUtils.add_seconds(start, float(item["duration"]))
                distance_node_id = self._activity_node_id_map[item["type"]]
                distance_node = {"nodeId": distance_node_id}
                distance_node["value"] = float(item["total_distance"]) / 1000.0
                log_nodes = [distance_node]
                text = self._create_text(log_nodes)
                raw_log = self._create_log(user_id, text, root_slug, log_nodes, source, start, end)
                raw_logs.append(raw_log)

        return raw_logs
