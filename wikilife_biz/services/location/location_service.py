# coding=utf-8


class LocationServiceException(Exception):
    pass


class LocationService(object):

    _location_dao = None
    
    def __init__(self, logger, location_dao):
        self._logger = logger
        self._location_dao = location_dao

    def search_location(self, name, country_code=None):
        if len(name) < 3:
            raise LocationServiceException("name to short")
        
        return self._location_dao.search_location(name=name, country=country_code)

    def validate_location(self, location):
        #return self._location_dao.search_political(location["political"]) != None
        return True

    def _validate_geo(self, geo):
        pass

    def _validate_political(self, political):
        pass
    
    def _validate_at(self, at):
        pass


    """    

    _logger = None
    _countries_mgr = None
    _regions_mgr = None
    _cities_mgr = None

    def __init__(self, logger, countries_manager, regions_manager, cities_manager):
        self._logger = logger
        self._countries_mgr = countries_manager
        self._regions_mgr = regions_manager
        self._cities_mgr = cities_manager

    def get_country_by_name(self, country_name):
        return self._countries_mgr.get_country_by_name(country_name)

    def get_regions(self, country_name, region_name=None):
        regions = None
        if region_name != None:
            regions = [self._regions_mgr.get_region(country_name, region_name)]
        else:
            regions = list(self._regions_mgr.get_regions(country_name))

        return regions

    def get_cities(self, country_name, region_name, city_name=None):
        cities = None
        if city_name != None:
            cities = [self._cities_mgr.get_city(country_name, region_name, city_name)]
        else:
            cities = list(self._cities_mgr.get_cities(country_name, region_name))

        return cities
    """    
