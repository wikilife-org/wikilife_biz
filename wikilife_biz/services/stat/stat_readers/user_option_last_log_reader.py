# coding=utf-8

from wikilife_biz.services.stat.stat_readers.base_stat_reader import \
    BaseStatReader
from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_data.model.meta import TEXT_METRIC_NODE


class UserOptionLastLogReaderException(Exception):
    pass


class UserOptionLastLogReader(BaseStatReader):

    _user_option_last_log_dao = None

    def _get_user_option_last_log_dao(self):
        pass

    def __get_user_option_last_log_dao(self):
        if self._user_option_last_log_dao == None:
            self._user_option_last_log_dao = self._get_user_option_last_log_dao()

        return self._user_option_last_log_dao 

    def read_stat(self, node_id, metric_id, user_id, from_date, to_date):
        dao = self.__get_user_option_last_log_dao()
        metric = self._daos.meta_dao.get_node_by_id(metric_id)

        if metric.element_type != TEXT_METRIC_NODE:
            raise UserOptionLastLogReaderException("Text Metric required")

        data = {}
        total = 0

        for option in metric.options.split(","):
            option = option.strip()
            count = dao.count_option(option, from_date, to_date)
            data[option] = {"count": count}
            total += count

        if total == 0:
            total = 1 

        user_option = dao.get_option_by_user_id(user_id)

        for k in data:
            option = data[k]
            option["percent"] = option["count"]*100.0 / total

            if user_option!= None and option == user_option["option"]:
                #TODO find a better key name
                option["user"] = True

        return {
         "nodeId": node_id,
         "metricId": metric_id,
         "userId": user_id,
         "from": DateFormatter.to_date(from_date) if from_date else None,
         "to": DateFormatter.to_date(to_date) if from_date else None,
         "data": data
        }
