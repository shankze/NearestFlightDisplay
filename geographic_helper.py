import project_properties
import haversine as hs
from haversine import Unit
from geographiclib.geodesic import Geodesic

def get_distance_to_my_address(lat,lon):
    loc1 = (project_properties.HOME_LAT,project_properties.HOME_LONG)
    loc2= (lat,lon)
    dist = hs.haversine(loc1,loc2,unit=Unit.MILES)
    return dist
    #return 10

def get_bearing(lat2, long2):
    bearing = Geodesic.WGS84.Inverse(project_properties.HOME_LAT,project_properties.HOME_LONG, lat2, long2)['azi1']
    return get_direction_from_bering(bearing)

def get_direction_from_bering(bearing):
    if bearing < -157.5:
        return 'S'
    if bearing < -112.5:
        return 'SW'
    if bearing < -67.5:
        return 'W'
    if bearing < -22.5:
        return 'NW'
    if bearing < 22.5:
        return 'N'
    if bearing < 67.5:
        return 'NE'
    if bearing < 112.5:
        return 'E'
    if bearing < 157.5:
        return 'SE'
    else:
        return 'S'