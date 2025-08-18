# Sprinkler-Controller
Sprinkler Controller - Raspberry Pi Pico 2W programmed in Micro Python

Raspberry Pi and sprinkler system control can be configured initially using the sprinkler_json_write.py program. You can define network credentials, the number of valves (sv's), valve names, valve groups (ie. lawn), gpio assigned and more. You'll find a commmented JSON format variable that can be modified as necessary. The raspberry pi will save any modifications to the sprinkler controller programming to sprinkler_config.json on the devices storage for persistence. 

The raspberry pi will host a web server which may be connected to from any browser on your local network. The raspberry pi runs a second background task that will monitor time, and turn sprinkler system valves on or off as required. There is a manual mode where valves may be run for a predefined duration, or be toggled on or off. Auto - Program mode provides an interface for sprnkler system programming. Auto - Run mode will monitor the time and automatically control sprinkler valves.
