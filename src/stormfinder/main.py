'''
Created on 25 Nov 2014

@author: Latifa Al-Naimi
'''

import xml.etree.ElementTree as ET
import observers, settings, datacenter
from metar import Metar

# take xml file of station data & optional dictionary to fill with Station objects
def _get_stations(st_src, st_dict = None):
    stations_list = []
    sysc = ET.ElementTree(file=settings.FILE_PATH+st_src)
    root = sysc.getroot()
    
    for c in root.findall('Station'):
        station_id = c.find('StationName').text
        loc = c.find('Location')
        (lat, lon) = [loc[0].text, loc[1].text]
        stations_list.append(datacenter.Station(station_id,lat,lon))
        if st_dict is not None:
            st_dict[station_id] = datacenter.Station(station_id,lat,lon) # populates dictionary        

    return stations_list 

# take data center data in xml, return list of newly created DataCenter objects
def _get_datacenters(dc_src):
    dc_list = []
    sysc = ET.ElementTree(file=settings.FILE_PATH+dc_src)
    root = sysc.getroot()
    
    for c in root.findall('Center'):
        center_id = c.find('CenterName').text
        loc = c.find('Location')
        (lat, lon) = [loc[0].text, loc[1].text]
        dc_list.append(datacenter.DataCenter(center_id,lat,lon))

    return dc_list

def run(stop_datetime, metar_src, datacenter_loc_src, station_loc_src):
    dc_created = False
    dc = [] 

    viewType = observers._set_view(settings.VIEW_TYPE)
    
    # create stations
    _get_stations(station_loc_src, datacenter.stations_dict)
        
    with open(settings.FILE_PATH + metar_src) as metar_file:
        while True:
            for line in metar_file:
                metar_obs = Metar.Metar(line)
                
                if int(line[5:11]) <= stop_datetime: # check time stamp 
                # updates given station with latest METAR reading
                    datacenter.stations_dict[metar_obs.station_id].set_metar(metar_obs)
            
            # create Data Centers once
            if not dc_created:
                dc = _get_datacenters(datacenter_loc_src)

                for center in dc:
                    center.register(viewType)
                    
                dc_created = True
            
            # always update status of data center
            for center in dc:
                center.update_status()

run(301100,"sandy_metar.txt", "datacenters.xml", "stations.xml")