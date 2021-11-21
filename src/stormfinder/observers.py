'''
Created on Nov 5, 2014

@author: Latifa Al-Naimi
'''
import datacenter, settings, gmaps

class PrintView:
    def update(self, subject):
        print subject.string()
        print "Data Center %s status: %s" %(subject.location_id, subject.status)
        

class MapView:
    map_url = settings.FILE_PATH + 'dc_map_test2.html' # html file to be generated
    def __init__(self):
        self.dc_map = gmaps.maps(37.6,-95.665,5) # USA coordinates
    
    def _set_color(self, color):
        if color == "R":
            return "#FF0000"
        elif color == "Y":
            return "#FFFF00"
        elif color == "G":
            return "#00FF00"
        else:
            return "000000"
    def update(self, subject):
        
        self.dc_map.addpoint(subject.lat, subject.lon, self._set_color(subject.status), subject.location_id)
        self.dc_map.setInfoWindow(subject.location_id, subject.status)
        self.dc_map.addradpoint(subject.lat, subject.lon, settings.CRITICAL_RADIUS*1000)  
        
        # TODO: change station icons?
        stations = datacenter.stations_dict
        for key in stations:
            self.dc_map.addpoint(stations[key].lat, stations[key].lon, self._set_color(stations[key].status), key)
            self.dc_map.setInfoWindow(key, stations[key].status, stations[key].wind_speed)
        
        self.dc_map.draw(self.map_url)

def _set_view(viewType):
    if viewType == "print":
        return PrintView()
    elif viewType == "map":
        return MapView()
