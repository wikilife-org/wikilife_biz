# coding=utf-8

from datetime import datetime
from dateutil.relativedelta import relativedelta


class ConditionInterpreterException(Exception):
    pass


class ConditionInterpreter(object):
    """
    Evaluates a boolean expression
    """

    _meta_mgr = None
    _log_mgr = None
    _profile_mgr = None

    def __init__(self, meta_manager, log_manager, profile_mgr):
        self._meta_mgr = meta_manager
        self._log_mgr = log_manager
        self._profile_mgr = profile_mgr

    def execute(self, boolean_expression, user_id):
        """

        NSs removed
        value("wikilife.profile.personal-info.gender") == "Female"
        count("wikilife.leisure.smoking.tobacco.quantity") == 0
        value("wikilife.profile.personal-info.birthdate") < birthdate(18)


        in favor of IDs

        value(1159) == "Female"
        count(241495) == 0
        value(1157) < birthdate(18)

        """

        def value(vn_id):
            return self._get_last_log_value(user_id, vn_id)

        def profile_value(field_name):
            return self._get_profile_value(user_id, field_name)

        def count(vn_id):
            return self._get_user_log_count(user_id, vn_id)

        def is_female():
            return profile_value("gender") == "Female"

        def is_male():
            return profile_value("gender") == "Male"

        def is_older_than(years):
            return str(datetime.now() - relativedelta(years=years)) >= profile_value("birthdate")

        def is_younger_than(years):
            return str(datetime.now() - relativedelta(years=years)) < profile_value("birthdate")

        def has_logs(vn_id):
            return count(vn_id) > 0

        try:
            return eval(boolean_expression) == True

        except Exception, e:
            print "ERROR: '%s' execute('%s', '%s')" % (e, boolean_expression, user_id)
            raise

    def _get_profile_value(self, user_id, item_slug):
        profile = self._profile_mgr.get_profile_by_user_id(user_id)

        if profile == None:
            raise ConditionInterpreterException("Profile not found, user_id: %s" % user_id)

        if not item_slug in profile["items"]:
            raise ConditionInterpreterException("Profile item '%s' not found, user_id: %s" % (item_slug, user_id))

        return profile["items"][item_slug]["value"]

    """
    def _get_value_node_id(self, namespace):
        #TODO multiple value-nodes scenario will crash
        value_node_ns = NameSpace(namespace).append("value-node")
        value_node = self._meta_mgr.get_node_by_namespace(value_node_ns)
        if value_node == None:
            raise ConditionInterpreterException("ValueNode not found '%s'" %value_node_ns)

        return value_node["pk"]
    """

    def _get_last_log_value(self, user_id, vn_id):
            log = self._log_mgr.get_last_user_log_by_node_id(user_id, vn_id)

            if log != None:
                return self._get_log_value(log, vn_id)
            else:
                return None

    def _get_log_value(self, log, vn_id):
        for log_node in log["nodes"]:
            if log_node["nodeId"] == vn_id:
                return log_node["value"]

    def _get_user_log_count(self, user_id, vn_id):
        return self._log_mgr.get_user_logs_by_node_id(user_id, vn_id).count()
