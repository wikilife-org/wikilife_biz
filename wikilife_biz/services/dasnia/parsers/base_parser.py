# coding=utf-8

from abc import abstractmethod
from wikilife_utils.formatters.date_formatter import DateFormatter


class BaseParser(object):
    """
    Abstract class
    """

    #This requires service restart after deploying meta db
    _nodes_map = None
    _meta_dao = None

    def __init__(self, meta_dao):
        self._meta_dao = meta_dao
        self._nodes_map = {}

    @abstractmethod
    def parse(self, item):
        """
        item: dict
        Returns raw log
        """
        raise NotImplementedError()

    def _create_log(self, user_id, text, category, nodes, source, start, end):
        """
        Creates a raw log
        """
        start_str = DateFormatter.to_datetime(start)
        end_str = DateFormatter.to_datetime(end)

        log = {
            "id": 0,
            "origId": 0,
            "source": source,
            "category": category,
            "userId": user_id,
            "start": start_str,
            "end": end_str,
            "text": text,
            "nodes": nodes
        }

        return log

    def _create_text(self, log_nodes):
        """
        Having nodes: "wikilife.exercise.exercise.running.duration.value-node" and "wikilife.exercise.exercise.running.distance.value-node"
        with values 45 and 5, shpould return: "Running, Duration 45 min, Distance 5 km"

        Note: Nodes must have the same meta root. If not, must be two separate logs.
        """

        value_node = self._get_node_by_id(log_nodes[0]["nodeId"])
        prop_node = self._get_node_by_id(value_node["fields"]["parent"])
        loggable_node = self._get_node_by_id(prop_node["fields"]["parent"])
        text = loggable_node["fields"]["title"]

        for log_node in log_nodes:
            value_node = self._get_node_by_id(log_node["nodeId"])
            prop_node = self._get_node_by_id(value_node["fields"]["parent"])
            unit = str(value_node["fields"]["properties"]["value_unit"])
            prop = str(prop_node["fields"]["title"])
            value = str(log_node["value"])
            text += ", %s %s %s" % (prop, value, unit)

        return text

    def _get_node_by_id(self, node_id):
        if not node_id in self._nodes_map:
            self._nodes_map[node_id] = self._meta_dao.get_node_by_id(node_id)

        return self._nodes_map[node_id]
