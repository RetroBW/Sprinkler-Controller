# Sprinkler-Controller
Sprinkler Controller - Raspberry Pi Pico 2W programmed in Micro Python
## Overview
This raspberry Pi Pico 2W based sprnkler controller uses a web based interface, which may be connected to from any browser on your local network. The raspberry pi runs a second background task that will monitor time, and turn sprinkler system valves on or off as required. There is a manual mode where valves may be run for a predefined duration, or be toggled on or off. Auto - Program mode provides an interface for sprnkler system programming. Auto - Run mode will monitor the time and automatically control sprinkler valves.
## Initial Configuration
Raspberry Pi and sprinkler system control can be configured initially using the sprinkler_json_write.py program. You can define network credentials, the number of valves (sv's), valve names, valve groups (ie. lawn), gpio assigned and more. You'll find a commmented JSON format variable that can be modified as necessary. The raspberry pi will save any modifications to the sprinkler controller programming to sprinkler_config.json on the devices storage for persistence. 
## Operation
![Alt text](main/assets/images/mode control page.png?raw=true "Mode Control")
![Alt text](https://github.com/RetroBW/Sprinkler-Controller/tree/main/assets/images)
The mode control page is used to select from Off, Manual, and Auto modes.
