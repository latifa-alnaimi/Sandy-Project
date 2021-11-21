# Calculations & mappings
'''
Created on Oct 31, 2014

@author: Latifa Al-Naimi
'''
import geo      

def get_distance(coord1, coord2):
    loc1 = geo.xyz(coord1[0], coord1[1])
    loc2 = geo.xyz(coord2[0], coord2[1])
 
    return geo.distance(loc1, loc2)/1000 # return in km



# haversine function for distance
# def get_distance(coord1, coord2):
#     """
#     Calculate the great circle distance between two points 
#     on the earth (specified in decimal degrees)
#     """
#   
#     # convert decimal degrees to radians 
#     lon1, lat1, lon2, lat2 = map(radians, [coord1[1], coord1[0], coord2[1], coord2[0]])
#       
#     # haversine formula 
#     dlon = lon2 - lon1 
#     dlat = lat2 - lat1 
#     a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#     c = 2 * asin(sqrt(a)) 
#   
#     # 6367 km = radius of Earth
#     km = 6367 * c
#     return km 
