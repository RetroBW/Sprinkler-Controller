import json

try:
    with open('sprinkler_config.json', 'r') as f:
        config = json.load(f)
    print("Data read from JSON file:")
    #print(config)
    print('data: ' + config['auto']['start_time'][0]['mon_start'])
except:
    print("Error")
