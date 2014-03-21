# coding=utf-8

from wikilife_biz.services.stat.stat_readers.base_stat_reader import \
    BaseStatReader
from wikilife_data.model.meta import NUMERIC_METRIC_NODE
from wikilife_utils.formatters.date_formatter import DateFormatter


class GlobalAggregatedLogsReader(BaseStatReader):

    def read_stat(self, node_id, metric_id, from_date, to_date):

        metric = self._daos.meta_dao.get_node_by_id(metric_id)

        if metric.element_type == NUMERIC_METRIC_NODE:
            data = self._read_numeric(node_id, metric_id, from_date, to_date)
        else:
            data = self._read_options(node_id, metric_id, from_date, to_date)

        return {
         "nodeId": node_id,
         "metricId": metric_id,
         "from": DateFormatter.to_date(from_date),
         "to": DateFormatter.to_date(to_date),
         "data": data
        }

    def _read_numeric(self, node_id, metric_id, from_date, to_date):
        items = self._daos.aggregation_dao.get_life_variable_by_day(node_id, metric_id, from_date, to_date)
        return items
        
    def _read_numeric_list(self, node_id, metric_id, from_date, to_date):
        items = self._daos.aggregation_dao.get_life_variable(node_id, metric_id, from_date, to_date)
        return items

    def _read_options(self, node_id, metric_id, from_date, to_date):
        #TODO definition pending
        raise NotImplementedError()
