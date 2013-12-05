# coding=utf-8

import hashlib
from datetime import datetime


class SecurityQuestionsServiceException(Exception):
    pass


class SecurityQuestionsService(object):
    """
    Public Security Question Service
    """

    _logger = None
    _user_mgr = None
    _security_question_mgr = None
    _recovery_information_mgr = None
    _user_token_mgr = None
    _profile_mgr = None

    def __init__(self, logger, user_mgr, security_question_mgr, recovery_information_mgr, user_token_mgr, profile_mgr):
        self._logger = logger
        self._recovery_information_mgr = recovery_information_mgr
        self._user_mgr = user_mgr
        self._security_question_mgr = security_question_mgr
        self._user_token_mgr = user_token_mgr
        self._profile_mgr = profile_mgr

    def get_security_questions(self, code):
        sc = []

        if code == "all":
            sc = list(self._security_question_mgr.get_security_questions())
        else:
            sc.append(self._security_question_mgr.get_security_question_by_id(code))

        return sc

    def get_security_questions_with_answers(self, code, user_id):

        sc = self.get_security_questions(code)
        user_info = self._recovery_information_mgr.get_recovery_information_by_user_id(user_id)

        if user_info:
            questions = user_info["security_questions"]
            for s in sc:
                for q in questions:
                    if q["pk"] == s["pk"]:
                        s["answer"] = q["answer"]

        return sc

    def validate_security_questions(self, question_list):
        total = len(question_list)

        if total < 5:
            raise SecurityQuestionsServiceException("Missing security questions, mandatory at least 5, received %s" % total)

        invalid_list = []
        incomplete_answers = []
        for sq in question_list:
            if  not self._security_question_mgr.get_security_question_by_id(sq["pk"]):
                invalid_list.append(sq["pk"])
            if not sq["answer"]:
                incomplete_answers.append(sq["pk"])

        if invalid_list:
            raise SecurityQuestionsServiceException("Invalid security questions: %s" % invalid_list)

        if incomplete_answers:
            raise SecurityQuestionsServiceException("Missing answers for code: %s" % invalid_list)

    def insert_user_recovery_information(self, user_id, device_id, birthdate, security_questions):

        info = {}
        info["user_id"] = user_id
        info["device_id"] = device_id
        info["birthdate"] = birthdate
        self._normalize_answers(security_questions)
        info["security_questions"] = security_questions
        self._recovery_information_mgr.insert_recovery_information(info)

    def update_user_recovery_information(self, user_id, device_id, security_questions):
        usr_rcv_info = self._recovery_information_mgr.get_recovery_information_by_user_id(user_id)
        birthdate = self._get_user_birthdate(user_id)
        if usr_rcv_info:

            usr_rcv_info["birthdate"] = birthdate
            usr_rcv_info["device_id"] = device_id
            self._normalize_answers(security_questions)
            usr_rcv_info["security_questions"] = security_questions

            self._recovery_information_mgr.save_recovery_information(usr_rcv_info)
        else:
            self.insert_user_recovery_information(user_id, device_id, birthdate, security_questions)

    def find_user_recovery_info_with_device_id(self, birthdate, device_id, security_questions):
        #Only  2 corrects
        if device_id:
            self._normalize_answers(security_questions)
            r_info = self._recovery_information_mgr.get_recovery_information_by_device_and_birthdate(device_id, birthdate)

            if not r_info:
                return self.find_user_recovery_info(birthdate, security_questions)

            stored_sc = r_info["security_questions"]

            corrects = 0

            for sc in security_questions:
                if sc in stored_sc:
                    corrects = corrects + 1

            if corrects >= 2:
                user_id = r_info["user_id"]
                user = self._user_mgr.get_user_by_id(user_id)
                user_name = user["user_name"]
                token = self._generate_token(datetime.now())

                self._insert_token(user_id, token, datetime.utcnow())

                return {"user_id": user_id, "user_name": user_name, "token": token}
            else:
                raise  SecurityQuestionsServiceException("INVALID_ANSWERS")

        else:
            return self.find_user_recovery_info(birthdate, security_questions)

    def find_user_recovery_info(self, birthdate, security_questions):
        #Only 3 corrects

        r_infos = list(self._recovery_information_mgr.get_recovery_information_birthdate(birthdate))

        self._normalize_answers(security_questions)
        l_r_infos = len(r_infos)
        corrects = 0
        index = 0

        while corrects < 3 and index < l_r_infos:
            corrects = 0
            r_info = r_infos[index]
            stored_sc = r_info["security_questions"]
            for sc in security_questions:
                if sc in stored_sc:
                    corrects = corrects + 1
            index = index + 1

        if corrects >= 3:
            user_id = r_info["user_id"]
            user = self._user_mgr.get_user_by_id(user_id)
            token = self._generate_token(datetime.now())

            self._insert_token(user_id, token, datetime.utcnow())

            return {"user_id": user_id, "user_name": user["user_name"], "token": token}
        else:

            raise SecurityQuestionsServiceException("INVALID_ANSWERS")

    def reset_user_credentials(self, user_id, token, new_username, new_pin):
        if self._validate_token(user_id, token):
            self._update_user_credentials(user_id, new_username, new_pin)
        else:
            raise SecurityQuestionsServiceException("Invalid token")

    def _generate_token(self, arg):
        return hashlib.sha224(str(arg)).hexdigest()

    def _delete_token(self, user_id, token):
        self._user_token_mgr.remove(user_id, token)

    def _insert_token(self, user_id, token, creation_date=datetime.utcnow()):
        self._user_token_mgr.insert_token(user_id, token, creation_date)

    def _validate_token(self, user_id, token):
        is_valid = False
        user_token = self._user_token_mgr.get_token(user_id, token)
        if user_token:
            delta = datetime.utcnow() - user_token["created_date"]
            is_valid = delta.seconds <= 310
        return is_valid

    def _get_user_birthdate(self, user_id):
        profile = self._profile_mgr.get_profile_by_user_id(user_id)
        item = profile["items"]["birthdate"]

        birthdate = item["value"]
        if len(birthdate) > 10:
            birthdate = birthdate[:10]
        return birthdate

    def _update_user_credentials(self, user_id, new_username, new_pin):
        user = self._user_mgr.get_user_by_id(user_id)
        user["username"] = new_username
        user["pin"] = new_pin
        self._user_mgr.save_user(user)

    def _normalize_answers(self, security_questions):
        for sc in security_questions:
            sc["answer"] = sc["answer"].lower().strip()
            sc["pk"] = sc["pk"].upper().strip()
