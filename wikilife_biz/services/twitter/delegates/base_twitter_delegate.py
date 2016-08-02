# coding=utf-8
import json
import urllib2
import requests

class QueryString(object):
    
    qs = None
    
    def __init__(self, qs = ""):
        self.qs = qs
    
    def add_param(self, name, value):
        value = str(value)
        value = urllib2.quote(value)
        self.qs += "&" + name + "=" + value
    
    def add_param_from_dict(self, dict, param_name, value_key=None):
        if value_key==None:
            value_key = param_name
        
        if value_key in dict and dict[value_key] != None: 
            self.add_param(param_name, dict[value_key])
    
    def add_param_from_obj(self, obj, param_name, value_key=None):
        if value_key==None:
            value_key = param_name
        
        if hasattr(obj, value_key) and getattr(obj, value_key, None) != None: 
            self.add_param(param_name, getattr(obj, value_key))
    
    def to_str(self):
        return self.qs


class BaseTwitterDelegate(object):

    _bearer_access_token = "AAAAAAAAAAAAAAAAAAAAADN1RQAAAAAAmVtYyNrCtp59urnIfj5u1f5ZEV8%3DECQSxvLGArFNd0SqMtN7uoOLdmqf7A1prf0kzKYMGY"


    def get(self, url, query_string, parse_format=None, headers={}):
        url = url + "?" + query_string.to_str()
        #https://dev.twitter.com/docs/auth/application-only-auth
        headers["Authorization"] = "Bearer " + self._bearer_access_token
        response = requests.request(method="GET", url=url, headers=headers)
        return json.loads(response.content)
