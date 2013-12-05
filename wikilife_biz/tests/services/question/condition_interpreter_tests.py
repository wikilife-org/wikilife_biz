# coding=utf-8

from wikilife_biz.services.question.condition_interpreter import ConditionInterpreter
from wikilife_biz.tests.services.question.base_question_test import BaseQuestionTest

TEST_USER_ID = "CKJG3L"


class ConditionInterpreterTest(BaseQuestionTest):

    meta_mgr = None
    log_mgr = None
    condition_iptr = None

    def setUp(self):
        dao_bldr = self.get_dao_builder()
        self.meta_mgr = dao_bldr.build_live_meta_dao()
        self.log_mgr = dao_bldr.build_log_dao()
        profile_mgr = dao_bldr.build_profile_dao()
        self.condition_iptr = ConditionInterpreter(self.meta_mgr, self.log_mgr, profile_mgr)
        self.log_mgr._collection.remove({"test": True})

    def tearDown(self):
        self.log_mgr._collection.remove({"test": True})

    def test_always(self):
        user_id = TEST_USER_ID
        expr = "True"

        assert self.condition_iptr.execute(expr, user_id) == True

    def test_never(self):
        user_id = TEST_USER_ID
        expr = "False"

        assert self.condition_iptr.execute(expr, user_id) == False

    def test_count_zero(self):
        user_id = TEST_USER_ID
        #expr = 'count("wikilife.leisure.general.psychoactives.ever") == 0'
        expr = 'count(317559) == 0'

        assert self.condition_iptr.execute(expr, user_id) == True

    def test_count_one(self):
        user_id = TEST_USER_ID
        self._insert_logs(user_id, 317559, 1)
        expr = 'count(317559) == 1'

        assert self.condition_iptr.execute(expr, user_id) == True

    def test_count_many(self):
        user_id = TEST_USER_ID
        self._insert_logs(user_id, 317559, 3)
        expr = 'count(317559) == 3'

        assert self.condition_iptr.execute(expr, user_id) == True

    """
    def test_has_logs(self):
        pass
    """

    def test_value(self):
        user_id = TEST_USER_ID
        #expr = 'value("wikilife.health.general.gynecology.pregnancy.ever") == "Yes"'
        expr = 'value(317572) == "Yes"'

        assert self.condition_iptr.execute(expr, user_id) == False

    """
    def test_profile_value(self):
        pass
    """

    def test_is_female(self):
        user_id = TEST_USER_ID
        expr = "is_female()"

        assert self.condition_iptr.execute(expr, user_id) == False

    def test_is_male(self):
        user_id = TEST_USER_ID
        expr = "is_male()"

        assert self.condition_iptr.execute(expr, user_id) == True

    def test_is_older_than(self):
        user_id = TEST_USER_ID
        expr = "is_older_than(18)"

        assert self.condition_iptr.execute(expr, user_id) == True

    def test_is_younger_than(self):
        user_id = TEST_USER_ID
        expr = "is_younger_than(18)"

        assert self.condition_iptr.execute(expr, user_id) == False

    """ helpers """

    def _insert_logs(self, user_id, vn_id, count):
        value_node = self.meta_mgr.get_node_by_id(vn_id)

        for i in range(0, count):
            node_id = value_node["pk"]
            log = self._create_log(user_id, node_id, "something")
            self.log_mgr.add_log(log)

    def _create_log(self, user_id, node_id, value):
        return {
            "source": "client.iphone",
            "category": "profile",
            "userId": user_id,
            "start": "2012-03-30 19:15:10 +0000",
            "end":   "2012-03-30 19:15:10 +0000",
            "text": "Gender Male",
            "nodes": [{"nodeId": int(node_id), "value":str(value)}],
            "test": True
        }
