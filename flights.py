import json
import requests
import haversine as hs
from haversine import Unit
from geographiclib.geodesic import Geodesic
import properties

dnp_equipment_codes = ['C68A','EC45','GLF4']

def get_distance_to_my_address(lat,lon):
    loc1 = (properties.HOME_LAT,properties.HOME_LONG)
    loc2= (lat,lon)
    dist = hs.haversine(loc1,loc2,unit=Unit.MILES)
    return dist

def get_bearing(lat2, long2):
    bearing = Geodesic.WGS84.Inverse(properties.HOME_LAT,properties.HOME_LONG, lat2, long2)['azi1']
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

def write_to_operators_json(operators_list):
        operators_file = open("operators.json","+w")
        operators_file.write(json.dumps(operators_list))
        operators_file.close()

def get_operator_name_from_api(code,operators_list):
    headers= {'x-apikey':properties.FA_API_KEY}
    print('Fetching operator code for ' + code)
    response = requests.get("https://aeroapi.flightaware.com/aeroapi/operators/" + code,headers=headers)
    if response.status_code == 200:
        operator_short_name = response.json()['shortname']
        operators_list[code] = operator_short_name
        write_to_operators_json(operators_list)
        return operator_short_name
    else:
        print('No operator code found for operator ' + code)
        operators_list[code] = 'NA'
        write_to_operators_json(operators_list)
        return 'NA'

def get_operator(aircraft_ident):
    code = aircraft_ident[:3]
    operators_file = open("operators.json")
    operators_list = json.load(operators_file)
    operators_file.close()
    if code in operators_list:
        return operators_list[code]
    else:
        return get_operator_name_from_api(code, operators_list)

def get_from_flightaware():
    headers= {'x-apikey':properties.FA_API_KEY}
    query_string = "\" " + str(properties.SEARCH_AREA_MIN_LAT) + " " +  str(properties.SEARCH_AREA_MIN_LON) + " " + str(properties.SEARCH_AREA_MAX_LAT) + " " + str(properties.SEARCH_AREA_MAX_LON) + "\""
    payload = {'query':'-latlong ' + query_string}
    response = requests.get("https://aeroapi.flightaware.com/aeroapi/flights/search",params=payload,headers=headers)
    if response.status_code == 200:
        flights = response.json()['flights']
        print(len(flights))

        filtered_flights = []
        for flight in flights:
            if flight['ident'] == '':
                continue
            if flight['ident'][0] == '0':
                continue
            if flight['aircraft_type'] in dnp_equipment_codes:
                continue
            if flight['ident'][0] == 'N' and (flight['ident'][1]).isdigit():
                continue
            filtered_flights.append(flight)
        print(len(filtered_flights))

        for flight in filtered_flights:
            dist = get_distance_to_my_address(flight['last_position']['latitude'],flight['last_position']['longitude'])
            flight['distance'] = dist
        sortedFlights = sorted(filtered_flights, key =lambda x:x['distance'])
        
        number_to_display = 5
        counter=0
        for flight in sortedFlights:
            operator_name=get_operator(flight['ident'])
            bearing = get_bearing(flight['last_position']['latitude'],flight['last_position']['longitude'])
            origin = flight['origin']['code'] if flight['origin'] else 'NA'
            destination = flight['destination']['code'] if flight['destination'] else 'NA'
            print("{:<8}".format(flight['ident']),"{:<25}".format(operator_name),origin,destination,"{:<5}".format(flight['aircraft_type']),"{:<6}".format((flight['last_position']['altitude'])*100),"{:.2f}".format(flight['distance']),bearing)
            counter +=1
            if counter >= number_to_display:
               break

def get_from_opensky():
    response = requests.get(properties.OPENSKY_API_CALL)
    flights = response.json()["states"]
    print(len(flights))
    flag = False
    for flight in flights:
        if flag is False:
            dist = get_distance_to_my_address(flight[6],flight[5])
            flight.append(dist)
    filtered_flights =[]
    for flight in flights:
        if flight[1] == '':
            continue
        if flight[1][0] == '0':
            continue
        if flight[1][0] == 'N' and (flight[1][1]).isdigit():
            continue
        filtered_flights.append(flight)
    print(len(filtered_flights))
    flights = filtered_flights
    sortedFlights = sorted(flights, key =lambda x:x[18])
    for flight in sortedFlights:
        print(flight)

get_from_flightaware()


