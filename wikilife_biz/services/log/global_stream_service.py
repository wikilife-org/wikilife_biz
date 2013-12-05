'''
Created on Nov 7, 2012

@author: hugo
'''
#from wikilife_data.namespace import NameSpace

GLOBAL_STREAM_FIELDS = ['exercise', 'update_datetime', 'text', 'source', 'nodes', 'category', 'user_id']


class GlobalStreamService():

    def __init__(self, logger, final_log_dao, meta_dao, profile_dao, question_dao):
        self._final_log_dao = final_log_dao
        self._meta_dao = meta_dao
        self._profile_dao = profile_dao
        self._question_dao = question_dao

    def get_logs_in_range(self, from_date, to_date):
        return self._final_log_dao.get_logs_in_range(from_date, to_date)

    def get_latest_logs(self, amount):
        return []
    
    """    
    def get_latest_logs(self, amount):
        latest_logs = self._final_log_dao.get_latest_logs(GLOBAL_STREAM_FIELDS, amount)
        for log in latest_logs:
            log["text"] = ""
            node = log['nodes'][0]

            # Get stuff from the meta database:
            loggable_name = self._meta_dao.get_node_by_id(node["loggable_id"])["fields"]["title"]
            property_node = self._meta_dao.get_node_by_id(node["property_id"])
            value_node = self._meta_dao.get_node_by_id(node["node_id"])
            parent_ns = NameSpace(value_node['fields']['namespace']).get_parent_namespace().to_str()
            question = self._question_dao.get_question_by_node_ns(parent_ns)

            if question is not None:
                log["name"] = question["fields"]["text"]
                log["text"] = str(node["value"])
                if "unit" in property_node["fields"]:
                    log["text"] += property_node["fields"]["unit"]
            else:
                log["name"] = loggable_name
                node_name = property_node["fields"]["title"]
                log["text"] = " (" + node_name + ": " + str(node["value"])
                if "unit" in property_node["fields"]:
                    log["text"] += property_node["fields"]["unit"]
                log["text"] += ") "
            # format data:

            log["user_gender"] = self._profile_dao.get_field_by_user_id(self._profile_dao.GENDER_ITEM, log["user_id"])
            log["device"] = log["source"].split('.')[-1]

            location = {}
            location["city"] = self._profile_dao.get_field_by_user_id(self._profile_dao.CITY_ITEM, log["user_id"])
            location["country"] = self._profile_dao.get_field_by_user_id(self._profile_dao.COUNTRY_ITEM, log["user_id"])
            log["user_location"] = location
            del(log["user_id"])
        return latest_logs
    """    
