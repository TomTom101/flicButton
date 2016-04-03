import time
import os
import lifx

class LifxLights(object):
    def __init__(self):
        self._bedroom = None
        broadcast_addr = os.environ.get('LIFX_BROADCAST', '192.168.0.255')

        # Start the client
        self.lights = lifx.Client(broadcast=broadcast_addr)
        time.sleep(1)

    @staticmethod
    def yield_first(iterable):
        for item in iterable or []:
            yield item
            return

    def by_label(self, label):
        try:
            return self.lights.by_label(label)[0]
        except IndexError:
            return None
