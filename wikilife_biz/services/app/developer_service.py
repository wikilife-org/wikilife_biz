# coding=utf-8

from wikilife_utils.hasher import Hasher


class DeveloperServiceException(Exception):
    pass


class DeveloperService(object):

    _logger = None

    def __init__(self, logger, developer_dao):
        self._logger = logger
        self._developer_dao = developer_dao

    def validate_developer_credentials(self, developer_name, password):
        """
        username: wikilife developer user name
        password:  wikilife developer password
        """

        developer = self._developer_dao.get_developer(developer_name, password)
        if developer == None:
            raise DeveloperServiceException("Developer Name or password incorrect")
        return developer

    def create_developer(self, developer_name, password, email):
        """
        username: wikilife developer user name
        password: wikilife developer password
        email: wikilife developer email
        """

        if self._developer_dao.get_developer_by_email(email) != None:
            raise DeveloperServiceException("Email already in use:%s" % email)

        if self._developer_dao.get_developer_by_name(developer_name) != None:
            raise DeveloperServiceException("Developer Name already in use: %s" % developer_name)

        developer_id = Hasher.create_pseudo_unique(16)

        while(self._developer_dao.get_developer_by_id(developer_id) != None):
            developer_id = Hasher.create_pseudo_unique(16)

        self._developer_dao.insert_developer(developer_id, developer_name, password, email)
        return self._developer_dao.get_developer_by_id(developer_id)

    def get_session_token(self, developer_id):
        token = Hasher.create_pseudo_unique(16)

        developer = self._developer_dao.get_developer_by_id(developer_id)
        if developer == None:
            raise DeveloperServiceException("Invalid Developer Id: %s" % developer_id)

        while(self._developer_dao.get_session(developer_id, token) != None):
            token = Hasher.create_pseudo_unique(16)

        self._developer_dao.insert_session(developer_id, token)

        return token

    def update_developer(self, developer_id, developer_name, password, email):

        developer = self._developer_dao.get_developer_by_id(developer_id)
        if developer == None:
            raise DeveloperServiceException("Invalid Developer Id: %s" % developer_id)

        developer["developerName"] = developer_name
        developer["password"] = password
        developer["email"] = email

        self._developer_dao.save_developer(developer)

    def get_developer_for_token(self, token):
        return self._developer_dao.get_session_by_token(token)

    def remove_session(self, developer_id, token):
        self._developer_dao.delete_session(developer_id, token)
