# coding=utf-8

from wikilife_data.managers.stats.stats_manager import StatsManager
from wikilife_data.managers.reports.reports_manager import ReportsManager
from wikilife_data.managers.meta.meta_manager import MetaManager

from wikilife_stat_service.stat_readers.complaints_last_30_days import ComplaintsLastThirtyDays
from wikilife_stat_service.tests.base_test import BaseTest
from wikilife_stat_service.utils.managers import Managers


class ComplaintsLastThirtyDaysTest(BaseTest):

    db = None
    stats_mgr = None
    meta_mgr = None
    reports_mgr = None
    reader = None

    def setUp(self):
        self.db = self.get_conn().test_complaints_last_30_days
        self.get_conn().drop_database("test_complaints_last_30_days")

        logger = self.get_logger()
        self.stats_mgr = StatsManager(logger, self.db)
        self.meta_mgr = MetaManager(logger, self.db)
        self.reports_mgr = ReportsManager(logger, self.db)

        managers = Managers(self.meta_mgr, self.stats_mgr, self.reports_mgr, None)

        self.reader = ComplaintsLastThirtyDays(logger, managers)

    def tearDown(self):
        self.get_conn().drop_database("test_complaints_last_30_days")

    def test_read_stat(self):

        self._create_test_data()
        user_id = "test1"
        node_id = 111

        stats = self.reader.read_stat(user_id, "2012-05-05", node_id)
        data = stats[1]

        for stat in data:
            assert stat["intensity"] == 8

        assert len(data) == 4

    """ helpers """

    def _create_test_data(self):
        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 111
        report["date"] = "2012-05-04"
        report["time"] = "10:10:10"
        report["log_id"] = 999
        report["intensity"] = 8
        self.reports_mgr.save_complaints_report(report)
        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 111
        report["date"] = "2012-05-02"
        report["time"] = "10:10:10"
        report["log_id"] = 888

        report["intensity"] = 8
        self.reports_mgr.save_complaints_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 111
        report["date"] = "2012-04-30"
        report["time"] = "10:10:10"
        report["log_id"] = 777
        report["intensity"] = 8
        self.reports_mgr.save_complaints_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 111
        report["date"] = "2012-04-24"
        report["time"] = "10:10:10"
        report["log_id"] = 666
        report["intensity"] = 8
        self.reports_mgr.save_complaints_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 111
        report["date"] = "2012-04-04"
        report["time"] = "10:10:10"
        report["log_id"] = 555
        report["intensity"] = 8
        self.reports_mgr.save_complaints_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 666
        report["date"] = "2012-06-06"
        report["time"] = "10:10:10"
        report["log_id"] = 444

        report["intensity"] = 2
        self.reports_mgr.save_complaints_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 777
        report["date"] = "2012-07-07"
        report["time"] = "10:10:10"
        report["log_id"] = 333

        report["intensity"] = 2
        self.reports_mgr.save_complaints_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 888
        report["date"] = "1999-01-01"
        report["time"] = "10:10:10"
        report["log_id"] = 222
        report["intensity"] = 2

        self.reports_mgr.save_complaints_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 999
        report["date"] = "1999-01-02"
        report["time"] = "10:10:10"
        report["log_id"] = 111
        report["intensity"] = 2

        self.reports_mgr.save_complaints_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 000
        report["date"] = "1999-01-03"
        report["time"] = "10:10:10"
        report["log_id"] = 100
        report["intensity"] = 2

        self.reports_mgr.save_complaints_report(report)

        #========== Test Record ============================
