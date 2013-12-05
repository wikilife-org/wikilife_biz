# coding=utf-8

from wikilife_question_service.question_service import QuestionService
from wikilife_data.managers.questions.question_manager import QuestionManager
from wikilife_data.managers.answers.answer_manager import AnswerManager
from wikilife_data.managers.meta.meta_manager import MetaManager
from wikilife_data.managers.users.user_manager import UserManager
from wikilife_stat_service.stat_service import StatService
import datetime
from wikilife_biz.tests.services.question.base_question_test import BaseQuestionTest

class QuestionServiceTest(BaseQuestionTest):
   
    db = None
    question_srv = None

    def setUp(self):
        logger = self.get_logger()
        self.db = self.get_conn().test_question_service
        self.get_conn().drop_database("test_question_service")
        
        answer_mgr = AnswerManager(logger, self.db)
        question_manager = QuestionManager(logger, self.db)
        meta_manager = MetaManager(logger, self.get_conn().wikilife)
        stat_service = StatService(logger, None, None, None, answer_mgr)
        user_manager = UserManager(logger, self.db)
        self.db.users.save({"pin":"TEST", "user_name":"TEST", "user_id":"TEST"})
        self.question_srv = QuestionService( logger, meta_manager, user_manager, question_manager, None, answer_mgr, None, stat_service, None)

    def tearDown(self):
        self.get_conn().drop_database("test_question_service")

    def test_get_stats_by_tag(self):
        self._create_test_data()
        result = self.question_srv.get_stats_by_tag("Mood", "TEST")
        del result[0]["answer"]["answer_id"]
        assert result == [{'answer': 
                           {'log_id': 15, 'answer_value': u'No', 
                            'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), 
                            'question_id': 22}
                           , 'stat': 
                           {u'p': {u'stats_name': u'Answer Stats'}, 
                            u'rows': [{u'c': [{u'v': u'1'}, {u'v': u'Yes'}]}, 
                                      {u'c': [{u'v': u'4'}, {u'v': u'No'}]}], 
                            u'cols': [{u'type': u'number', u'id': u'num_answers', u'label': u'Number of Answers'},
                                       {u'type': u'string', u'id': u'option', u'label': u'Option'}]}, 
                           'question': {'text': u'What is your hiv status 1?', 'node_id': 251380.0, 'question_id': 22}}]



    def _create_test_data(self):

        sample_answers = [
                          
                          {u'pk': 1, 'status': 1, u'update_date': u'2011-10-24', u'server_id': 1, 'type': 1, u'value': u'No', 'log_id':15,
                           u'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), u'is_last': True, u'user_id': u'TEST', u'question_id': 22},
                          {u'pk': 2, 'status': 1, u'update_date': u'2011-10-24', u'server_id': 2, 'type': 1, u'value': u'Yes','log_id':14,
                            u'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), u'is_last': False, u'user_id': u'TEST', u'question_id': 22},
                          {u'pk': 4, 'status': 1, u'update_date': u'2011-10-24', u'server_id': 4, 'type': 1, u'value': u'I dont know', 'log_id':13,
                            u'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), u'is_last': False, u'user_id': u'TEST', u'question_id': 22},
                          
                          
                          {u'pk': 3, 'status': 1, u'update_date': u'2011-10-24', u'server_id': 3, 'type': 1, u'value': u'No', 'log_id':12,
                            u'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), u'is_last': True, u'user_id': u'X378Q9', u'question_id': 22},
                          {u'pk': 5, 'status': 1, u'update_date': u'2011-10-24', u'server_id': 5, 'type': 1, u'value': u'No', 'log_id':11,
                            u'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), u'is_last': True, u'user_id': u'X258Q9', u'question_id': 22},
                          {u'pk': 6, 'status': 1, u'update_date': u'2011-10-24', u'server_id': 6, 'type': 1, u'value': u'Yes', 'log_id':10,
                            u'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), u'is_last': True, u'user_id': u'X238Q9', u'question_id': 22},
                          {u'pk': 7, 'status': 1, u'update_date': u'2011-10-24', u'server_id': 7, 'type': 1, u'value': u'No', 'log_id':9,
                            u'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), u'is_last': True, u'user_id': u'X248Q9', u'question_id': 22},
                          
                          {u'pk': 8, 'status': 1, u'update_date': u'2011-10-24', u'server_id': 1, 'type': 1, u'value': u'1', 'log_id':8,
                            u'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), u'is_last': True, u'user_id': u'X278Q9', u'question_id': 23},
                          {u'pk': 9, 'status': 1, u'update_date': u'2011-10-24', u'server_id': 2, 'type': 1, u'value': u'2', 'log_id':7,
                            u'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), u'is_last': False, u'user_id': u'X278Q9', u'question_id': 23},
                          {u'pk': 13, 'status': 1, u'update_date': u'2011-10-24', u'server_id': 3, 'type': 1, u'value': u'3', 'log_id':6,
                            u'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), u'is_last': True, u'user_id': u'X378Q9', u'question_id': 23},
                          {u'pk': 24, 'status': 1, u'update_date': u'2011-10-24', u'server_id': 4, 'type': 1, u'value': u'1', 'log_id':5,
                            u'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), u'is_last': False, u'user_id': u'X278Q9', u'question_id': 23},
                          {u'pk': 25, 'status': 1, u'update_date': u'2011-10-24', u'server_id': 5, 'type': 1, u'value': u'2', 'log_id':4,
                            u'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), u'is_last': True, u'user_id': u'X288Q9', u'question_id': 23},
                          {u'pk': 26, 'status': 1, u'update_date': u'2011-10-24', u'server_id': 6, 'type': 1, u'value': u'2', 'log_id':3,
                            u'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), u'is_last': True, u'user_id': u'X288Q9', u'question_id': 23},
                          {u'pk': 27, 'status': 1, u'update_date': u'2011-10-24', u'server_id': 7, 'type': 1, u'value': u'3', 'log_id':2,
                            u'execute_time': datetime.datetime(2011, 10, 24, 22, 38, 53), u'is_last': True, u'user_id': u'X288Q9', u'question_id': 23},
                       
                       
                          ]
        
        sample_questions = [{ "pk" : 22, "model" : "Question", 
                             "fields" :
                                     { "node" : "wikilife.healthcare.event.hiv.status", 
                                      "status" : 1, "tags" : [ "Mood" ], 
                                      "text" : "What is your hiv status 1?", 
                                      "server_id" : 22,  "frequency" : 365, 
                                      "answer" : "The result of my last hiv test was %s" } },
                            { "pk" : 13, "model" : "Question", 
                             "fields" :
                                     { "node" : "wikilife.healthcare.event.hiv.status", 
                                      "status" : 1, "tags" : [ "Mood" ], 
                                      "text" : "What is your hiv status 2?", 
                                      "server_id" : 13,  "frequency" : 365, 
                                      "answer" : "The result of my last hiv test was %s" } },
                              { "pk" : 15, "model" : "Question", 
                             "fields" :
                                     { "node" : "wikilife.healthcare.event.hiv.status", 
                                      "status" : 1, "tags" : [ "Mood" ], 
                                      "text" : "What is your hiv status 3?", 
                                      "server_id" : 15,  "frequency" : 365, 
                                      "answer" : "The result of my last hiv test was %s" } }]
             
        for sample_answer in sample_answers:
            self.db.answers.save(sample_answer)
        
        for sample_question in sample_questions:
            self.db.questions.save(sample_question)