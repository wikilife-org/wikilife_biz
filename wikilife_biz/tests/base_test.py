# coding=utf-8

from wikilife_data.utils.db_conn import DBConn
from wikilife_data.utils.dao_builder import DAOBuilder
from wikilife_utils.settings.settings_loader import SettingsLoader
import unittest


class BaseTest(unittest.TestCase):

    _settings = None

    def get_settings(self):
        if not self._settings:
            self._settings = SettingsLoader().load_settings("tests")
        return self._settings

    def get_logger(self):
        #return self.get_settings()["LOGGER"]
        return MockLogger()

    def get_db_conn(self):
        db_user = None
        db_pass = None
        return DBConn(self.get_settings()["DB_SETTINGS"], db_user, db_pass)

    def get_dao_builder(self):
        return DAOBuilder(self.get_logger(), self.get_db_conn())


class MockLogger(object):

    def info(self, message):
        print message

    def error(self, message):
        print message
