# coding=utf-8

from wikilife_biz.services.stat.stat_readers.base_stat_reader import \
    BaseStatReader
from wikilife_utils.date_utils import DateUtils


class InternalStatsReader(BaseStatReader):

    def read_stat(self):
        current_date_utc = DateUtils.get_datetime_utc()

        data = {}
        data["users"] = self._get_global_user_stats(current_date_utc)
        data["logs"] = self._get_global_log_stats(current_date_utc)

        return {
            "data": data
        }

    def _get_global_user_stats(self, current_utc):
        """
                    Total    Yesterday
        Users
        All:      470471        11
        WL Apps:      989        0
        External:      469482        11
        Active:      20782        271
        """

        user_dao = self._daos.user_dao
        aggregation_dao = self._daos.aggregation_node_dao

        date_to = DateUtils.create_datetime(current_utc.year, current_utc.month, current_utc.day)
        date_from = DateUtils.add_days(date_to, -1)
        date_from_lastmonth = DateUtils.add_days(date_to, -30)

        yesterday_human_users = user_dao.count_users(auto=False, create_utc_from=date_from, create_utc_to=date_to)
        yesterday_auto_users = user_dao.count_users(auto=True, create_utc_from=date_from, create_utc_to=date_to)
        yesterday_users = yesterday_human_users + yesterday_auto_users  

        total_human_users = user_dao.count_users(auto=False)
        total_auto_users = user_dao.count_users(auto=True)
        total_users = total_human_users + total_auto_users

        lastmonth_active_users = aggregation_dao.count_active_users(date_from_lastmonth, date_to)
        yesterday_active_users = aggregation_dao.count_active_users(date_from, date_to)

        data = {}
        data["all"] = {"total": total_users, "yesterday": yesterday_users}
        data["wlApps"] = {"total": total_human_users, "yesterday": yesterday_human_users}
        data["external"] = {"total": total_auto_users, "yesterday": yesterday_auto_users}
        data["active"] = {"lastmonth": lastmonth_active_users, "yesterday": yesterday_active_users}

        return data

    def _get_global_log_stats(self, current_utc):
        """
                    Total    Yesterday
        Logs
        All:      2787747        74
        mood:      1405        0
        education:      7        0
        physiological:      2261        0
        exercise:      1497265        41
        ...
        """

        LV_NODE_ID = 1

        meta_dao = self._daos.meta_dao
        aggregation_dao = self._daos.aggregation_node_dao

        date_to = DateUtils.create_datetime(current_utc.year, current_utc.month, current_utc.day)
        date_from = DateUtils.add_days(date_to, -1)

        data = []
        node_id_map = {}

        for node in meta_dao.get_children(LV_NODE_ID):
            item = {"id": node._id, "name": node.name, "yesterday": 0, "total": 0}
            data.append(item)
            node_id_map[node._id] = item

        for item in aggregation_dao.count_logged_nodes(node_id_map.keys(), date_from, date_to):
            node_id_map[int(item["_id"])]["yesterday"] = int(item["value"])

        for item in aggregation_dao.count_logged_nodes(node_id_map.keys()):
            node_id_map[int(item["_id"])]["total"] = int(item["value"])

        return data