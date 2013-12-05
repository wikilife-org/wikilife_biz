# coding=utf-8

from wikilife_stat_service.stat_readers.base_stat_reader import BaseStatReader
from wikilife_utils.stats_utils import StatsUtils


class FoodDailyCaloriesLast14Days(BaseStatReader):

    """
    Reader for Food nodes.
    Search for the last 14 days with at least 1 food entry, it searches from week_id - 35 weeks
    Return the total Calories per day, and total food logs per day
    """
    def read_stat(self, user_id, user_date):

        table_description = {"day": ("date", "Day"), "calories": ("number", "Calories"), "log_count": ("number", "Log Count")}
        table_custom_data = {"stats_name": "Food Daily Calories - Last 14 Days with Entries"}
        table_data = []

        week_id, day_index = StatsUtils.get_wikilife_week_info(user_date)

        stats_manager = self._mgrs.stats_mgr

        final_week = week_id - 35  # Search a month ago max.
        #too complex?

        while week_id >= final_week and len(table_data) <= 14:
            stats_current_week = stats_manager.get_stats(user_id, week_id)
            if stats_current_week:
                while day_index >= 0 and len(table_data) <= 14:
                    total_calories = 0
                    if "foods" in stats_current_week:

                        foods = stats_current_week["foods"][day_index]
                        count = stats_current_week["count_foods"][day_index]

                        if count > 0:
                            for food in foods:
                                total_calories = total_calories + food["nutrients"]["ENERC_KCAL"]["value"]

                            stat = {}
                            exe_date = StatsUtils.get_date_from_week_id(stats_current_week["week_id"], day_index)
                            stat["day"] = (exe_date, exe_date.strftime("%Y-%m-%d"))
                            stat["calories"] = total_calories
                            stat["log_count"] = count
                            table_data.append(stat)

                    day_index = day_index - 1
                day_index = 6
            week_id = week_id - 1

        return (table_description, table_data, table_custom_data)
