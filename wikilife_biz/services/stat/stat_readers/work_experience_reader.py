# coding=utf-8

from wikilife_biz.services.stat.stat_readers.base_stat_reader import \
    BaseStatReader

AGE_BUCKETS = [
    {"min": 15, "max": 25},
    {"min": 26, "max": 35},
    {"min": 36, "max": 45},
    {"min": 46, "max": 55},
    {"min": 56, "max": 65}
]

class WorkExperienceReader(BaseStatReader):

    _dao = None

    def _get_dao(self):
        if not self._dao:
            self._dao = self._daos.generic_dao.get_instance_for(name="work_experience", indexes=[{"field": "age"}])

        return self._dao

    def read_stat(self):
        dao = self._get_dao()
        data = {}
        data["buckets"] = []
        total_sum = 0

        for bucket in AGE_BUCKETS: 
            item = {}
            item["ageMin"] = bucket["min"]
            item["ageMax"] = bucket["max"]
            where = {"age": {"$gte": item["ageMin"], "$lte": item["ageMax"]}}
            item["experienceAvg"] = dao.get_avg(avg_field="experience", where=where) 
            data["buckets"].append(item)
            total_sum += item["experienceAvg"] 

        data["totalExperienceAvg"] = total_sum*1.0/len(AGE_BUCKETS)

        return {
         "data": data
        }
