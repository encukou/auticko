import network
import socket
import machine
import time

PORT = 4004

class _Motor:
    def __init__(self, dir_pin, speed_pin):
        self.dir_pin = machine.Pin(dir_pin, machine.Pin.OUT)
        self.speed_pwm = machine.PWM(
            machine.Pin(speed_pin, machine.Pin.OUT), freq=500)

    def stop(self):
        self.speed_pwm.duty(0)

    def _go(self, speed):
        self.speed_pwm.duty(min(11*speed,1024))

    def set_dir(self, dir):
        self.dir_pin.value(dir)

    def set_speed(self, speed=100):
        self._go(speed)

    def forward(self, speed=100):
        self.dir_pin.value(1)
        self._go(speed)

    def backward(self, speed=100):
        self.dir_pin.value(0)
        self._go(speed)

    def set_value(self, value, speed=100):
        value &= 0b11
        if value == 0b01:
            self.dir_pin.value(1)
            self._go(speed)
        elif value == 0b10:
            self.dir_pin.value(0)
            self._go(speed)
        else:
            self.speed_pwm.duty(0)

    def test(self):
        "Run motor test"
        for i in range(5,11,+1):
            print("motor forward %i" % i)
            self.forward(10*i)
            time.sleep(1)
        for i in range(10,1,-1):
            print("motor backward %i" % i)
            self.forward(10*i)
            self.backward(10*i)
            time.sleep(1)
        print("motor stop")
        self.stop()

motor_a = _Motor(dir_pin=0, speed_pin=5)
motor_b = _Motor(dir_pin=2, speed_pin=4)

network.WLAN(network.STA_IF).active(False)

w = network.WLAN(network.AP_IF)
w.active(True)
w.config(essid="auticko", password="microPYthon")
print('network config:', w.ifconfig())

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', PORT))
try:

    prev_byte = None
    while True:
        message, address = s.recvfrom(1)
        for byte in message:
            if byte != prev_byte:
                print('<', '{:b}'.format(byte))
                motor_a.set_value(byte >> 0)
                motor_b.set_value(byte >> 2)
finally:
    s.close()
