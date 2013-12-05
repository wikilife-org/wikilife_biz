# coding=utf-8

import re


ID_INVALID_CHARS_PATTERN = re.compile("[^a-z0-9\\-_]")


class TagServiceException(Exception):
    pass


class TagService(object):

    def __init__(self, logger, tag_manager):
        self._logger = logger
        self._tag_mgr = tag_manager

    def create_tag(self, name):
        """
        name: str. Friendly Name
        Returns created tag
        """
        tag_id = self._create_code(name)
        if self.get_tag_by_id(tag_id) != None:
            raise TagServiceException("tag id already exists: {}".format(tag_id))

        self._tag_mgr.create_tag(tag_id, name)
        return self.get_tag_by_id(tag_id)

    def get_or_create_tag(self, name):
        """
        name: str. Friendly Name
        Returns {} if the tag existed, or the created tag if it did not
        """
        tag_id = self._create_code(name)
        tag = self.get_tag_by_id(tag_id)
        if not tag:
            tag = self.create_tag(name)
        return tag

    def remove_tag_by_id(self, tag_id):
        """
        tag_id: str
        Returns deleted tag
        """
        tag = self.get_tag_by_id(tag_id)
        if tag == None:
            raise TagServiceException("tag id not found: {}".format(tag_id))

        self._tag_mgr.delete_tag_by_id(tag_id)
        return tag

    def get_tag_by_id(self, tag_id):
        """
        tag_id: str
        Returns {}
        """
        return self._tag_mgr.get_tag_by_id(tag_id)

    def get_tag_by_name(self, name):
        """
        name: str
        Returns {}
        """
        return self._tag_mgr.get_tag_by_name(name)

    '''
    def find_tags(self, name):
        """
        name: str. Friendly Name
        Returns [{}]
        """
        return self._tag_mgr.find_tags(name)
    '''

    def get_all_tags(self):
        return self._tag_mgr.get_all_tags()

    def _create_code(self, tag_name):
        code = tag_name.strip()
        code = code.lower()
        code = "".join(code.split())
        code = code.replace(" ", "_")
        code = re.sub(ID_INVALID_CHARS_PATTERN, "", code)

        if len(code) == 0:
            raise TagServiceException("Cannot generate code from name: {}".format(tag_name))

        return code
