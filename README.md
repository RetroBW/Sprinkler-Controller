# Sprinkler-Controller
Sprinkler Controller - Raspberry Pi Pico 2W programmed in Micro Python
## Overview
This raspberry Pi Pico 2W based sprnkler controller application uses a web based interface, which may be connected to from any browser on your local network. The raspberry pi runs a second background task that will monitor time, and turn sprinkler system valves on or off as required. There is a manual mode where valves may be run for a predefined duration, or be toggled on or off. Auto - Program mode provides an interface for sprnkler system programming. Auto - Run mode will monitor the time and automatically control sprinkler valves.
## Initial Configuration
Raspberry Pi and sprinkler system control can be configured initially using the sprinkler_json_write.py program. You can define network credentials, the number of valves (sv's), valve names, valve groups (ie. lawn), gpio assigned and more. You'll find a commmented JSON format variable that can be modified as necessary. The raspberry pi will save any modifications to the sprinkler controller programming to sprinkler_config.json on the devices storage for persistence. 
## Operation
### Mode Control Webpage
![Alt text](assets/images/mode_control_page.png?raw=true "Mode Control")<br>
The mode control page is used to select from Off, Manual, and Auto modes.
### Manual Mode Webpage
![Alt text](assets/images/manual_control_page.png?raw=true "Manual Control")<br>
The manual mode page allows a single valve to manually be turned on or off. The duration field allows the runtime of the valve to be defined. Clicking on the valve again while it is running will turn the valve off. Clicking on another valve while a valve is running will turn the previous valve off and the new valve on.
### Auto Program Mode
![Alt text](assets/images/auto_program_page_1_of_2.png?raw=true "Auto Program 1 of 2")<br>
![Alt text](assets/images/auto_program_page_2_of_2.png?raw=true "Auto Program 2 of 2")<br>
The auto program page allows automatic valve durations to be defined, valve group start times for each day to be defined, and days to be enabled or disabled. After editing a valve duration or valve group start time the save button must be pressed to save changes.
### Auto Run Mode
![Alt text](assets/images/auto_run_page.png?raw=true "Auto Run")<br>
Auto run mode will execute the defined automatic operation. The auto run page shows if a valve is currently being run, and if any valves are queued to be run. There is also an event log at the bottom of the page to allow previous actions to be viewed.
