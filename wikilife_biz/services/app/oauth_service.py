# coding=utf-8

from wikilife_utils.hasher import Hasher


class OAuthServiceException(Exception):
    pass


class OAuthService(object):

    _logger = None

    def __init__(self, logger, user_dao, oauth_token_dao, oauth_client_dao):
        self._logger = logger
        self._user_dao = user_dao
        self._oauth_token_dao = oauth_token_dao
        self._oauth_client_dao = oauth_client_dao

    def login(self, user_name, pin):
        token = None
        user = self._user_dao.get_user_by_user_name(user_name)

        if user != None and user["pin"] == pin:
            user_id = user["userId"]
            client_id = "login"
            token = self._create_token()
            code = ""
            self._oauth_token_dao.delete_token(user_id, client_id)
            self._oauth_token_dao.insert_token(user_id, client_id, token, code)

        return token

    def authorize(self, user_id, client_id):
        """
        """
        #Create token and code for user_id and client_id
        token = self._create_token()
        code = self._create_code()
        self._oauth_token_dao.insert_token(user_id, client_id, token, code)
        return (token, code)

    def get_token_for_user(self, user_name, pin):
        token = None
        user = self._user_dao.get_user_by_user_name(user_name)
        if user != None and user["pin"] == pin:
            token = self._oauth_token_dao.get_token_for_user_id(user["userId"])

        return token

    def get_user_for_token(self, token):
        self._validate_token(token)
        return self._oauth_token_dao.get_user_id_for_token(token)

    def get_token_for_code(self, code, client_id):
        self._validate_code(code)
        self._validate_client_id(client_id)
        token = self._oauth_token_dao.get_token_for_code(code, client_id)

        if token != None:
            self._oauth_token_dao.blank_code(code, client_id)

        return token

    def revoke_token(self, token):
        self._validate_token(token)
        return self.oauth_token_dao.delete_token(token)
    
    def _create_token(self):
        token = Hasher.create_pseudo_unique(24)
        
        #check unique
        while(self._oauth_token_dao.get_user_id_for_token(token) != None):
            token = Hasher.create_pseudo_unique(24)

        return token

    def _create_code(self):
        code = Hasher.create_pseudo_unique(24)

        #check unique
        while(self._oauth_token_dao.get_user_id_for_code(code) != None):
            code = Hasher.create_pseudo_unique(24)
        
        return code

    def _validate_token(self, token):
        #TODO improve validation
        if token == None:
            raise OAuthServiceException("Invalid token: %s" % token)

    def _validate_code(self, code):
        #TODO improve validation
        if code == None:
            raise OAuthServiceException("Invalid code: %s" % code)

    def _validate_user_id(self, user_id):
        #TODO improve validation
        if user_id == None:
            raise OAuthServiceException("Invalid user_id: %s" % user_id)

    def _validate_client_id(self, client_id):
        #TODO improve validation
        if client_id == None:
            raise OAuthServiceException("Invalid client_id: %s" % client_id)
