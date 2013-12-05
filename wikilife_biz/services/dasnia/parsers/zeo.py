# coding=utf-8

from wikilife_biz.services.dasnia.parsers.base_parser import BaseParser
from wikilife_utils.date_utils import DateUtils


class Zeo(BaseParser):

    def parse(self, user_id, dto):
        raw_logs = []
        root_slug = "exercise"
        source = "dasnia.singly.zeo"

        for item in dto:
            #TODO
            #execute_datetime = DateParser.from_timestamp(item["at"])
            dt = item["data"]["bedTime"]
            start = DateUtils.create_datetime(dt["year"], dt["month"], dt["day"], dt["hour"], dt["minute"], dt["second"])
            end = DateUtils.add_seconds(start, float(item["data"]["totalZ"]) * 60)

            light_node = {"nodeId": 241563}
            light_node["value"] = item["data"]["timeInLight"]

            deep_node = {"nodeId": 241563}
            deep_node["value"] = item["data"]["timeInDeep"]

            rem_node = {"nodeId": 241565}
            rem_node["value"] = item["data"]["timeInRem"]

            awake_node = {"nodeId": 241567}
            awake_node["value"] = item["data"]["timeInWake"]

            log_nodes = [light_node, deep_node, rem_node, awake_node]
            text = self._create_text(log_nodes)
            raw_log = self._create_log(user_id, text, root_slug, log_nodes, source, start, end)
            raw_logs.append(raw_log)

        return raw_logs
