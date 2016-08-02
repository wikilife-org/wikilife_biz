# coding=utf-8

from wikilife_biz.services.stat.stat_readers.base_stat_reader import \
    BaseStatReader
from wikilife_data.model.meta import NUMERIC_METRIC_NODE
from wikilife_utils.formatters.date_formatter import DateFormatter


class GlobalAggregatedLogsByDayReader(BaseStatReader):

    def read_stat(self, metric_id, from_date, to_date):

        metric = self._daos.meta_dao.get_node_by_id(metric_id)

        if metric.element_type == NUMERIC_METRIC_NODE:
            data = self._read_numeric(metric_id, from_date, to_date)
        else:
            data = self._read_options(metric_id, from_date, to_date)
        result = []
        for d in data:
            result.append({"date":DateFormatter.to_date(d["_id"]), "avg":d["value"]["avg"], "sum":d["value"]["sum"], "entries":d["value"]["entries"]}) 
        return {
         #"nodeId": node_id,
         "metricId": metric_id,
         "from": DateFormatter.to_date(from_date),
         "to": DateFormatter.to_date(to_date),
         "data": result
        }

        
    def _read_numeric(self, metric_id, from_date, to_date):
        items = self._daos.aggregation_dao.get_life_variable_by_day(metric_id, from_date, to_date)
        return items

    def _read_options(self, node_id, metric_id, from_date, to_date):
        #TODO definition pending
        raise NotImplementedError()
