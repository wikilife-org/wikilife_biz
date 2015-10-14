# coding=utf-8

from datetime import timedelta
#from wikilife_data.managers.timeline.timeline_manager import \
#    UPDATE_DATETIME_UTC_FIELD
from wikilife_utils.date_utils import DateUtils
import datetime

MAX_SYNC_ITEMS = 180
DAYS_COUNT = 7
#DAYS_COUNT = 30
#MAX_RESULTS = 20
PAST = "past"
FUTURE = "future"


class TimelineServiceException(Exception):
    pass


class TimelineService(object):
    """
    Public Business Service
    User Timeline Reader
    """
    _timeline_mgr = None
    _reports_mgr = None

    def __init__(self, logger, timeline_manager, reports_manager):
        self._logger = logger
        self._timeline_mgr = timeline_manager
        self._reports_mgr = reports_manager

    def get_user_timeline(self, user_id, categories=None, from_date=None, direction=None):
        """
        user_id: String
        categories=None: List
        from_date=None: Date
        direction: String. Use PAST, FUTURE constants


        PAST,  FUTURE
        Devuelve 7 días con logs (pasado o futuro). O sea cada día es un registro del timeline, no un día calendario.
        from_date es excluido.

        Ejemplo:
        para un timeline con days:
        1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 18, 24, 25, 27, 28, 29, 30

        from_date=10, direction=”past”
        devuelve: 9, 7, 6, 4, 3, 2, 1

        from_date=10, direction=”future”
        devuelve: 28, 27, 25, 24, 18, 12, 11

        PRESENT
        Devuelve 14 dias (registro) desde hoy (inclusive) hacia pasado.

        Ejemplo:
        para un timeline con days:
        1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 18, 24, 25, 27, 28, 29, 30

        from_date=None, direction=None
        siendo hoy dia 28
        devuelve: 28, 27, 25, 24, 18, 12, 11, 10, 9, 7, 6, 4, 3, 2
        """

        if from_date == None:
            from_date = datetime.datetime.utcnow() + timedelta(days=1)
            user_timeline = self._timeline_mgr.get_user_timeline_before(user_id, from_date, DAYS_COUNT * 2, categories)

        elif direction == PAST or direction == None:
            user_timeline = self._timeline_mgr.get_user_timeline_before(user_id, from_date, DAYS_COUNT, categories)

        elif direction == FUTURE:
            user_timeline = self._timeline_mgr.get_user_timeline_after(user_id, from_date, DAYS_COUNT, categories)

        else:
            raise TimelineServiceException("Invalid direction '%s'" % direction)

        return user_timeline

    def get_user_timeline_with_daily_stats(self, user_id, categories=None, from_date=None, direction=None):

        if from_date == None:
            from_date = datetime.datetime.utcnow() + timedelta(days=1)

        user_timeline = self.get_user_timeline(user_id, categories, from_date, direction)
        before_date = from_date.isoformat()[:10]
        #Moods Stats
        mood_reports = self._reports_mgr.get_moods_reports(user_id, before_date, limit=14)
        mood_dict = self._process_mood_daily_stat(mood_reports)

        #Drugs Stats
        drug_reports = self._reports_mgr.get_medical_drugs_reports(user_id, before_date, limit=14)
        drug_dict = self._process_drug_daily_stat(drug_reports)

        #Complaints Stats
        complaint_reports = self._reports_mgr.get_complaints_reports(user_id, before_date, limit=14)
        complaint_dict = self._process_complaint_daily_stat(complaint_reports)

        #Foods Stats
        food_reports = self._reports_mgr.get_foods_reports(user_id, before_date, limit=14)
        food_dict = self._process_nutrition_daily_stat(food_reports)

        for timeline_day in user_timeline:
            t_date = timeline_day["date"]
            timeline_day["stats"] = {}
            try:
                timeline_day["stats"]["mood"] = {"avg": mood_dict[t_date]}
            except KeyError:
                #No mood for that day
                pass
            try:
                timeline_day["stats"]["med_drug"] = {"log_count": drug_dict[t_date]["log_count"]}
            except KeyError:
                #No drug for that day
                pass
            try:
                timeline_day["stats"]["complaint"] = {"log_count": complaint_dict[t_date]["log_count"]}
            except KeyError:
                #No complaint for that day
                pass
            try:
                timeline_day["stats"]["nutrition"] = {
                    "log_count": food_dict[t_date]["log_count"],
                    "calories": food_dict[t_date]["calories"]
                }
            except KeyError:
                #No complaint for that day
                pass

        return user_timeline

    def _process_mood_daily_stat(self, mood_reports):
        mood_dict = {}

        if mood_reports:
            log_count = 0
            total_mood = 0
            aux_date = mood_reports[0]["date"]
            mood_dict[aux_date] = {}

            for report in mood_reports:

                if report["date"] != aux_date:

                    mood_dict[aux_date] = total_mood / log_count
                    aux_date = report["date"]
                    log_count = 0
                    total_mood = 0
                    mood_dict[aux_date] = {}

                log_count = log_count + 1
                total_mood = total_mood + report["intensity"]

        return mood_dict

    def _process_drug_daily_stat(self, drug_reports):
        drug_dict = {}

        if drug_reports:
            log_count = 0
            aux_date = drug_reports[0]["date"]
            drug_dict[aux_date] = {}

            for report in drug_reports:

                if report["date"] != aux_date:
                    drug_dict[aux_date]["log_count"] = log_count
                    aux_date = report["date"]

                    log_count = 0
                    drug_dict[aux_date] = {}

                log_count = log_count + 1

            drug_dict[aux_date]["log_count"] = log_count
        return drug_dict

    def _process_complaint_daily_stat(self, complaint_reports):
        complaint_dict = {}

        if complaint_reports:
            log_count = 0
            aux_date = complaint_reports[0]["date"]
            complaint_dict[aux_date] = {}

            for report in complaint_reports:

                if report["date"] != aux_date:
                    complaint_dict[aux_date]["log_count"] = log_count
                    aux_date = report["date"]

                    log_count = 0
                    complaint_dict[aux_date] = {}

                log_count = log_count + 1

            complaint_dict[aux_date]["log_count"] = log_count
        return complaint_dict

    def _process_nutrition_daily_stat(self, food_reports):
        food_dict = {}

        if food_reports:
            log_count = 0
            total_calories = 0
            aux_date = food_reports[0]["date"]
            food_dict[aux_date] = {}

            for report in food_reports:

                if report["date"] != aux_date:
                    food_dict[aux_date]["log_count"] = log_count
                    food_dict[aux_date]["calories"] = int(total_calories)

                    aux_date = report["date"]
                    food_dict[aux_date] = {}
                    log_count = 0
                    total_calories = 0

                log_count = log_count + 1
                total_calories = total_calories + report["nutrients"]["ENERC_KCAL"]["value"]

            food_dict[aux_date]["log_count"] = log_count
            food_dict[aux_date]["calories"] = int(total_calories)

        return food_dict

    def sync_user_timeline(self, user_id, client_last_sync_datetime_utc=None):
        """
        Sync is performed by push/pull.
        Push is performed by adding logs (LogService).
        This method provides the pull operation.

        user_id: String
        client_last_sync_datetime_utc=None: Date

        Returns: {
            items: [{user_timeline_mo}],
            sync_datetime_utc: datetimeUTC,
            has_more: Boolean
        }
        """

        if client_last_sync_datetime_utc == None:
            from_update_datetime_utc = DateUtils.get_zero_datetime()

        else:
            from_update_datetime_utc = client_last_sync_datetime_utc

        items, total = self._timeline_mgr.get_user_timeline_by_update_time_after(user_id, from_update_datetime_utc, MAX_SYNC_ITEMS)

        """if len(items) > 0:
            sync_datetime_utc = items[-1][UPDATE_DATETIME_UTC_FIELD]
        else:
            sync_datetime_utc = client_last_sync_datetime_utc"""
        
        sync_datetime_utc = client_last_sync_datetime_utc
        dto = {}
        dto["items"] = items
        dto["sync_datetime_utc"] = sync_datetime_utc
        dto["has_more"] = len(items) < total

        return dto
