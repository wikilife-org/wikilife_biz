# coding=utf-8

from wikilife_biz.services.stat.stat_readers.base_stat_reader import \
    BaseStatReader
from wikilife_utils.formatters.date_formatter import DateFormatter


class TimesPerWeekReader(BaseStatReader):

    def read_stat(self, node_id, from_date, to_date):

        items = self._daos.aggregation_dao.get_node(node_id, from_date, to_date)

        day_avg_sum = float(0)

        if len(items)>0:
            for item in items:
                day_avg_sum += item["sum"] / item["count"]

            avg = day_avg_sum / len(items) 

        else:
            tpw_avg = 0 

        return {
         "nodeId": node_id,
         "from": DateFormatter.to_date(from_date),
         "to": DateFormatter.to_date(to_date),
         "data": tpw_avg
        }



    def _get_weekly_avg(self, node_id, from_date, to_date):
        """
        weekly average
        """
        result = self._daos.aggregation_dao.get_node(node_id, from_date, to_date)
        rlen = len(result)

        if rlen==0:
            return 0

        #el problema son los días sin logs
        """
        self._day_delta = 7*2 = 14
        logs
        day  value
        6      4
       #7           from_date   w1_start
       #8      
        9      9
       #10     
       #11     
        12     6
       #13          w1_end
        14     3    w2_start
        15     4
        16     5
        17     1
        18     8
        19     1
        20     9   to_date (current date)  w2_end
        """

        #Super makae impl v2
        week_map = {}

        for day in result:
            diff_days = (day["date"] - from_date).days
            week_i = diff_days / 7

            if week_i in week_map:
                week_map[week_i]["day_value"] += self._get_day_value(day)
                week_map[week_i]["day_count"] += 1

            else:
                week_map[week_i] = {}
                week_map[week_i]["day_value"] = self._get_day_value(day)
                week_map[week_i]["day_count"] = 1

        week_avg = 0
        week_count = 0

        for k in week_map.keys():
            week = week_map[k]
            week_avg += float(week["day_value"]) / float(week["day_count"])
            week_count += 1

        current_weekly_avg = week_avg*1.0 / week_count
        return current_weekly_avg
