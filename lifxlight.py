import time
import os
import lifx
from lifx import color
from itertools import cycle

class LifxLights(object):
    def __init__(self):
        self._controls = {}
        self._ambients = cycle([
            color.HSBK(0, 0, 1, 6500),
            color.HSBK(0, 0, .3, 3500)
        ])
        broadcast_addr = os.environ.get('LIFX_BROADCAST', '192.168.0.255')

        self.lights = lifx.Client(broadcast=broadcast_addr, discoverpoll=120)
        time.sleep(1)

    def add_control(self, flic_mac, lifx_label):
        self._controls[flic_mac] = lifx_label

    def next_ambient(self, light):
        light.fade_color(self._ambients.next(), 2000)


    def by_control(self, flic_mac):
        """Get the light controlled by that Flic MAC address"""
        label = self._controls[flic_mac]
        return self.by_label(label)

    def __by_label(self, label):
        """Using own filter to get around the last_seen limitation """
        return filter(lambda d: d.label == label, self.lights._devices.values())

    def by_label(self, label):
        try:
            return self.__by_label(label)[0]
        except IndexError:
            print "Label " + label + " not found"
            return None
