# coding=utf-8

from wikilife_biz.services.stat.stat_readers.was2.global_aggregated_logs_reader import GlobalAggregatedLogsReader
from wikilife_utils.date_utils import DateUtils

class SocialReader(GlobalAggregatedLogsReader):

    def read_stat(self):
        to_date = DateUtils.get_datetime_utc()
        from_date = DateUtils.add_days(to_date, -7)
        data = {}
        data["Facebook.Friends"]     = self._read_social_lv(node_id=216818, metric_id=216810, from_date=from_date, to_date=to_date) 
        data["Facebook.Posts"]       = self._read_social_lv(node_id=216818, metric_id=216807, from_date=from_date, to_date=to_date) 
        data["Facebook.Likes given"] = self._read_social_lv(node_id=216818, metric_id=216805, from_date=from_date, to_date=to_date) 
        data["Twitter.Followers"]    = self._read_social_lv(node_id=216819, metric_id=216798, from_date=from_date, to_date=to_date) 
        data["Twitter.Tweets"]       = self._read_social_lv(node_id=216819, metric_id=216811, from_date=from_date, to_date=to_date) 
        data["Twitter.Retweets"]     = self._read_social_lv(node_id=216819, metric_id=216802, from_date=from_date, to_date=to_date) 
        data["Gmail.Contacts"]       = self._read_social_lv(node_id=216820, metric_id=216801, from_date=from_date, to_date=to_date) 
        data["Foursquare.Friends"]   = self._read_social_lv(node_id=216821, metric_id=216799, from_date=from_date, to_date=to_date) 
        data["LinkedIn.Connections"] = self._read_social_lv(node_id=3176, metric_id=3171, from_date=from_date, to_date=to_date) 

        return {
         "from": from_date, 
         "to": to_date,
         "data": data
        }

    def _read_social_lv(self, node_id, metric_id, from_date, to_date):
        avg = self._read_numeric(node_id, metric_id, from_date, to_date)

        return {
         "nodeId": node_id,
         "metricId": metric_id,
         "avg": avg
        }
