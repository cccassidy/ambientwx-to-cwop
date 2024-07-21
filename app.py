import json
import socket
import datetime
import time
import urllib3

http = urllib3.PoolManager() 

def lambda_handler(event, context):

    DEVICE_MAC = '<DEVICE MAC ADDRESS>'
    DEVICE_TYPE = '<DEVICE TYPE ie aw2902c>'
    API_KEY = '<AMBIENTWX API KEY>'
    APPLICATION_KEY = 'edf1a355218446179f58e35a66506adde62b54aee1394faebd683358e9cc2666'   ### This is for use only with this API code
    CWOP_ID = '<CWOP_ID>'
    LATLON = '<LATLON_STRING>'

    ### Collect Data
    r = http.request('GET','https://api.ambientweather.net/v1/devices/{}?apiKey={}&applicationKey={}&limit=1'.format(DEVICE_MAC, API_KEY, APPLICATION_KEY))
    raw_data = json.loads(r.data)[0]
    print(raw_data)
    
    ### Confirm Ob Is Recent
    timestamp_from_data = int(raw_data['dateutc']/1000)
    current_time = int(time.time())
    if current_time - timestamp_from_data > 600:
        print('Old Data: ' + str(current_time - timestamp_from_data))
        return -1
    
    ### Send Data
    header = 'user {} pass -1 vers ambientwxtocwop 1.00\r\n'.format(CWOP_ID).encode('ascii')
    print(header)
    if round(raw_data['solarradiation']) >= 1000:
        srad_string = 'l{:03d}'.format(round(raw_data['solarradiation']-1000))
    else:
        srad_string = 'L{:03d}'.format(round(raw_data['solarradiation']))
    data = '{}>APRS,TCPIP*:@{}z{}_{:03d}/{:03d}g{:03d}t{:03d}P{:03d}h{:02d}b{:05d}{}{}\r\n'.format(
        CWOP_ID,
        (datetime.datetime.utcfromtimestamp(int(raw_data['dateutc']/1000))).strftime('%d%H%M'),
        LATLON,
        raw_data['winddir'],
        round(raw_data['windspeedmph']),
        round(raw_data['windgustmph']),
        round(raw_data['tempf']),
        round(raw_data['dailyrainin'] * 100),
        raw_data['humidity'],
        round(raw_data['baromrelin'] * 33.8637526 * 10),
        srad_string,
        DEVICE_TYPE
    )
    print(data)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('cwop.aprs.net', 14580))
    s.recv(1024)
    s.send(header)
    s.send(bytes(data, "ascii"))
    s.close()
