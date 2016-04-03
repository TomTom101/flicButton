#!/usr/bin/python

import time
from flic import flic
from lifxlight import LifxLights

client = flic.Client()
lights = LifxLights()
lights.add_control("80:E4:DA:70:A1:C0", "Deckenlampe")

class ButtonEventListener(flic.ButtonEventListener):

    def getHash(self):
        return "main"

    def onBatteryStatus(self, deviceId, battery):
        print "Battery for " + deviceId + " is " + battery

    def onReady(self, deviceId):
        print "Ready!"

    def onConnecting(self, deviceId):
        print "Connecting to " + deviceId

    def onConnect(self, deviceId):
        print "Connected to " + deviceId

    def onConnectionFail(self, deviceId):
        print "Connection failed to " + deviceId

    def onDisconnect(self, deviceId):
        print "disconnected from " + deviceId

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
                print(light.label + " click")
                light.power_toggle()

            if isDoubleClick:
                print(light.label + " double click")
                """If the light is off, honey sleeping, set a dim color first and turn on"""
                if not light.power:
                    print "Light is off, quite!"
                    lights.set_dim_ambient(light)
                    light.fade_power(True, 0)

                time.sleep(5)
                light.fade_power(0, 2 * 60 * 1000)

            if isHold:
                print(light.label + " hold")
                lights.next_ambient(light)
        else:
            print "No light found for " + button.getDeviceId()

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

init = InitializedCallback()
uninit =  UninitializedCallback()
client.start(init.getCallback(), uninit.getCallback())

client.run()
