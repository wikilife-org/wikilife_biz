# coding=utf-8
from wikilife_data.managers.stats.daily_stats_manager import DailyStatsManager

from wikilife_stat_service.stat_readers.running_by_date import RunningStats
from wikilife_stat_service.tests.base_test import BaseTest
from wikilife_stat_service.utils.managers import Managers


class RunningStatTest(BaseTest):

    db = None
    stats_mgr = None
    meta_mgr = None
    reports_mgr = None
    reader = None

    def setUp(self):
        self.db = self.get_conn().test_running_by_date
        self.get_conn().drop_database("test_running_by_date")
        logger = self.get_logger()
        self.stats_mgr = DailyStatsManager(logger, self.db)
        managers = Managers(None, None, None, None, self.stats_mgr)
        self.reader = RunningStats(logger, managers)

    def tearDown(self):
        self.get_conn().drop_database("test_running_by_date")

    def test_read_stat(self):

        self._create_test_data()
        stats = self.reader.read_stat("2012-05-05", "2012-05-05")
        data = stats[1]

        for stat in data:
            assert stat["distance"] == 15
            assert stat["duration"] == 15

        assert len(data) == 5

    """ helpers """

    def _create_test_data(self):

        times_of_day = ["MORNING", "MIDDAY", "AFTERNOON", "EVENING", "NIGHT"]

        for timeframe in times_of_day:
            stats = {}
            stats["date"] = "2012-05-05"
            stats["user_id"] = "xxxxx"
            stats["distance"] = 10
            stats["duration"] = 10
            stats["time_of_day"] = timeframe
            stats["count_log"] = 1
            stats["dis_avg"] = stats["distance"]
            stats["dur_avg"] = stats["duration"]
            self.stats_mgr.save_running_velocity_daily_stat(stats)

        for timeframe in times_of_day:
            stats = {}
            stats["date"] = "2012-05-05"
            stats["user_id"] = "xxxxy"
            stats["distance"] = 20
            stats["duration"] = 20
            stats["time_of_day"] = timeframe
            stats["count_log"] = 1
            stats["dis_avg"] = stats["distance"]
            stats["dur_avg"] = stats["duration"]
            self.stats_mgr.save_running_velocity_daily_stat(stats)

        for timeframe in times_of_day:
            stats = {}
            stats["date"] = "2012-09-05"
            stats["user_id"] = "xxxxx"
            stats["distance"] = 100
            stats["duration"] = 100
            stats["time_of_day"] = timeframe
            stats["count_log"] = 1
            stats["dis_avg"] = stats["distance"]
            stats["dur_avg"] = stats["duration"]
            self.stats_mgr.save_running_velocity_daily_stat(stats)
