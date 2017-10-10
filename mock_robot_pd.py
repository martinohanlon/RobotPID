from time import sleep
import threading

class MockRobotEncoder(object):
    def __init__(self, speed_error):
        self._speed_error = speed_error
        self._value = 0
        self.speed = 0.5

        self._t = threading.Thread(
            target = self._mock_encoder,
            args = (0.1,))
        self._t.start()

    def reset(self):
        self._value = 0

    def _mock_encoder(self, interval):
        while True:
            self._increment()
            sleep(interval)

    def _increment(self):
        self._value += (self._speed) 

    @property
    def value(self):
        return int(self._value)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value * self._speed_error

target = 7
KP = 0.05
KD = 0.025

e1 = MockRobotEncoder(1.1)
e2 = MockRobotEncoder(0.9)
#e2.speed = 0.615

previous_error = 0

while True:
    print("1={} 2={}".format(e1.value, e2.value))

    error_p = float(e1.value) - float(e2.value)
    error_d = error_p - previous_error
    previous_error = error_p

    e2.speed += (error_p * KP) + (error_d * KD)

    sleep(1)