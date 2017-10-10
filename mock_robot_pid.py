from time import sleep
import threading

class MockRobotEncoder(object):
    def __init__(self, speed_error):
        self._speed_error = speed_error
        self._value = 0
        self._total = 0
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
            #sleep differing amounts based on the speed and error introduced
            sleep(interval * (2 - self._speed) * self._speed_error)

    def _increment(self):
        self._value += 1
        self._total += 1

    @property
    def value(self):
        return int(self._value)

    @property
    def speed(self):
        return self._speed

    @property
    def total(self):
        return int(self._total)

    @speed.setter
    def speed(self, value):
        self._speed = value 

#constants
KP = 0.1
KD = 0.025
KI = 0.01
TARGET = 7
SAMPLETIME = 1

#create 2 encoders
e1 = MockRobotEncoder(1.13)
e2 = MockRobotEncoder(0.87)
#e2.speed = 0.615

#create robot
#r = Robot((1,2), (3,4))
m1_speed = 0.5
m2_speed = 0.5
#r.value = (m1_speed, m2_speed)

e1_prev_error = 0
e2_prev_error = 0

e1_sum_error = 0
e2_sum_error = 0

while True:

    e1_error = TARGET - e1.value
    e2_error = TARGET - e2.value

    e1_sum_error += e1_error
    e2_sum_error += e2_error

    e1_adj = (e1_error * KP) + (e1_prev_error * KD) + (e1_sum_error * KI)
    e2_adj = (e2_error * KP) + (e2_prev_error * KD) + (e2_sum_error * KI)

    e1_prev_error = e1_error
    e2_prev_error = e2_error

    print("error1 {} error2 {} adj1 {} adj2 {}".format(e1_error, e2_error, e1_adj, e2_adj))

    m1_speed += e1_adj
    m2_speed += e2_adj
    
    print("e1 {} e2 {} m1 {} m2 {}".format(e1.value, e2.value, m1_speed, m2_speed))

    e1.speed = m1_speed
    e2.speed = m2_speed

    # update the robots speed
    #r.value = (m1_speed, m2_speed)

    e1.reset()
    e2.reset()

    sleep(SAMPLETIME)