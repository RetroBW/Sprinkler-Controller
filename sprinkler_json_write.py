import json

# sprinkler control app configuration
# -----------------------------------
# This application can be executed once after modifying the structure to match your sprinkler system. This will create a
# JSON based list variable that will be referenced, modifed and saved for persistence by the sprinkler control preogram. 

# NOTE: List lengths must match for: ['sv names'], ['sv pins'], ['manual']['duration'], ['manual']['class']
#       and ['auto']['duration']. The list lengths should match the number of sprinkler valves.
config = {
    "wifi": {
        "ssid": "west",
        "pwd": "21571BalermaMV@CA"
    },
    #offset hours from UTC
    "time_zone_offset": -6,
    "days": [
        {'title': 'Monday', 'name': 'mon'},
        {'title': 'Tuesday', 'name': 'tue'},
        {'title': 'Wednesday', 'name': 'wed'},
        {'title': 'Thursday', 'name': 'thu'},
        {'title': 'Friday', 'name': 'fri'},
        {'title': 'Saturday', 'name': 'sat'},
        {'title': 'Sunday', 'name': 'sun'}
    ],
    #raspberry-pi output gpio number. The list length may be changed as necessary. See note above for other affected lists.
    "sv pins": [0, 1, 2, 3, 4, 5, 6, 7],
    "sv names": [
        "Front Strip (1)", 
        "Front (2)", 
        "Side (3)", 
        "Back Fence (4)", 
        "Back Mid (5)", 
        "Back Patio (6)", 
        "Drip (7)", 
        "Garden (8)"
    ],
    #modes = off, man, auto
    "mode": "off",
    "manual": {
        #sv pin index
        "duration": ['10', '10', '10', '10', '10', '10', '10', '10'],
        "class": ['btn_off', 'btn_off', 'btn_off', 'btn_off', 'btn_off', 'btn_off', 'btn_off', 'btn_off']
    },
    "auto": {
        #mode = run, prog
        "mode": "prog",
        #sv (valve) pin index
        "duration": ['1', '1', '1', '1', '1', '1', '1', '1'],
        #Each group contains a list of sv pin indexes. The number of group lists can be changed as necessary.
        "group": {
            "Lawn": [0, 1, 2, 3, 4, 5],
            "Drip": [6],
            "Garden": [7]
        },
        #Each start_time list controls a group (of valves). The number of start_time lists can be changed as necessary.
        "start_time": [
            {	"name": 'lawn1',
                "title": 'Lawn 1st',
                "group": 'Lawn',
                "mon_start": "07:00",
                "tue_start": "06:00",
                "wed_start": "06:00",
                "thu_start": "06:00",
                "fri_start": "06:00",
                "sat_start": "06:00",
                "sun_start": "06:00",
                "mon_class": 'btn_off_small',
                "tue_class": 'btn_off_small',
                "wed_class": 'btn_off_small',
                "thu_class": 'btn_off_small',
                "fri_class": 'btn_off_small',
                "sat_class": 'btn_off_small',
                "sun_class": 'btn_off_small'
            },
            {	"name": 'lawn2',
                "title": 'Lawn 2nd',
                "group": 'Lawn',
                "mon_start": "06:00",
                "tue_start": "06:00",
                "wed_start": "06:00",
                "thu_start": "06:00",
                "fri_start": "06:00",
                "sat_start": "06:00",
                "sun_start": "06:00",
                "mon_class": 'btn_off_small',
                "tue_class": 'btn_off_small',
                "wed_class": 'btn_off_small',
                "thu_class": 'btn_off_small',
                "fri_class": 'btn_off_small',
                "sat_class": 'btn_off_small',
                "sun_class": 'btn_off_small'
            },
            {	"name": 'lawn3',
                "title": 'Lawn 3rd',
                "group": 'Lawn',
                "mon_start": "06:00",
                "tue_start": "06:00",
                "wed_start": "06:00",
                "thu_start": "06:00",
                "fri_start": "06:00",
                "sat_start": "06:00",
                "sun_start": "06:00",
                "mon_class": 'btn_off_small',
                "tue_class": 'btn_off_small',
                "wed_class": 'btn_off_small',
                "thu_class": 'btn_off_small',
                "fri_class": 'btn_off_small',
                "sat_class": 'btn_off_small',
                "sun_class": 'btn_off_small'
            },
            {	"name": 'drip',
                "title": 'Drip',
                "group": 'Drip',
                "mon_start": "06:00",
                "tue_start": "06:00",
                "wed_start": "06:00",
                "thu_start": "06:00",
                "fri_start": "06:00",
                "sat_start": "06:00",
                "sun_start": "06:00",
                "mon_class": 'btn_off_small',
                "tue_class": 'btn_off_small',
                "wed_class": 'btn_off_small',
                "thu_class": 'btn_off_small',
                "fri_class": 'btn_off_small',
                "sat_class": 'btn_off_small',
                "sun_class": 'btn_off_small'
            },
            {	"name": 'garden',
                "title": 'Garden',
                "group": 'Garden',
                "mon_start": "06:00",
                "tue_start": "06:00",
                "wed_start": "06:00",
                "thu_start": "06:00",
                "fri_start": "06:00",
                "sat_start": "06:00",
                "sun_start": "06:00",
                "mon_class": 'btn_off_small',
                "tue_class": 'btn_off_small',
                "wed_class": 'btn_off_small',
                "thu_class": 'btn_off_small',
                "fri_class": 'btn_off_small',
                "sat_class": 'btn_off_small',
                "sun_class": 'btn_off_small'
            },
        ],
    }
}

# Write the data to a JSON file
# for i in config['sv pins']:
#     print(str(i))
#print('data: ' + str(config['sv pins'][0]))
try:
    with open('sprinkler_config.json', 'w') as f:
        json.dump(config, f) # indent for pretty-printing
    print("Sprinkler configuration JSON data successfully written")
except IOError as e:
    print(f"Error writing to file: {e}")
