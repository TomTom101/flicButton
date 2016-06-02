#!/usr/bin/python

from lifxlight import LifxLights
from lifx import color

lights = LifxLights()
lights.add_control("80:E4:DA:70:A1:C0", "Deckenlampe")
bed = lights.by_control("80:E4:DA:70:A1:C0")


print ambients

if bed and True:
    print bed.color
else:
    print "no lights"
