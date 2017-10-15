import threading
from gpiozero import DigitalInputDevice, Robot
from time import sleep

class Encoder(object):
    def __init__(self, pin):
        self._value = 0

        encoder = DigitalInputDevice(pin)
        encoder.when_activated = self._increment
        encoder.when_deactivated = self._increment
        
    def reset(self):
        self._value = 0

    def _increment(self):
        self._value += 1

    @property
    def value(self):
        return self._value

SAMPLETIME = 1
TARGET = 45
KP = 0.02

r = Robot((10,9), (8,7)) 
e1 = Encoder(17)
e2 = Encoder(18)

m1_speed = 1
m2_speed = 1
r.value = (m1_speed, m2_speed)

while True:

    e1_error = TARGET - e1.value
    e2_error = TARGET - e2.value

    m1_speed += e1_error * KP
    m2_speed += e2_error * KP

    m1_speed = max(min(1, m1_speed), 0)
    m2_speed = max(min(1, m2_speed), 0)

    r.value = (m1_speed, m2_speed)

    print("e1 {} e2 {}".format(e1.value, e2.value))
    print("m1 {} m2 {}".format(m1_speed, m2_speed))

    e1.reset()
    e2.reset()

    sleep(SAMPLETIME)