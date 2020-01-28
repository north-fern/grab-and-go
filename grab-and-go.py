#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# Write your program here

# TEST


import ubinascii, ujson, urequests, utime, random

#for later information and possible further study, putting the API Key 
# elsewhere (not public) might make this easier to protect it. 
#import passwords
#key = passwords.ni

oldKanyeBool = 'true'
Key = 'zNnNwKEfdOammemzcvUawnFpJF5E7lCz_tuKGV2HUb'

## Setting up DriveBase and Sensors
motorLeft = Motor(Port.A)
motorRight = Motor(Port.D)
sensor = UltrasonicSensor(Port.S1)
wheelDiam = 56
wheelSpace = 150
robot = DriveBase(motorLeft, motorRight, wheelDiam, wheelSpace)

  
def SL_setup():
     #SL_setup() creates the link between SystemLinkCloud and the ev3
     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     headers = {"Accept":"application/json","x-ni-api-key":Key}
     return urlBase, headers
     
def Put_SL(Tag, Type, Value):
     #Put_SL() takes the tag, type, and value of the tag and writes it to the website (SLC)
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
     #Get_SL() takes the tag and retrieves the value from SystemLink
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
     # Create_SL() creates a new tag on SystemLink
     urlBase, headers = SL_setup()
     urlTag = urlBase + Tag
     propName={"type":Type,"path":Tag}
     try:
          urequests.put(urlTag,headers=headers,json=propName).text
     except Exception as e:
          print(e)
     

def getKanye():
     ## Type out the desired URL Value
     urlValue = 'http://api.kanye.rest'
     ## Using the MircoPython urequests, go to the site and get the information from it
     ##additionally, convert the file to text (JSON)
     quote = urequests.get(urlValue).text
     ## load it as a MicroPyton json file!
     kanye = ujson.loads(quote)
     #printing that part of the dictionary and adding the little tag "-- Kanye West"
     #print(kanye['quote'] +  '\n-- Kanye West')
     newquote = kanye['quote'] +  '\n-- Kanye West'
     return newquote


def NewKanye(oldKanyeBool):
     KanyeBool = Get_SL('newKanye')
     #print(type(KanyeBool))
     #print(KanyeBool)
     #print(oldKanyeBool)
     if KanyeBool != oldKanyeBool:
          newquote = getKanye()
          formatting = newquote.split()
          #print(formatting)
          #print(len(formatting))
          j = 0
          newtext = ''
          if len(formatting)%3 == 1:
               formatting.append('')
          else if len(formatting)%3 == 2:
               formatting.append('')
               formatting.append('')
          for i in range(0, len(formatting)/3):
               brick.display.text(formatting[3*i] + ' ' + formatting[3*i+1] + ' ' + formatting[3*i+2])
               newtext[i] = formatting[3*i] + ' ' + formatting[3*i+1] + ' ' + formatting[3*i+2] + '\n'
               wait(300)
          Put_SL('KanyeQuote', 'STRING', newtext)
          oldKanyeBool = KanyeBool
          #brick.display.text(newtext)


while True:
    # check speed
    motorSpeed = Get_SL('motorSpeed')
    #print(type(motorSpeed))
    # check turning
    motorTurning = Get_SL('motorTurning')
    #print(type(motorTurning))
    # run motor at speed
    robot.drive(int(motorSpeed), -1*int(motorTurning))
    # read data from sensor
    sensorVal = sensor.distance()
    # write data from sensor to dashboard
    Put_SL('Distance2', 'INT', str(sensorVal))
    NewKanye(oldKanyeBool)

     







