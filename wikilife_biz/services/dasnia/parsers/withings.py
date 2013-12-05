# coding=utf-8

from wikilife_biz.services.dasnia.parsers.base_parser import BaseParser
from wikilife_utils.parsers.date_parser import DateParser

MEASURE_CATEG = 1
WEIGHT_TYPE = 1
VALID_ATTRIBUTION_MODES = [0, 2]


class Withings(BaseParser):

    def parse(self, user_id, dto):
        raw_logs = []
        root_slug = "exercise"
        source = "dasnia.singly.withings"

        for item in dto:
            if item["data"]["attrib"] in VALID_ATTRIBUTION_MODES and item["data"]["category"] == MEASURE_CATEG:
                start = DateParser.from_timestamp(item["data"]["date"])
                end = start
                weight_measure = self._get_weight_measure(item["data"]["measures"])
                weight_node = {"nodeId": 1140}
                weight_node["value"] = float(weight_measure["value"]) / 1000.0
                log_nodes = [weight_node]
                text = self._create_text(log_nodes)
                raw_log = self._create_log(user_id, text, root_slug, log_nodes, source, start, end)
                raw_logs.append(raw_log)

        return raw_logs

    def _get_weight_measure(self, measure_list):
        for measure in measure_list:
            if measure["type"] == WEIGHT_TYPE:
                return measure
