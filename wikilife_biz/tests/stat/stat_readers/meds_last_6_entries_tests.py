# coding=utf-8

from wikilife_data.managers.stats.stats_manager import StatsManager
from wikilife_data.managers.reports.reports_manager import ReportsManager
from wikilife_data.managers.meta.meta_manager import MetaManager

from wikilife_stat_service.stat_readers.meds_last_6_entries import MedsLastSixEntries
from wikilife_stat_service.tests.base_test import BaseTest
from wikilife_stat_service.utils.managers import Managers


class MedsLastSixEntriesTests(BaseTest):

    db = None
    stats_mgr = None
    meta_mgr = None
    reports_mgr = None
    reader = None

    def setUp(self):
        self.db = self.get_conn().test_meds_last_six_entries
        self.get_conn().drop_database("test_meds_last_six_entries")

        logger = self.get_logger()
        self.stats_mgr = StatsManager(logger, self.db)
        self.meta_mgr = MetaManager(logger, self.db)
        self.reports_mgr = ReportsManager(logger, self.db)

        managers = Managers(self.meta_mgr, self.stats_mgr, self.reports_mgr, None)

        self.reader = MedsLastSixEntries(logger, managers)

    def tearDown(self):
        self.get_conn().drop_database("test_meds_last_six_entries")

    def test_read_stat(self):

        self._create_test_data()
        user_id = "test1"
        node_id = 316699

        stats = self.reader.read_stat(user_id, "2012-05-05", node_id)
        data = stats[1]

        for stat in data:
            assert stat["strength"] == "180Mg"

        assert len(data) == 6

    """ helpers """

    def _create_test_data(self):
        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "2012-01-01"
        report["time"] = "10:10:10"
        report["log_id"] = 999

        report["strength"] = "180Mg"
        self.reports_mgr.save_medical_drugs_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "2012-02-02"
        report["time"] = "10:10:10"
        report["log_id"] = 888
        report["strength"] = "180Mg"
        self.reports_mgr.save_medical_drugs_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "2012-03-03"
        report["time"] = "10:10:10"
        report["log_id"] = 777
        report["strength"] = "180Mg"
        self.reports_mgr.save_medical_drugs_report(report)
        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "2012-04-04"
        report["time"] = "10:10:10"
        report["log_id"] = 666
        report["strength"] = "180Mg"
        self.reports_mgr.save_medical_drugs_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "2012-05-05"
        report["time"] = "10:10:10"
        report["log_id"] = 555
        report["strength"] = "180Mg"
        self.reports_mgr.save_medical_drugs_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "2012-06-06"
        report["time"] = "10:10:10"
        report["log_id"] = 444
        report["strength"] = "180Mg"
        self.reports_mgr.save_medical_drugs_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "2012-07-07"
        report["time"] = "10:10:10"
        report["log_id"] = 333
        report["strength"] = "180Mg"
        self.reports_mgr.save_medical_drugs_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "1999-01-01"
        report["time"] = "10:10:10"
        report["log_id"] = 222
        report["strength"] = "180Mg"
        self.reports_mgr.save_medical_drugs_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "1999-01-02"
        report["time"] = "10:10:10"
        report["log_id"] = 111
        report["strength"] = "180Mg"
        self.reports_mgr.save_medical_drugs_report(report)

        #========== Test Record ============================

        report = {}
        report["user_id"] = "test1"
        report["node_id"] = 316699
        report["date"] = "1999-01-03"
        report["time"] = "10:10:10"
        report["log_id"] = 100
        report["strength"] = "180Mg"
        self.reports_mgr.save_medical_drugs_report(report)

        #========== Test Record ============================
