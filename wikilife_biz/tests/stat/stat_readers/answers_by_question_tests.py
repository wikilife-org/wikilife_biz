# coding=utf-8

from wikilife_stat_service.stat_readers.answers_by_question import \
    AnswersByQuestion
from wikilife_stat_service.tests.base_test import BaseTest


class AnswersByQuestionTest(BaseTest):
    _answers = None
    _rdr = None

    def setUp(self):
        self._answers = self.get_db_conn().get_conn_logs().answers
        self._rdr = AnswersByQuestion(self.get_logger(), self.get_managers())
        self._create_test_data()

    def tearDown(self):
        self._answers.remove({"test": True})
        self._answers = None
        self._rdr = None

    def test_read_stat(self):
        question_id = 1
        stats = self._rdr.read_stat(question_id)

        assert "option" in stats[0]
        assert stats[0]["option"] == ('string', 'Option')
        assert "num_answers" in stats[0]
        assert stats[0]["num_answers"] == ('number', 'Number of Answers')

        assert "users_count" in stats[2]
        assert stats[2]["users_count"] == 3
        assert "stats_name" in stats[2]
        assert stats[2]["stats_name"] == "Answer Stats"

        assert {'option': 'one', 'num_answers': 2} in stats[1]
        assert {'option': 'two', 'num_answers': 1} in stats[1]

    """ helpers """

    def _create_test_data(self):
        sample_answers = [
            {"test": True, "_id": -1, "status": 1, "user_id": "test1", "log_id": 123, "value": "zero", "execute_time": "2012-03-21 14:11:24 -0300", "is_last": False, "type": 1, "question_id": 1},
            {"test": True, "_id": -2, "status": 1, "user_id": "test1", "log_id": 124, "value": "one", "execute_time": "2012-03-21 14:11:24 -0300", "is_last": True, "type": 1, "question_id": 1},
            {"test": True, "_id": -3, "status": 1, "user_id": "test2", "log_id": 125, "value": "one", "execute_time": "2011-03-21 00:00:00 -0300", "is_last": True, "type": 1, "question_id": 1},
            {"test": True, "_id": -4, "status": 1, "user_id": "test3", "log_id": 126, "value": "two", "execute_time": "2012-02-10 00:00:00 -0300", "is_last": True, "type": 1, "question_id": 1},
            {"test": True, "_id": -5, "status": 1, "user_id": "test3", "log_id": 127, "value": "other", "execute_time": "2012-02-11 00:00:00 -0300", "is_last": True, "type": 1, "question_id": 2}
        ]

        for sample_answer in sample_answers:
            self._answers.save(sample_answer)
