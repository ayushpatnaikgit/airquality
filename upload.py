import requests
import sys
import datetime
from SDSLinux import *
AQI = loop(USBPORT)
sample = open('/home/pi/data/airquality.txt', 'a')

print(str(datetime.datetime.now()) + " PM2.5: "+str(AQI[0])," PM10: "+str(AQI[1]), file = sample) 
sample.close() 

sensorReadings = [   

  {'specie':'pm25', 'value': AQI[0]},  

  {'specie':'pm10', 'value': AQI[1]}  

] 

 

# Station parameter   

station = { 

  'id':    "SW-Karjat",  

  'name':   "Still Waters",  

  'location':  { 

    'latitude': 18.9323,  

    'longitude': 73.34170

  } 

} 

 

# User parameter - get yours from https://aqicn.org/data-platform/token/ 

userToken = sys.argv[1] 

 

# Then Upload the data  

params = {'station':station,'readings':sensorReadings,'token':userToken}  

request = requests.post( url = "https://aqicn.org/sensor/upload/",  json = params) 

#print(request.text) 

data = request.json()  

 

if data["status"]!="ok": 

  print("Something went wrong: %s" % data) 

else: 

  print("Data successfully posted: %s"%data) 