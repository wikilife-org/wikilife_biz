# coding=utf-8

from wikilife_biz.services.question.condition_interpreter import \
    ConditionInterpreter
from wikilife_biz.services.question.question_service import QuestionService
from wikilife_biz.utils.base_service_builder import BaseServiceBuilder


class QuestionServiceBuilder(BaseServiceBuilder):

    def build_question_service(self, log_srv, stat_srv):
        meta_dao = self._dao_bldr.build_live_meta_dao()
        question_dao = self._dao_bldr.build_live_question_dao()
        questions_tag_dao = self._dao_bldr.build_live_questions_tag_dao()
        user_dao = self._dao_bldr.build_user_dao()
        log_dao = self._dao_bldr.build_log_dao()
        answer_dao = self._dao_bldr.build_answer_dao()
        profile_dao = self._dao_bldr.build_profile_dao()
        condition_iptr = ConditionInterpreter(meta_dao, log_dao, profile_dao)
        return QuestionService(self._logger, meta_dao, user_dao, question_dao, questions_tag_dao, answer_dao, log_srv, stat_srv, condition_iptr)
