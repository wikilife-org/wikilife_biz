# coding=utf-8

from wikilife_data.managers.stats.stats_manager import StatsManager
from wikilife_data.managers.reports.reports_manager import ReportsManager
from wikilife_data.managers.meta.meta_manager import MetaManager

from wikilife_stat_service.stat_readers.mood_last_5_entries import MoodLastFiveEntries
from wikilife_stat_service.tests.base_test import BaseTest
from wikilife_stat_service.utils.managers import Managers


class MoodLastFiveEntriesTests(BaseTest):

    db = None
    stats_mgr = None
    meta_mgr = None
    reports_mgr = None
    reader = None

    def setUp(self):
        self.db = self.get_conn().MoodLastFiveEntries
        self.get_conn().drop_database("test_moods_last_five_entries")

        logger = self.get_logger()
        self.stats_mgr = StatsManager(logger, self.db)
        self.meta_mgr = MetaManager(logger, self.db)
        self.reports_mgr = ReportsManager(logger, self.db)

        managers = Managers(self.meta_mgr, self.stats_mgr, self.reports_mgr, None)

        self.reader = MoodLastFiveEntries(logger, managers)

    def tearDown(self):
        self.get_conn().drop_database("test_moods_last_five_entries")

    def test_read_stat(self):

        self._create_test_data()
        user_id = "test1"
        node_id = 316699

        stats = self.reader.read_stat(user_id, "2012-05-05", node_id)
        data = stats[1]

        for stat in data:
            assert stat["intensity"] == 2

        assert len(data) == 5

    """ helpers """

    def _create_test_data(self):
        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "2012-01-01"
        report["time"] = "10:10:10"
        report["log_id"] = 999

        report["intensity"] = 2
        self.reports_mgr.save_moods_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "2012-02-02"
        report["time"] = "10:10:10"
        report["log_id"] = 888
        report["intensity"] = 2
        self.reports_mgr.save_moods_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "2012-03-03"
        report["time"] = "10:10:10"
        report["log_id"] = 777
        report["intensity"] = 2
        self.reports_mgr.save_moods_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "2012-04-04"
        report["time"] = "10:10:10"
        report["log_id"] = 666
        report["intensity"] = 2
        self.reports_mgr.save_moods_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "2012-05-05"
        report["time"] = "10:10:10"
        report["log_id"] = 555
        report["intensity"] = 2
        self.reports_mgr.save_moods_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "2012-06-06"
        report["time"] = "10:10:10"
        report["log_id"] = 444
        report["intensity"] = 2
        self.reports_mgr.save_moods_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "2012-07-07"
        report["time"] = "10:10:10"
        report["log_id"] = 333
        report["intensity"] = 2
        self.reports_mgr.save_moods_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "1999-01-01"
        report["time"] = "10:10:10"
        report["log_id"] = 222
        report["intensity"] = 2
        self.reports_mgr.save_moods_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "1999-01-02"
        report["time"] = "10:10:10"
        report["log_id"] = 111
        report["intensity"] = 2
        self.reports_mgr.save_moods_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "1999-01-03"
        report["time"] = "10:10:10"
        report["log_id"] = 100
        report["intensity"] = 2
        self.reports_mgr.save_moods_report(report)

        #========== Test Record ============================
