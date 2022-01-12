import json

def write_to_json(data,file_name):
        file = open(file_name,"+w")
        file.write(json.dumps(data, indent=4, sort_keys=True))
        file.close()
