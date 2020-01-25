#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# Write your program here
import ubinascii, ujson, urequests, utime, random
     
Key = 'zNnNwKEfdOammemzcvUawnFpJF5E7lCz_tuKGV2HUb'

motor = Motor(Port.A)
sensor = UltrasonicSensor(Port.S1)
     
def SL_setup():
     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     headers = {"Accept":"application/json","x-ni-api-key":Key}
     return urlBase, headers
     
def Put_SL(Tag, Type, Value):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     propValue = {"value":{"type":Type,"value":Value}}
     try:
          reply = urequests.put(urlValue,headers=headers,json=propValue).text
     except Exception as e:
          print(e)         
          reply = 'failed'
     return reply

def Get_SL(Tag):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     try:
          value = urequests.get(urlValue,headers=headers).text
          data = ujson.loads(value)
          #print(data)
          result = data.get("value").get("value")
     except Exception as e:
          print(e)
          result = 'failed'
     return result
     
def Create_SL(Tag, Type):
     urlBase, headers = SL_setup()
     urlTag = urlBase + Tag
     propName={"type":Type,"path":Tag}
     try:
          urequests.put(urlTag,headers=headers,json=propName).text
     except Exception as e:
          print(e)
          
def Get_WEATHER():
     #intval = random.randint(100000,10000000)
     #print(intval)
     #urlValue = "http://api.openweathermap.org/data/2.5/weather?id=" + str(intval) + "&units=imperial&APPID=89c56a7a461ecb8bdb0dd5a686e5aafa"
     #urlValue = 'https://icanhazdadjoke.com/'
     val = "main"
     city = "main"
     try:
          #value = urequests.get(urlValue, {"temp":temp}).text
          #data = ujson.loads(value)
          #print(data)
          while val == "main":
               intval = random.randint(100000,10000000)
               urlValue = "http://api.openweathermap.org/data/2.5/weather?id=" + str(intval) + "&units=imperial&APPID=89c56a7a461ecb8bdb0dd5a686e5aafa"
               result = urequests.get(urlValue)
               print(type(result.json()))
               newresult = result.text
               print(type(newresult))
               extra = ujson.loads(newresult)
               print(extra)
               print(val)
               val = str(extra['main']['feels_like'])
               print(val)
               wait(500)
               city = str(extra['name'])
               if val != "main":
                    print(val)
                    print(city)
     except Exception as e:
          print(e)
          result = 'failed'
     #print(val)
     #print(city)
     print("DONE")
     return val
#distance = Get_SL('Distance')

#Create_SL('Bill','STRING')
#Put_SL('Bill','STRING','done')
#Get_SL('Bill')

#motorSpeed = Get_SL('Motor Speed')
#print(motorSpeed)
Create_SL('Distance2','INT')
Create_SL('WEATHER', 'STRING')
weather = Get_WEATHER()

while True:
    # check motor on status

    # check speed
    motorSpeed = Get_SL('motorSpeed')
    # run motor at speed
    motor.dc(int(motorSpeed))
    # read data from sensor
    sensorVal = sensor.distance()
    # write data from sensor to dashboard
    Put_SL('Distance2', 'INT', str(sensorVal))
    #generate random fact
    #weather = Get_WEATHER()
    #Put_SL('WEATHER', 'STRING', str(weather))



