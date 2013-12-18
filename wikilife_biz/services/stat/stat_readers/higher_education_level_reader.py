# coding=utf-8

from wikilife_biz.services.stat.stat_readers.user_option_last_log_reader import UserOptionLastLogReader


class HigherEducationLevelReader(UserOptionLastLogReader):

    def _get_user_option_last_log_dao(self):
        return self._daos.user_option_last_log_dao.get_instance_for_life_variable_ns("higher_education_level")

    def read_stat(self):
        node_id = 2
        metric_id = 278326
        user_id = ""
        from_date = None
        to_date = None

        return UserOptionLastLogReader.read_stat(self, node_id, metric_id, user_id, from_date, to_date)