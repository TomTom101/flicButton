#!/usr/bin/python

from flic import flic
from lifxlight import LifxLights

client = flic.Client()
lights = LifxLights()

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
        bedroom = lights.by_label("Deckenlampe")
        if bedroom:
            if isSingleClick:
                #bedroom.power_toggle()
                print(button.getDeviceId() + " click ")

            if isDoubleClick:
                print(button.getDeviceId() + " double click")

            if isHold:
                print(button.getDeviceId() + " hold")

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
