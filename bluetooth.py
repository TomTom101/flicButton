#!/usr/bin/python

import subprocess
import time
from flic import flic
from lifxlight import LifxLights

client = flic.Client()
lights = LifxLights()
lights.add_control("80:E4:DA:70:A1:C0", "Deckenlampe")

class ButtonEventListener(flic.ButtonEventListener):

    def getHash(self):
        return "main"

    def onButtonSingleOrDoubleClickOrHold(self, deviceId, queued, timeDiff, isSingleClick, isDoubleClick, isHold):
        """onButtonSingleOrDoubleClickOrHold(
                const std::string& deviceId,
                const bool& queued,
                const int& timeDiff,
                const bool& isSingleClick,
                const bool& isDoubleClick,
                const bool& isHold);
        """
        manager = client.getManager()
        button = manager.getButton(deviceId)
        light = lights.by_control(button.getDeviceId())

        if light:
            if isSingleClick:
                #bedroom.power_toggle()
                print(light.label + " click ")

            if isDoubleClick:
                print(light.label + " double click")

            if isHold:
                print(light.label + " hold")

buttonEventListener = ButtonEventListener()

def addButtonEventListener(button):
    button.addButtonEventListener(buttonEventListener)

class ButtonListener(flic.ButtonListener):
    def getHash(self):
        return "main"

    def onButtonDiscover(self, button):
        addButtonEventListener(button)

buttonListener = ButtonListener()

class InitializedCallback(flic.CallbackVoid):
    def callback(self):
        print("Initialized")
        manager = client.getManager()
        buttons = manager.getButtons()
        try:
            for button in buttons:
                addButtonEventListener(button)
            manager.addButtonListener(buttonListener)
        except:
            pass

class UninitializedCallback(flic.CallbackBool):
    def callback(self):
        print("Uninitialized")

subprocess.Popen(["./daemon", "-f", "flic.sqlite3"])
time.sleep(2)
init = InitializedCallback()
uninit =  UninitializedCallback()
client.start(init.getCallback(), uninit.getCallback())

client.run()
