# coding=utf-8

from wikilife_data.dao.questions.answer_dao import ACTIVE, SKIP
from wikilife_biz.services.question.answer_template_renderer import \
    AnswerTemplateRenderer
from wikilife_utils.data_formatter import DataFormatter
from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_utils.parsers.str_parser import StrParser
from wikilife_utils.validators.node_value_validator import NodeValueValidator
import datetime


class QuestionServiceException(Exception):
    pass


class QuestionService(object):
    """
    Public Business Service
    """

    _meta_dao = None
    _user_dao = None
    _question_dao = None
    _questions_tag_dao = None
    _answer_dao = None
    _log_srv = None
    _stat_srv = None
    _condition_iptr = None
    _tpl_rndr = None
    _node_validator = None

    def __init__(self, logger, meta_dao, user_dao, question_dao, questions_tag_dao, answer_dao, log_service, stat_service, condition_interpreter):
        self._logger = logger
        self._meta_dao = meta_dao
        self._user_dao = user_dao
        self._question_dao = question_dao
        self._questions_tag_dao = questions_tag_dao
        self._answer_dao = answer_dao
        self._log_srv = log_service
        self._stat_srv = stat_service
        self._condition_iptr = condition_interpreter
        self._tpl_rndr = AnswerTemplateRenderer()
        self._node_validator = NodeValueValidator(meta_dao)

    def get_questions_tags(self):
        return self._questions_tag_dao.get_questions_tags_code()

    def get_questions_by_tag(self, tag):
        return self._question_dao.get_questions_by_tag(tag)

    def get_next_question(self, user_id, tag):
        """

        """
        self._validate_user(user_id)
        cursor = self._question_dao.get_questions(tag)

        for question in cursor:
            if self._is_question_for_user(user_id, question):
                question_dto = self._prepare_question_dto(question)
                return question_dto

    #TODO name not apply
    def get_categories(self, user_id):
        self._validate_user(user_id)
        categs = []
        cursor = self._questions_tag_dao.get_questions_tags()

        for question_tag in cursor:
            categ = {}
            categ["tag"] = question_tag["tag"]
            categ["total_questions"], categ["pending_questions"] = self._count_user_questions_by_tag(user_id, question_tag["tag"])
            categs.append(categ)

        return categs

    def _is_question_for_user(self, user_id, question):
        last_answer = self._answer_dao.get_last_answer(user_id, question["id"])

        return (last_answer == None or self._is_question_in_freq(question, last_answer)) \
                and self._condition_iptr.execute(question["condition"], user_id)

    def _is_question_in_freq(self, question, last_answer):
        freq = question["frequency"]

        #frequency == -1 means question has no frequency / its not repeteable
        if freq == -1:
            return False

        last_execute_date_str = last_answer["execute_time"][:10]
        last_execute_date = StrParser.parse_date(last_execute_date_str)
        next_execute_date = last_execute_date + datetime.timedelta(days=freq)
        return next_execute_date <= datetime.datetime.utcnow()

    def _count_user_questions_by_tag(self, user_id, tag):
        cursor = self._question_dao.get_questions(tag)
        pending = 0
        answered = 0

        for question in cursor:
            if self._is_question_for_user(user_id, question):
                pending += 1

            elif self._answer_dao.get_last_answer(user_id, question["id"]) != None:
                answered += 1

        total = pending + answered
        return total, pending

    """
    TODO move to AnswerService
    """

    def get_answer_by_id(self, user_id, answer_id):
        self._validate_user(user_id)
        answer_mo = self._get_answer_mo(answer_id)
        question_mo = self._get_question_mo(answer_mo["question_id"])

        dto = {}
        dto["question"] = self._prepare_question_dto(question_mo)
        dto["answer"] = self._prepare_answer_dto(answer_mo)

        return dto

    def add_answer(self, user_id, answer_dto, answer_type):
        """
        user_id: String,

        answer_dto: dict
            {
                "execute_time": "2012-03-01 12:13:01 -0300",
                "answer_value": "2 unit",
                "question_id": 40,
                "answer_id": 0
            }

        answer_type: int. ACTIVE, SKIP

        returns: dict
            {
            "question": {
                "quesiton_id": 40,
                "text": "How many cigarettes a day do you smoke?",
                "node_id": 241559
            },
            "answer": {
                "execute_time": "2012-03-01 12:13:01 -0300",
                "answer_value": "2 unit",
                "question_id": 40,
                "answer_id": 3
            }
        """
        self._validate_user(user_id)
        question_mo = self._get_question_mo(answer_dto["question_id"])

        answer_value = answer_dto["answer_value"]

        answer_mo = {
            "user_id": user_id,
            "question_id": answer_dto["question_id"],
            "is_last": True,
            "answer_type": answer_type,
            "value": answer_value,
            "execute_time": answer_dto["execute_time"]
        }

        if answer_type == ACTIVE:
            self._node_validator.validate_node_value(answer_value, question_mo["target"])
            log = self._create_answer_raw_log_mo(user_id, question_mo, answer_mo)

            def on_before_publish(inserted_raw_log_id):
                answer_mo["log_id"] = inserted_raw_log_id
                answer_dto["log_id"] = inserted_raw_log_id
                answer_dto["answer_id"] = self._answer_dao.insert_last_answer(answer_mo)

            self._log_srv.add_logs([log], on_before_publish)

        elif answer_type == SKIP:
            answer_mo["log_id"] = 0
            answer_dto["answer_id"] = self._answer_dao.insert_last_answer(answer_mo)

        else:
            raise QuestionServiceException("Unknown answer answer_type: '%s'" % answer_type)

        dto = {}
        dto["stat"] = self._get_stat(answer_dto["question_id"])
        dto["question"] = self._prepare_question_dto(question_mo)
        dto["answer"] = answer_dto

        return dto

    def edit_answer(self, user_id, answer_dto, answer_type):
        """
        user_id: String,

        answer_dto: dict
            {
                "execute_time": "2012-03-01 12:13:01 -0300",
                "answer_value": "2 unit",
                "question_id": 40,
                "answer_id": 3
            }

        answer_type: int. ACTIVE

        returns: dict
            {
            "question": {
                "quesiton_id": 40,
                "text": "How many cigarettes a day do you smoke?",
                "node_id": 241559
            },
            "answer": {
                "execute_time": "2012-03-01 12:13:01 -0300",
                "answer_value": "2 unit",
                "question_id": 40,
                "answer_id": 3
            }
        """
        self._validate_user(user_id)
        answer_mo = self._get_answer_mo(answer_dto["answer_id"])
        question_mo = self._get_question_mo(answer_dto["question_id"])

        if answer_type == ACTIVE:
            log = self._create_answer_raw_log_mo(user_id, question_mo, answer_mo, answer_mo["log_id"])

            def on_before_publish(inserted_raw_log_id):
                answer_mo["value"] = answer_dto["answer_value"]
                answer_mo["execute_time"] = answer_dto["execute_time"]
                answer_mo["log_id"] = inserted_raw_log_id
                self._answer_dao.update_answer(answer_mo)

            self._log_srv.edit_logs([log], on_before_publish)

        elif answer_type == SKIP:
            raise QuestionServiceException("Cannot SKIP while editing an existing answer")

        else:
            raise QuestionServiceException("Unknown answer answer_type: '%s'" % answer_type)

        dto = {}
        dto["stat"] = self._get_stat(answer_dto["question_id"])
        dto["question"] = self._prepare_question_dto(question_mo)
        dto["answer"] = answer_dto

        return dto

    def remove_answer(self, user_id, answer_id):
        """
        user_id: String,
        answer_id: int
        """
        self._validate_user(user_id)
        answer_mo = self._get_answer_mo(answer_id)
        question_mo = self._get_question_mo(answer_mo["question_id"])
        log = self._create_answer_raw_log_mo(user_id, question_mo, answer_mo, answer_mo["log_id"])
        self._answer_dao.delete_answer(answer_id)
        self._log_srv.delete_logs([log])

    def _validate_user(self, user_id):
        """
        user_id: String
        """
        if self._user_dao.get_user_by_id(user_id) == None:
            raise QuestionServiceException("user not valid (%s)" % user_id)

    def _get_answer_mo(self, answer_id):
        answer_mo = self._answer_dao.get_answer_by_id(answer_id)
        if answer_mo == None:
            raise QuestionServiceException("answer id=%s not found" % answer_id)

        return answer_mo

    def _get_question_mo(self, question_id):
        question_mo = self._question_dao.get_question_by_id(question_id)
        if question_mo == None:
            raise QuestionServiceException("question id=%s not found" % question_id)

        return question_mo

    def _create_answer_raw_log_mo(self, user_id, question_mo, answer_mo, log_id=0):
        root_category_name = self._meta_dao.get_root_category(question_mo["target"])["fields"]["slug"]

        node = {}
        node["nodeId"] = question_mo["target"]
        node["value"] = answer_mo["value"]
        text = self._tpl_rndr.render(question_mo["answerTemplate"], str(answer_mo["value"]))

        log = {}
        log["id"] = log_id
        log["source"] = "question-service"
        log["category"] = root_category_name
        log["userId"] = user_id
        log["start"] = answer_mo["execute_time"]
        log["end"] = log["start"]
        log["text"] = text
        log["nodes"] = [node]

        return log

    """
    TODO move to converter
    """

    def _prepare_question_dto(self, question_mo):
        question_dto = {}
        question_dto["question_id"] = question_mo["id"]
        question_dto["text"] = question_mo["statement"]

        #question_dto["node_id"] = self._meta_dao.get_node_by_namespace(question_mo["fields"]["node"] + ".value-node")["pk"]
        question_dto["node_id"] = question_mo["target"]

        return question_dto

    def _prepare_answer_dto(self, answer_mo):
        answer_dto = {}
        answer_dto["answer_id"] = answer_mo["_id"]
        answer_dto["question_id"] = answer_mo["question_id"]
        answer_dto["log_id"] = answer_mo["log_id"]
        answer_dto["execute_time"] = answer_mo["execute_time"]
        answer_dto["answer_value"] = answer_mo["value"]
        return answer_dto

    """
    TODO move to question_stats_service
    """

    def get_stats_by_tag(self, tag, user_id):
        """
        1. All Questions answered for this user with this tag.
        2. Get the stat for each question
        3.Complete the structure:
           [ {
             "question": {
            "quesiton_id": 42,
            "text": "How many cigarettes a day do you smoke?",
            "node_id": 241559
        },
        "answer": {
            "execute_time": "2012-03-01 12:13:01 -0300",
            "answer_value": "2 unit",
            "question_id": 40,
            "answer_id": 3
        },
        "stat":{STAT}

        },... ]


        """
        self._validate_user(user_id)
        questions = self._question_dao.get_questions_by_tag(tag)

        stat_list = []

        for question in questions:
            question_id = question["id"]
            answer = self._answer_dao.get_last_answer(user_id, question_id)
            if answer:
                result = {}
                result["question"] = self._prepare_question_dto(question)
                result["answer"] = self._prepare_answer_dto(answer)
                result["stat"] = self._get_stat(question_id)
                stat_list.append(result)

        return stat_list

    def get_stats_by_question(self, user_id, question_id):
        """
        """
        self._validate_user(user_id)
        question_mo = self._get_question_mo(question_id)

        dto = {}
        dto["stat"] = self._get_stat(question_id)
        dto["question"] = self._prepare_question_dto(question_mo)

        return dto

    def _get_stat(self, question_id):
        kwargs = {"question_id": question_id}
        description, data, custom = self._stat_srv.get_stat_by_id(5, **kwargs)
        stat = DataFormatter(description, data, custom).google_visualization()

        return JSONParser.to_collection(stat)
