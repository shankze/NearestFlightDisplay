import project_properties
import json_helper
import json
import requests

def get_operator_name_from_api(code, operators_list, call_list):
    headers= {'x-apikey':project_properties.FA_API_KEY}
    #print('Fetching operator code for ' + code)
    call_list.append('Fetching operator code for ' + code)
    response = requests.get("https://aeroapi.flightaware.com/aeroapi/operators/" + code,headers=headers)
    if response.status_code == 200:
        if response.json()['shortname'] is None:
            operator_short_name = 'NA'
        else:    
            operator_short_name = response.json()['shortname']
        operators_list[code] = operator_short_name
        json_helper.write_to_json(operators_list,"operators.json")
        return operator_short_name
    else:
        print('No operator code found for operator ' + code)
        operators_list[code] = 'NA'
        json_helper.write_to_json(operators_list,"operators.json")
        return 'NA'

def get_operator(aircraft_ident, call_list):
    code = aircraft_ident[:3]
    operators_file = open("operators.json")
    operators_list = json.load(operators_file)
    operators_file.close()
    if code in operators_list:
        return operators_list[code]
    else:
        return get_operator_name_from_api(code, operators_list, call_list)