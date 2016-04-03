import time
import os
import lifx

class LifxLights(object):
    def __init__(self):
        self._controls = {}
        broadcast_addr = os.environ.get('LIFX_BROADCAST', '192.168.0.255')

        # Start the client
        self.lights = lifx.Client(broadcast=broadcast_addr)
        time.sleep(1)

    def add_control(self, flic_mac, lifx_label):
        self._controls[flic_mac] = lifx_label

    @staticmethod
    def yield_first(iterable):
        for item in iterable or []:
            yield item
            return

    def by_control(self, flic_mac):
        """Get the light controlled by that Flic MAC address"""
        label = self._controls[flic_mac]
        return self.by_label(label)

    def by_label(self, label):
        try:
            return self.lights.by_label(label)[0]
        except IndexError:
            return None
