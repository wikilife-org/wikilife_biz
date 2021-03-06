# coding=utf-8

from wikilife_biz.services.user.user_service import UserServiceException
from wikilife_data.dao.crawler.twitter.twitter_user_dao import INTERNAL_ID_FIELD
from wikilife_biz.services.twitter.delegates.twitter_search_user_delegate import TwitterSearchFilter
from geopy.geocoders import Nominatim
from collections import OrderedDict
import time

import hashlib


class TwitterUserServiceException(Exception):
    pass


class TwitterUserService(object):

    INTERNAL_ID_FIELD = "internal_id"
    TWITTER_ID_HASH_FIELD = "twitter_id_hash"

    def __init__(self, logger, twitter_user_dao, twitter_config_dao, log_dao, final_log_dao, profile_dao, account_service, twitter_search_location, user_dao, oper_queue_publisher):
        self._logger = logger
        self._twitter_user_dao = twitter_user_dao
        self._twitter_config_dao = twitter_config_dao
        self._log_dao = log_dao
        self._final_log_dao = final_log_dao
        self._account_srv = account_service
        self._profile_dao = profile_dao
        self._user_dao = user_dao
        self._oper_queue_publisher = oper_queue_publisher
        self._twitter_search_location = twitter_search_location

    def obtain_twitter_user(self, twitter_id):
        twitter_id_hash = self._create_hash(twitter_id)
        twitter_user = self.find_twitter_user(twitter_id_hash)

        if twitter_user == None:
            twitter_user = self.create_twitter_user(twitter_id)
            time.sleep(10)

        self.obtain_twitter_user_location(twitter_user, twitter_id)
        return twitter_user

    def obtain_twitter_user_location(self, twitter_user, twitter_id):
        #GEt account from internal_id
        LOCATION_MAP = {}
        LOCATION_MAP_COUNT = {}
        self._logger.info( "--------- twitter_user" )
        self._logger.info( twitter_user )
        self._logger.info(twitter_user["internal_id"])
        profile = self._profile_dao.get_profile_by_user_id(str(twitter_user["internal_id"]))
        self._logger.info( "--------- account" )
        self._logger.info(  profile )
        #Check if it has location
        
        """
        
        u'geo': {
            u'type': u'Point',
            u'coordinates': [
                -34.57409579,
                -58.40231352
            ]
        },
        """
        geolocator = Nominatim()

        if not (profile.get("city", None) or profile.get("region", None) \
                    or profile.get("country", None)):
            filter = TwitterSearchFilter(user_id=twitter_id)
            result = self._twitter_search_location.search(filter)

            result_items = result
            print result_items
            for item in result_items:
                if item.get("geo", None):
                    geo_str = "{0}, {1}".format(item["geo"]["coordinates"][0], item["geo"]["coordinates"][1])
                    location = geolocator.reverse(geo_str)

                    city = location.raw["address"].get("city", None)
                    region = location.raw["address"]["state"]
                    country = location.raw["address"]["country"]

                    if region in LOCATION_MAP_COUNT:
                        LOCATION_MAP_COUNT[region]  = LOCATION_MAP_COUNT[region] + 1
                    else:
                        LOCATION_MAP_COUNT[region] = 1
                        LOCATION_MAP[region] = {"region": region, "city":city, "country": country}

            if LOCATION_MAP_COUNT:
                d_sorted_by_value = list(OrderedDict(sorted(LOCATION_MAP_COUNT.items(), key=lambda x: x[1])))
                d_sorted_by_value.reverse()
                region = d_sorted_by_value[0]
                self._logger.info(LOCATION_MAP[region])
                self._account_srv.update_profile(str(twitter_user["internal_id"]), "UTC", "AccountService", LOCATION_MAP[region]["country"], LOCATION_MAP[region]["region"] ,LOCATION_MAP[region]["city"] )


    def get_twitter_users_with_no_location(self, limit=300):
        profiles = self._profile_dao.get_profiles_with_no_location(limit)
        twitter_users = []
        for profile in profiles:
            user = self._user_dao.get_user_by_id(profile["userId"])
            if "tw_" in user["userName"]:
                #Get TwitterUse
                
                internal_twitter_user = self._twitter_user_dao.find_twitter_user_by_id(user["userId"])
                twitter_user = self._twitter_user_dao._db.twitter_users_hash_tmp.find_one({"twitter_id_hash": internal_twitter_user["twitter_id_hash"]})
                twitter_users.append((internal_twitter_user, twitter_user["twitter_id"]))
                
        return twitter_users


    def find_twitter_user(self, twitter_id_hash):
        """
        twitter_id_hash: Hash
        """
        return self._twitter_user_dao.find_twitter_user(twitter_id_hash)

    def create_twitter_user(self, twitter_id):
        """
        Creates an account for a new twitter user.
        twitter_id: Twitter user id
        Returns: created_user
        Raises: UserServiceException
        """

        internal_user_id = None
        created_twitter_user = None

        try:
            twitter_id_hash = self._create_hash(twitter_id)
            user_name_prefix = "tw_"
            internal_user_id = self._account_srv.create_autogenerated_account(user_name_prefix)
            self._twitter_user_dao.create_twitter_user(internal_user_id, twitter_id_hash)
            created_twitter_user = self._twitter_user_dao.find_twitter_user(twitter_id_hash)
            self._tmp(twitter_id, twitter_id_hash)

            self._logger.info(  "CRAETED Twitter USER!" )
            return created_twitter_user

        except UserServiceException, e:
            raise TwitterUserServiceException(e)

        #except UserManagerException, e:
        except Exception, e:
            if internal_user_id:
                self._account_srv.delete_account(internal_user_id)

            if created_twitter_user:
                self._twitter_user_dao.delete_user_by_twitter_id(twitter_id)

            raise UserServiceException(e)

    def get_twitter_settings(self, user_id):
        raise NotImplementedError("TwitterUserService.get_twitter_settings() V4 version not implemented yet")
    '''
    def get_twitter_settings(self, user_id):
        return self._twitter_config_dao.get_twitter_setting(user_id)
    '''

    def set_twitter_settings(self, user_id, twitter_settings):
        raise NotImplementedError("TwitterUserService.set_twitter_settings() V4 version not implemented yet")
    '''
    def set_twitter_settings(self, user_id, twitter_settings):
        self._twitter_config_dao.save_twitter_setting(twitter_settings, user_id)
        if twitter_settings["active"] == True:
            twitter_id = twitter_settings["access_token_key"].partition("-")[0]
            self.set_twitter_user(user_id, twitter_id)
    '''

    def set_twitter_user(self, user_id, twitter_id):
        raise NotImplementedError("TwitterUserService.set_twitter_user() V4 version not implemented yet")
    '''
    def set_twitter_user(self, user_id, twitter_id):
        """
        user_id: String, Wikilife internal user id
        twitter_id: Twitter user id
        """

        twitter_id_hash = self._create_hash(twitter_id)

        self._logger.info('1 - set_twitter_user user_id: "%s",  twitter_id: "%s", twitter_id_hash: "%s"' % (user_id, twitter_id, twitter_id_hash))

        twitter_user = self.find_twitter_user(twitter_id_hash)

        if twitter_user == None:
            self._twitter_user_dao.create_twitter_user(user_id, twitter_id_hash)
            self._tmp(twitter_id, twitter_id_hash)

        else:

            old_user_id = twitter_user[INTERNAL_ID_FIELD]
            if old_user_id != user_id:
                self._logger.info('2 - set_twitter_user  user_id: "%s",   old_autogenerated_user: "%s"' % (user_id, old_user_id))
                self._log_dao.delete_profile_logs(old_user_id)
                self._logger.info('3 - set_twitter_user  user_id: "%s",   old_autogenerated_user: "%s"' % (user_id, old_user_id))
                self._log_dao.update_user_id(old_user_id, user_id)
                self._logger.info('4 - set_twitter_user  user_id: "%s",   old_autogenerated_user: "%s"' % (user_id, old_user_id))
                self._final_log_dao.delete_profile_final_logs(old_user_id)
                self._logger.info('5 - set_twitter_user  user_id: "%s",   old_autogenerated_user: "%s"' % (user_id, old_user_id))
                self._final_log_dao.update_user_id(old_user_id, user_id)
                self._logger.info('6 - set_twitter_user  user_id: "%s",   old_autogenerated_user: "%s"' % (user_id, old_user_id))

                #TODO: workaround para operaciones que se reintentan, la cuenta podría ya haber sido borrada
                try:
                    self._account_srv.delete_account(old_user_id)
                    self._logger.info('7 - set_twitter_user  user_id: "%s",   old_autogenerated_user: "%s"' % (user_id, old_user_id))

                except:
                    self._logger.info('ERROR: set_twitter_user  Remove account Error: user_id: "%s",   old_user: "%s"' % (user_id, old_user_id))

                oper = {"code": "user_merge", "twitter_id_hash": twitter_id_hash, "old_user_id": old_user_id, "user_id": user_id}
                self._logger.info('8 - set_twitter_user  user_id: "%s",   old_autogenerated_user: "%s"' % (user_id, old_user_id))
                self._twitter_user_dao.set_internal_user(twitter_id_hash, user_id)
                self._logger.info('9 - set_twitter_user  user_id: "%s",   old_autogenerated_user: "%s"' % (user_id, old_user_id))
                self._logger.info('10 - set_twitter_user From OperDict  user_id: "%s",   old_autogenerated_user: "%s"' % (oper["user_id"], oper["old_user_id"]))
                self._oper_queue_publisher.publish(oper)
    '''

    def _create_hash(self, twitter_user_id):
        hasher = hashlib.sha256()
        hasher.update(str(twitter_user_id))
        unique_hash = hasher.hexdigest()
        return unique_hash

    def _tmp(self, twitter_id, twitter_id_hash):
        """
        This is temporal (ask CEO)
        """
        self._twitter_user_dao._db.twitter_users_hash_tmp.save({"twitter_id": twitter_id, "twitter_id_hash": twitter_id_hash})
