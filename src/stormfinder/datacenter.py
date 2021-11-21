'''
Created on Nov 4, 2014

@author: Latifa Al-Naimi
'''

# import module that calculates distance between GPS coordinates
import string, settings
import gps

stations_dict = {}

#======================================================================
# CLASSES
#======================================================================
class Subject: # Observable

    def __init__(self):
        self._observers = []
        
    def register(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.update(self) # observers all have function update
            
    def deregister(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

# instances typically created only when METAR is available
class Location(object):
    def __init__(self, location_id = None, lat = None, lon = None):
        self.location_id = location_id
        
        if lat is not None and lon is not None:
            self.lat = float(lat)
            self.lon = float(lon)

class Station(Location):
    '''
    classdocs
    '''

    def __init__(self, station_id = None, lat = None, lon = None): 
        '''
        Constructor
        '''
        Location.__init__(self, station_id, lat, lon)
        self.metar = None
        self.wind_speed = None
        self.gust_speed = None
        self.status = None

        
    def set_metar(self, metar_data):
        self.metar = metar_data
        self.wind_speed = self.metar.wind_speed.value() if self.metar.wind_speed else 0.0
        self.gust_speed = self.metar.wind_gust.value() if self.metar.wind_gust else 0.0
        self.status = self._label()
        
    def _label(self):
        if self.metar is None:
            return "N/A"
        else:
            if self.wind_speed > settings.HIGH_WIND:
                return "R"
            elif self.wind_speed > settings.NORMAL_WIND and self.wind_speed <= settings.HIGH_WIND:
                return "Y"
            elif self.wind_speed < settings.NORMAL_WIND:
                return "G"
            

    def string(self):
        lines = []
        lines.append("Station Code: %s" % self.location_id)
        if self.wind_speed is not None:
            lines.append("Wind Speed: %s" % self.wind_speed)
        if self.gust_speed is not None:
            lines.append("Gust Speed: %s" % self.gust_speed)
        if self.lat is not None:
            lines.append("Latitude: %s" % self.lat)
        if self.lon is not None:
            lines.append("Longitude: %s" % self.lon)
        if self.status is not None:
            lines.append("Storm Indicator: %s" % self.status)    
            
        return string.join(lines, "\n") + "\n"


class DataCenter(Location, Subject):
    '''
    classdocs
    '''

    def __init__(self, center_id, lat, lon):
        '''
        Constructor
        '''
        Subject.__init__(self)
        Location.__init__(self, center_id, lat, lon)
        self.nearby_stations = []
        if stations_dict != {}:
            self.nearby_stations = self._get_nearby_stations() 
        self.status = None
    
    # finds stations near data center instance
    def _get_nearby_stations(self):  
        nearby_stations = []
        for key in stations_dict:
            distance = gps.get_distance([stations_dict[key].lat, stations_dict[key].lon], [self.lat, self.lon])
            # compare distance of current data center with all stations in dictionary 
            # this is independent to whether or not METAR is provided
            if distance < settings.CRITICAL_RADIUS:
                nearby_stations.append(stations_dict[key])
        return nearby_stations
    
    
    def update_status(self):
        (y_count, r_count) = (0, 0)
        status = None
        if self.nearby_stations is not None:
            for station in self.nearby_stations:
                if station.status == "Y":
                    y_count += 1
                if station.status == "R":
                    r_count += 1
        if r_count >= settings.MAX_R_COUNT:
            status = "R"          
        elif y_count >= settings.MIN_Y_COUNT or (r_count > settings.MIN_R_COUNT and r_count < settings.MAX_R_COUNT):
            status = "Y"
        else:
            status = "G"
#         print "Data center status: %s" % self.status
        
        if self.status != status:
            self.status = status
            self.notify()
        
    
    def string(self):
        lines = []
        lines.append("Data Center Code: %s" % self.location_id)
        if self.lat is not None:
            lines.append("Latitude: %f" % self.lat)
        if self.lon is not None:
            lines.append("Longitude: %f" % self.lon)
        if self.status is not None:
            lines.append("Status: %s" % self.status)    
#         print self.status
        return string.join(lines, "\n") + "\n"



