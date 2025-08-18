# Based On Example Provide By: Rui Santos & Sara Santos - Random Nerd Tutorials
# Example Project: https://RandomNerdTutorials.com/raspberry-pi-pico-w-asynchronous-web-server-micropython/

# Import necessary modules
import network
import asyncio
import socket
import time
import random
from machine import Pin
import utime
import json

outSVs = []

#solenoid on/off control
SV_off_time = utime.mktime(utime.localtime()) #seconds since the epoch + duration in seconds
SV_on_list = []
SV_last_on_time = ''

#user defined configuration
config = []

last_mode = ''

#auto run log
auto_run_log = []

def read_config():
    global config
    try:
        with open('sprinkler_config.json', 'r') as f:
            config = json.load(f)
    except:
        print("Configuration Read Error")

def write_config():
    try:
        with open('sprinkler_config.json', 'w') as f:
            json.dump(config, f) # indent for pretty-printing
        print("Sprinkler configuration JSON data successfully written")
    except:
        print("Configuration Write Error")

def init_io():
    #init sv pin assignments
    for i in config['sv pins']:
        outSVs.append(Pin(i, Pin.OUT))
    
def write_auto_run_log(s):
    #get current day of week and time
    tm_now = time.localtime()
    tm_now_weekday = config['days'][tm_now[6]]['name']
    tm_now_hh_mm = "{:02d}:{:02d}".format(tm_now[3], tm_now[4])
    auto_run_log.append(tm_now_weekday + ' ' + tm_now_hh_mm + ': ' + s)
    while len(auto_run_log) > 100:
        del auto_run_log[0]
        
def get_sv_on():
    global config
    str_sv_on = 'None'
    for i in range(len(outSVs)):
        if outSVs[i].value() == 1:
            str_sv_on = config['sv names'][i]
    return str_sv_on
    
# HTML template for the webpage
def webpage_off():
    global config
    html = """
    <!DOCTYPE html>
    <html lang='en-US'>
    <head>
        <title>Sprinkler Controller</title>
        <style>
            body {
                background-color: lightgrey;
            }
            h2 {
                padding-left: 25px;
            }
            h3 {
                padding-left: 50px;
            }
            h4 {
                padding-left: 75px;
            }
            table, th, td {
                border: 1px solid;
            }
            .btn_off {
                    width: 150px;
                    background-color: red;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    margin: 10px;
            }
            .btn_on {
                width: 150px;
                background-color: green;
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 10px;
            }
            .btn_off_small {
                    width: 50px;
                    background-color: red;
                    color: white;
                    border: none;
                    padding: 5px 5px;
                    margin: 5px;
            }
            .btn_on_small {
                width: 50px;
                background-color: green;
                color: white;
                border: none;
                padding: 5px 5px;
                margin: 5px;
            }
            .manual_control {
                display: none;
            }
            .auto_control {
                display: none;
            }
            .auto_duration {
                position: absolute;
                left: 200px;
            }
        </style>
    </head>
    <body>
        <h1>Sprinkler Control</h1>
        <div id='div_time'>
        <h2>Time: <span id='time'></span></h2>
        </div>
        <form id='frmMode'>
            <h2>Mode</h2>
            <input type='hidden' id='inMode' name='inMode' value='off'>
            <button id='btnManualMode' class='btn_off' onclick='submit_form("man")'>Manual</button>
            <button id='btnOffMode' class='btn_on' onclick='submit_form("off")'>Off</button>
            <button id='btnAutoMode' class='btn_off' onclick='submit_form("auto")'> Auto </button><br><br>
        </form>
        <script>
            function updateTime() {
                const weekday = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
                const now = new Date();
                document.getElementById('time').textContent = weekday[now.getDay()] + ', ' + now.toLocaleTimeString();
            }
            setInterval(updateTime, 1000);
            updateTime();
            function submit_form(strMode) {
                document.getElementById('inMode').value = strMode;
                document.getElementById('frmMode').submit();
            }
        </script>
    </body>
    </html
    """
    return str(html)

# HTML template for the webpage
def webpage_man():
    global config
    
    strManControl = ""
    
    for i in range(len(config['sv pins'])):
        strManControl = strManControl + "<button id='btn_" + str(i) + "' class=" + config['manual']['class'][i] + " onclick='ManualZoneSelect(\"btn_" + str(i) + "\")'>" + config['sv names'][i] + "</button>"
        strManControl = strManControl + "<input type='number' id='dur_" + str(i) + "' name='Duration_" + str(i) + "' min='1' max='90' step='1' value=" + config['manual']['duration'][i] + "><br>"

    html = """
    <!DOCTYPE html>
    <html lang='en-US'>
    <head>
        <title>Sprinkler Controller</title>
        <style>
            body {
                background-color: lightgrey;
            }
            h2 {
                padding-left: 25px;
            }
            h3 {
                padding-left: 50px;
            }
            h4 {
                padding-left: 75px;
            }
            table, th, td {
                border: 1px solid;
            }
            .btn_off {
                    width: 150px;
                    background-color: red;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    margin: 10px;
            }
            .btn_on {
                width: 150px;
                background-color: green;
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 10px;
            }
            .btn_off_small {
                    width: 50px;
                    background-color: red;
                    color: white;
                    border: none;
                    padding: 5px 5px;
                    margin: 5px;
            }
            .btn_on_small {
                width: 50px;
                background-color: green;
                color: white;
                border: none;
                padding: 5px 5px;
                margin: 5px;
            }
            .manual_control {
                display: none;
            }
            .auto_control {
                display: none;
            }
            .auto_duration {
                position: absolute;
                left: 200px;
            }
        </style>
    </head>
    <body>
        <h1>Sprinkler Control</h1>
        <div id='div_time'>
        <h2>Time: <span id='time'></span></h2>
        </div>
        <form id='frmMode'>
            <h2>Mode</h2>
            <input type='hidden' id='inMode' name='inMode' value='off'>
            <button id='btnManualMode' class='btn_on' onclick='submit_form("man")'>Manual</button>
            <button id='btnOffMode' class='btn_off' onclick='submit_form("off")'>Off</button>
            <button id='btnAutoMode' class='btn_off' onclick='submit_form("auto")'> Auto </button><br><br>
        </form>
        <form id='frmManualControl'>
            <h2>Manual Run Zone</h2>
            <input type='hidden' id='inZone' name='inZone' value=''>
        """ + strManControl + """
        </form>
        <script>
            function updateTime() {
                const weekday = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
                const now = new Date();
                document.getElementById('time').textContent = weekday[now.getDay()] + ', ' + now.toLocaleTimeString();
            }
            setInterval(updateTime, 1000);
            updateTime();
            function submit_form(strMode) {
                document.getElementById('inMode').value = strMode;
                document.getElementById('frmMode').submit();
            }
            function ManualZoneSelect(strZone) {
                document.getElementById('inZone').value = strZone;
                document.getElementById('frmManualControl').submit();
            }
            function ReloadPage() {
                window.location.replace(location.protocol + '//' + location.host + location.pathname);
            }
            setInterval(ReloadPage, 15000);
        </script>
    </body>
    </html
    """
    return str(html)

# HTML template for the webpage
def webpage_auto_prog():
    global config
    html = """
    <!DOCTYPE html>
    <html lang='en-US'>
    <head>
        <title>Sprinkler Controller</title>
        <style>
            body {
                background-color: lightgrey;
            }
            h2 {
                padding-left: 25px;
            }
            h3 {
                padding-left: 50px;
            }
            h4 {
                padding-left: 75px;
            }
            table, th, td {
                border: 1px solid;
            }
            .btn_off {
                    width: 150px;
                    background-color: red;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    margin: 10px;
            }
            .btn_on {
                width: 150px;
                background-color: green;
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 10px;
            }
            .btn_off_small {
                    width: 50px;
                    background-color: red;
                    color: white;
                    border: none;
                    padding: 5px 5px;
                    margin: 5px;
            }
            .btn_on_small {
                width: 50px;
                background-color: green;
                color: white;
                border: none;
                padding: 5px 5px;
                margin: 5px;
            }
            .manual_control {
                display: none;
            }
            .auto_control {
                display: none;
            }
            .auto_duration {
                position: absolute;
                left: 200px;
            }
        </style>
    </head>
        <body>
        <h1>Sprinkler Control</h1>
        <div id='div_time'>
        <h2>Time: <span id='time'></span></h2>
        </div>
        <form id='frmMode'>
            <h2>Mode</h2>
            <input type='hidden' id='inMode' name='inMode' value='off'>
            <button id='btnManualMode' class='btn_off' onclick='submit_form("man")'>Manual</button>
            <button id='btnOffMode' class='btn_off' onclick='submit_form("off")'>Off</button>
            <button id='btnAutoMode' class='btn_on' onclick='submit_form("auto")'> Auto </button><br><br>
        </form>
        <form id='frmAutoMode'>
            <h2>Auto Mode</h2>
            <input type='hidden' id='inAutoMode' name='inAutoMode' value='prog'>
            <button id='btnAutoProg' class='btn_on' onclick='submit_auto_form("prog")'>Progam</button>
            <button id='btnAutoRun' class='btn_off' onclick='submit_auto_form("run")'>Run</button>
        </form>
        <form id='frmAutoProg'>
            <input type='hidden' id='inAutoProg' name='inAutoProg' value=''><br>
            <h2>Valve On Duration</h2>
            <table>
                <tr>
                    <th></th>
                    <th>Minutes</th>
                </tr>"""

    i = 0
    for dur in config['auto']['duration']:
        html = html + """
                <tr>
                    <td>""" + config['sv names'][i] + """</td>
                    <td><input type='number' id='""" + dur + """_""" + str(i) + """' name='""" + dur + """_""" + str(i) + """' min='1' max='90' step='1' value='""" + dur + """'</td>
                </tr>"""
        i+=1
        
    html = html + """
            </table>
            <button id='btn_dur_save' class='btn_on' onclick='AutoStartTimeEna("btn_dur_save")'>Save</button>
    """        

    for tbl in config['auto']['start_time']:
        html = html + """
            <h2>""" + tbl['title'] + """</h2>
            <table>
                <tr>
                    <th></th>
                    <th>Start Time</th>
                </tr>"""
        for day in config['days']:
            if tbl[day['name'] + '_class'] == 'btn_off_small':
                btnText = 'Off'
            else:
                btnText = 'On'
            tm = tbl[day['name'] + '_start']
            html = html + """
                <tr>
                    <td>""" + day['title'] + """</td>
                    <td><button id='btn_""" + tbl['name'] + """_""" + day['name'] + """' class='""" + tbl[day['name'] + '_class'] + """' onclick='AutoStartTimeEna(&apos;btn_""" + tbl['name'] + """_""" + day['name'] + """&apos;)'>""" + btnText + """</button><input type='time' id='id_""" + tbl['name'] + """_""" + day['name'] + """' name='Time' value=""" + tm + """></td>
                </tr>"""
        html = html + """
            </table><br>"""
    
    html = html + """
        </form>
        <script>
            function updateTime() {
                const weekday = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
                const now = new Date();
                document.getElementById('time').textContent = weekday[now.getDay()] + ', ' + now.toLocaleTimeString();
            }
            setInterval(updateTime, 1000);
            updateTime();
            function submit_form(strMode) {
                document.getElementById('inMode').value = strMode;
                document.getElementById('frmMode').submit();
            }
            function submit_auto_form(strMode) {
                document.getElementById('inAutoMode').value = strMode;
                document.getElementById('frmAutoMode').submit();
            }
			function AutoStartTimeEna(strBtn) {
                document.getElementById('inAutoProg').value = strBtn;
                document.getElementById('frmAutoProg').submit();
			}
        </script>
    </body>
    </html
    """
    return str(html)

# HTML template for the webpage
def webpage_auto_run():
    global config
    html = """
    <!DOCTYPE html>
    <html lang='en-US'>
    <head>
        <title>Sprinkler Controller</title>
        <style>
            body {
                background-color: lightgrey;
            }
            h2 {
                padding-left: 25px;
            }
            h3 {
                padding-left: 50px;
            }
            h4 {
                padding-left: 75px;
            }
            table, th, td {
                border: 1px solid;
            }
            .btn_off {
                    width: 150px;
                    background-color: red;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    margin: 10px;
            }
            .btn_on {
                width: 150px;
                background-color: green;
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 10px;
            }
            .btn_off_small {
                    width: 50px;
                    background-color: red;
                    color: white;
                    border: none;
                    padding: 5px 5px;
                    margin: 5px;
            }
            .btn_on_small {
                width: 50px;
                background-color: green;
                color: white;
                border: none;
                padding: 5px 5px;
                margin: 5px;
            }
            .manual_control {
                display: none;
            }
            .auto_control {
                display: none;
            }
            .auto_duration {
                position: absolute;
                left: 200px;
            }
        </style>
    </head>
    <body>
        <h1>Sprinkler Control</h1>
        <div id='div_time'>
        <h2>Time: <span id='time'></span></h2>
        </div>
        <form id='frmMode'>
            <h2>Mode</h2>
            <input type='hidden' id='inMode' name='inMode' value='off'>
            <button id='btnManualMode' class='btn_off' onclick='submit_form("man")'>Manual</button>
            <button id='btnOffMode' class='btn_off' onclick='submit_form("off")'>Off</button>
            <button id='btnAutoMode' class='btn_on' onclick='submit_form("auto")'> Auto </button><br><br>
        </form>
        <form id='frmAutoMode'>
            <h2>Auto Mode</h2>
            <input type='hidden' id='inAutoMode' name='inAutoMode' value='prog'>
            <button id='btnAutoProg' class='btn_off' onclick='submit_auto_form("prog")'>Progam</button>
            <button id='btnAutoRun' class='btn_on' onclick='submit_auto_form("run")'>Run</button>
        </form>
        <div>
            <h2>Valve Currently On</h2>
            """ + get_sv_on() + """<br>
        </div>
        <div>
            <h2>Valves Queued To Be Turned On</h2>
            """
    
    if len(SV_on_list) > 0:
        for v in SV_on_list:
            html = html + config['sv names'][v] + "<br>"
    else:
        html = html + "None<br>"

    html = html + """
        </div>
        <div>
            <h2>Auto Run Log</h2>
            """
    
    for s in auto_run_log:
        html = html + s + "<br>"
        
    html = html + """
        </div>
        <script>
            function updateTime() {
                const weekday = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
                const now = new Date();
                document.getElementById('time').textContent = weekday[now.getDay()] + ', ' + now.toLocaleTimeString();
            }
            setInterval(updateTime, 1000);
            updateTime();
            function submit_form(strMode) {
                document.getElementById('inMode').value = strMode;
                document.getElementById('frmMode').submit();
            }
            function submit_auto_form(strMode) {
                document.getElementById('inAutoMode').value = strMode;
                document.getElementById('frmAutoMode').submit();
            }
            function ReloadPage() {
                window.location.replace(location.protocol + '//' + location.host + location.pathname);
            }
            setInterval(ReloadPage, 15000);
        </script>
    </body>
    </html
    """
    return str(html)

# Init Wi-Fi Interface
def init_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Set the hostname before connecting
    wlan.config(hostname='sprinkler')
    # Connect to your network
    wlan.connect(ssid, password)
    # Wait for Wi-Fi connection
    connection_timeout = 10
    while connection_timeout > 0:
        print(wlan.status())
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        time.sleep(1)
    # Check if connection is successful
    if wlan.status() != 3:
        print('Failed to connect to Wi-Fi')
        return False
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return True

def update_manual_duration(request):
    global config
    #split durations
    request_list = request.split('&')
    #iterate durations
    for request_item in request_list:
        for i in range(len(config['sv pins'])):
            if request_item.find('Duration_' + str(i)) == 0:
                request_item_list = request_item.split('=')
                config['manual']['duration'][i] = request_item_list[1]
    # write configuration
    write_config()

def update_auto_prog(request):
    global config
    #split durations
    request_list = request.split('&')
    #get button
    temp_list = request_list[0].split('=')
    button = temp_list[1]
    #save durations button pressed
    if button == 'btn_dur_save':
        # update durations
        for i in range(len(config['auto']['duration'])):
            temp_list = request_list[i+1].split('=')
            config['auto']['duration'][i] = temp_list[1]
        i = 0
    #start time enable button pressed
    else:
        #get table and day
        temp_list = button.split('_')
        btn_table = temp_list[1]
        btn_day = temp_list[2]
        #update button state
        for tbl in config['auto']['start_time']:
            if tbl['name'] == btn_table:
                if tbl[btn_day + '_class'] == 'btn_off_small':
                    tbl[btn_day + '_class'] = 'btn_on_small'
                else:
                    tbl[btn_day + '_class'] = 'btn_off_small'
    # update times
    i=9
    for tbl in config['auto']['start_time']:
        for day in config['days']:
            temp_list = request_list[i].split('=')
            time_string = temp_list[1][:2] + ':' + temp_list[1][-2:]
            tbl[day['name'] + '_start'] = time_string
            i+=1
            
def auto_run_handler():
    global config
    global SV_on_list
    global SV_off_time
    global SV_last_on_time
    #update SV_on_list
    #-----------------
    #get current day of week and time
    tm_now = time.localtime()
    tm_now_weekday = config['days'][tm_now[6]]['name']
    tm_now_hh_mm = "{:02d}:{:02d}".format(tm_now[3], tm_now[4])
    #iterate auto start time lists
    if SV_last_on_time != tm_now_hh_mm:
        for tbl in config['auto']['start_time']:
            #check for matching start time
            if tm_now_hh_mm == tbl[tm_now_weekday + '_start']:
                for sv in config['auto']['group'][tbl['group']]:
                    #append sv to SV_on_list
                    if not sv in SV_on_list:
                        SV_on_list.append(sv)
                        write_auto_run_log(config['sv names'][sv] + " appended to valve on list")
        SV_last_on_time = tm_now_hh_mm
    #check for solenoid off time reached
    #-----------------------------------
    if SV_off_time == utime.mktime(utime.localtime()):
        # turn off solenoids
        for outSV in outSVs:
            outSV.value(0)
        #clear off time
        SV_off_time = ''
        write_auto_run_log("all valves turned off")
    #check for next solenoid on
    #--------------------------
    sv_on = False
    for outSV in outSVs:
        sv_on = sv_on or outSV.value()
    if (sv_on == False) and (len(SV_on_list) > 0):
        #get next solennoid on index and remove ffrom list
        i = SV_on_list.pop(0)
        #turn on solenoid
        outSVs[i].value(1)
        #update stop time
        SV_off_time = utime.mktime(utime.localtime()) + (int(config['auto']['duration'][i]) * 60)
        write_auto_run_log(config['sv names'][i] + " turned on")
        write_auto_run_log("current epoch seconds = " +str(utime.mktime(utime.localtime())))
        write_auto_run_log("off time epoch seconds = " + str(SV_off_time))
                      
# Asynchronous functio to handle client's requests
async def handle_client(reader, writer):
    global config
    global SV_off_time
    
    request_line = await reader.readline()
    #print('Request:', request_line)
    
    # Skip HTTP request headers
    while await reader.readline() != b"\r\n":
        pass
    
    request = str(request_line, 'utf-8').split()[1]
    if request.find('/?') == 0:
        print('Request:', request)
    
    # Process the request and update variables
    if request.find('/?inMode=man') == 0:
        # Generate HTML response
        config['mode'] = 'man'
        # write configuration
        write_config()
    elif request.find('/?inMode=off') == 0:
        # Generate HTML response
        config['mode'] = 'off'  
        # write configuration
        write_config()
    elif request.find('/?inMode=auto') == 0:
        config['mode'] = 'auto'
        # write configuration
        write_config()
    elif request.find('/?inAutoMode=prog') == 0:
        config['auto']['mode'] = 'prog'
        # write configuration
        write_config()
    elif request.find('/?inAutoMode=run') == 0:
        config['auto']['mode'] = 'run'
        # write configuration
        write_config()
    elif request.find('/?inAutoProg') == 0:
        update_auto_prog(request)
        # write configuration
        write_config()
    elif request.find('/?inZone=btn_') == 0:
        update_manual_duration(request)
        request_list = request.split('&')
        request_list = request_list[0].split('_')
        for i in range(len(config['sv pins'])):
            if int(request_list[1]) == i:
                if config['manual']['class'][i] == 'btn_off':
                    config['manual']['class'][i] = 'btn_on'
                    SV_off_time = utime.mktime(utime.localtime()) + (int(config['manual']['duration'][i]) * 60)
                else:
                    config['manual']['class'][i] = 'btn_off'
            else:
                config['manual']['class'][i] = 'btn_off'
 
    if config['mode'] == 'off':
        # Generate HTML response
        response = webpage_off()  
    elif config['mode'] == 'man':
        # Generate HTML response
        response = webpage_man()  
    elif config['mode'] == 'auto':
        # Generate HTML response
        if config['auto']['mode'] == 'prog':
            response = webpage_auto_prog()
        else:
            response = webpage_auto_run()
        
    # Send the HTTP response and close the connection
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    #writer.write(b"Refresh: 15; URL=/\r\n") # Refresh every 15 seconds, staying on the same URL
    writer.write(response)
    await writer.drain()
    await writer.wait_closed()

async def SV_control():
    global config
    global SV_off_time
    global last_mode

    # Toggle SV state
    while True:

        # mode change
        if config['mode'] != last_mode:
            last_mode = config['mode']
            for outSV in outSVs:
                outSV.value(0)
            
        # manual mode
        if config['mode'] == 'man':
            btn_on = False
            for c in config['manual']['class']:
                btn_on = btn_on or (c == 'btn_on')
            if btn_on and (utime.mktime(utime.localtime()) > SV_off_time):
                for j in range(len(config['manual']['class'])):
                    config['manual']['class'][j] = 'btn_off'
            i=0
            for c in config['manual']['class']:
                if c == 'btn_on':
                    outSVs[i].value(1)
                else:
                    outSVs[i].value(0)
                i+=1
        else:
            for j in range(len(config['manual']['class'])):
                config['manual']['class'][j] = 'btn_off'

        # auto run mode
        if (config['mode'] == 'auto'):
            if (config['auto']['mode'] == 'run'):
                auto_run_handler()
            else:
                SV_on_list.clear()
                for outSV in outSVs:
                    outSV.value(0)
        else:
            SV_on_list.clear()

        # off mode
        if (config['mode'] == 'off'):
            for outSV in outSVs:
                outSV.value(0)

        await asyncio.sleep(1)

async def main():    
    #init wifi
    if not init_wifi(config['wifi']['ssid'], config['wifi']['pwd']):
        print('Exiting program.')
        return
    
    # Start the server and run the event loop
    print('Setting up server')
    server = asyncio.start_server(handle_client, "0.0.0.0", 80)
    asyncio.create_task(server)
    asyncio.create_task(SV_control())
    
    while True:
        # Add other tasks that you might need to do in the loop
        await asyncio.sleep(5)
        #print('This message will be printed every 5 seconds')
        
# Read configuration
read_config()
# init io pin assignments
init_io()
# Create an Event Loop
loop = asyncio.get_event_loop()
# Create a task to run the main function
loop.create_task(main())

try:
    # Run the event loop indefinitely
    loop.run_forever()
except Exception as e:
    print('Error occurred: ', e)
except KeyboardInterrupt:
    print('Program Interrupted by the user')