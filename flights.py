import project_properties
import operator_helper
import requests
import geographic_helper
import airport_helper

dnp_equipment_codes = ['C68A','EC45','GLF4','FA20','E55P']
call_list = []

def get_from_flightaware():
    headers= {'x-apikey':project_properties.FA_API_KEY}
    query_string = "\" " + str(project_properties.SEARCH_AREA_MIN_LAT) + " " +  str(project_properties.SEARCH_AREA_MIN_LON) + " " + str(project_properties.SEARCH_AREA_MAX_LAT) + " " + str(project_properties.SEARCH_AREA_MAX_LON) + "\""
    payload = {'query':'-latlong ' + query_string + ' -filter airline','max_pages':1}
    response = requests.get("https://aeroapi.flightaware.com/aeroapi/flights/search",params=payload,headers=headers)
    if response.status_code == 200:
        flights = response.json()['flights']
        print(response.json()['links'])
        #print(len(flights))

        filtered_flights = []
        skipped_flights = []
        for flight in flights:
            if flight['ident'] == '':
                skipped_flights.append(flight['ident'])
                continue
            if flight['ident'][0] == '0':
                skipped_flights.append(flight['ident'])
                continue
            if flight['aircraft_type'] is None or flight['aircraft_type'] in dnp_equipment_codes:
                skipped_flights.append(flight['ident'])
                continue
            if flight['ident'][0] == 'N' and (flight['ident'][1]).isdigit():
                skipped_flights.append(flight['ident'])
                continue
            filtered_flights.append(flight)
        #print(len(filtered_flights))
        print(skipped_flights)

        for flight in filtered_flights:
            dist = geographic_helper.get_distance_to_my_address(flight['last_position']['latitude'],flight['last_position']['longitude'])
            flight['distance'] = dist
        sortedFlights = sorted(filtered_flights, key =lambda x:x['distance'])
        
        number_to_display = 5
        counter=0
        for flight in sortedFlights:
            #print(flight)
            operator_name= operator_helper.get_operator(flight['ident'],call_list)
            bearing = geographic_helper.get_bearing(flight['last_position']['latitude'],flight['last_position']['longitude'])
            origin = flight['origin']['code'] if flight['origin'] else 'NA'
            destination = flight['destination']['code'] if flight['destination'] else 'NA'
            origin_airport_name = airport_helper.get_airport_name(origin, call_list)
            destination_airport_name = airport_helper.get_airport_name(destination, call_list)
            origin_airport_text = origin + " (" + origin_airport_name + ")"
            destination_airport_text = destination + " (" + destination_airport_name + ")"
            print("{:<8}".format(flight['ident']),"{:<15}".format(operator_name),"{:<40}".format(origin_airport_text),"{:<40}".format(destination_airport_text),"{:<5}".format(flight['aircraft_type']),
                "{:<8}".format((flight['last_position']['altitude'])*100),"{:<4}".format(flight['last_position']['altitude_change']),"{:.2f}".format(flight['distance']),bearing)
            counter +=1
            if counter >= number_to_display:
               break
        for call in call_list:
            print(call)

def get_from_opensky():
    response = requests.get(project_properties.OPENSKY_API_CALL)
    flights = response.json()["states"]
    print(len(flights))
    flag = False
    for flight in flights:
        if flag is False:
            dist = geographic_helper.get_distance_to_my_address(flight[6],flight[5])
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


