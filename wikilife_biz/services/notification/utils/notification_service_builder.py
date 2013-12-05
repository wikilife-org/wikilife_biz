# coding=utf-8

from wikilife_biz.utils.base_service_builder import BaseServiceBuilder
from wikilife_biz.services.notification.notification_service import NotificationService


class NotificationServiceBuilder(BaseServiceBuilder):

    def build_notification_service(self):
        return NotificationService(self._logger)
