# coding=utf-8

from wikilife_biz.services.meta.meta_service import MetaService
from wikilife_biz.services.meta.tag_service import TagService
from wikilife_biz.utils.base_service_builder import BaseServiceBuilder
from wikilife_biz.services.meta.converter import Converter


class MetaServiceBuilder(BaseServiceBuilder):

    def build_meta_service(self):
        meta_dao = self._dao_bldr.build_live_meta_dao()
        converter = Converter()
        return MetaService(self._logger, meta_dao, converter)

    def build_tag_service(self):
        tag_dao = self._dao_bldr.build_tag_dao()
        return TagService(self._logger, tag_dao)
