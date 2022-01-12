import project_properties
import json_helper
import json
import requests

def get_airport_name_from_api(code,airports_list,call_list):
    headers= {'x-apikey':project_properties.FA_API_KEY}
    #print('Fetching city info for ' + code)
    call_list.append('Fetching airport code for ' + code)
    response = requests.get("https://aeroapi.flightaware.com/aeroapi/airports/" + code,headers=headers)
    if response.status_code == 200:
        airport_name = response.json()['city']
        airports_list[code] = airport_name
        json_helper.write_to_json(airports_list,"airports.json")
        return airport_name
    else:
        print('No airport city found for airport ' + code)
        airports_list[code] = 'NA'
        json_helper.write_to_json(airports_list,"airports.json")
        return 'NA'

def get_airport_name(airport_code,call_list):
    airports_file = open("airports.json")
    airports_list = json.load(airports_file)
    airports_file.close()
    if airport_code in airports_list:
        return airports_list[airport_code]
    else:
        return get_airport_name_from_api(airport_code, airports_list,call_list)