# coding=utf-8

from wikilife_biz.services.stat.stat_readers.base_stat_reader import \
    BaseStatReader
from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_data.model.meta import NUMERIC_METRIC_NODE


class UserAggregatedLogsReader(BaseStatReader):

    def read_stat(self, node_id, metric_id, from_date, to_date, user_id):

        metric = self._daos.meta_dao.get_node_by_id(metric_id)

        if metric.element_type == NUMERIC_METRIC_NODE:
            data = self._read_user_last_numeric(node_id, metric_id, from_date, to_date, user_id)
        else:
            data = self._read_user_last_options(node_id, metric_id, from_date, to_date, user_id)

        return {
         "nodeId": node_id,
         "metricId": metric_id,
         "userId": user_id,
         "from": DateFormatter.to_date(from_date),
         "to": DateFormatter.to_date(to_date),
         "data": data
        }

    def _read_user_last_numeric(self, node_id, metric_id, from_date, to_date, user_id):
        r = self._daos.aggregation_dao.get_numeric_user_life_variable_last_day(node_id, metric_id, user_id, from_date, to_date)
        return r["sum"]/r["count"] if r else 0

    def _read_user_last_options(self, node_id, metric_id, from_date, to_date, user_id):
        raise NotImplementedError()

