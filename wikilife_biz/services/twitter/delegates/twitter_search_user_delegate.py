
# coding=utf-8

from wikilife_biz.services.twitter.delegates.base_twitter_delegate import \
    BaseTwitterDelegate, QueryString

"""

https://github.com/geopy/geopy
>>> from geopy.geocoders import Nominatim
>>> geolocator = Nominatim()
>>> location = geolocator.reverse("52.509669, 13.376294")
>>> print(location.address)
Potsdamer Platz, Mitte, Berlin, 10117, Deutschland, European Union

"""


class TwitterUserLocationException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class TwitterSearchFilter(object):
    """
    https://dev.twitter.com/docs/api/1/get/search
    """


    def __init__(self, user_id, since_id=None, exclude_replies=True):
        self.user_id = user_id
        self.exclude_replies = exclude_replies
        self.since_id = since_id

        
class TwitterUserLocation(BaseTwitterDelegate):
    """
    https://dev.twitter.com/docs/api/1.1/get/search/tweets
    """

    SEARCH_SERVICE_URL = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    def search(self, filter):
        self._validate_search_filter(filter)

        #TODO code review: prefiero hacerlo a mano para tener más control, parámetro por parámetro y su matcheo, ej: qs.add_param_from_obj(filter, "q", "myObjPropname") 
        qs = QueryString()
        qs.add_param_from_obj(filter, "user_id")
        qs.add_param_from_obj(filter, "exclude_replies")
        qs.add_param_from_obj(filter, "since_id")

        response = self.get(TwitterUserLocation.SEARCH_SERVICE_URL, qs)

        return response

    def _validate_search_filter(self, search_filter):
        #TODO improve validation
        if search_filter.user_id == None:
            raise TwitterUserLocationException("user_id param is required")