import network
import socket
import machine
import time

PORT = 4004

network.WLAN(network.AP_IF).active(False)

w = network.WLAN(network.STA_IF)
w.active(True)
w.connect("auticko", "microPYthon")
print("connecting")
while not w.isconnected():
    pass

print("wifi connected")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("connected")

lb = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
lf = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
rb = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
rf = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)

prev_time = 0
prev_result = None

while 1:
    result = 0b0000
    if not lb.value():
        result |= 0b00001
    if not lf.value():
        result |= 0b00010
    if not rb.value():
        result |= 0b00100
    if not rf.value():
        result |= 0b01000

    now = time.ticks_us()
    if result != prev_result or now > prev_time + 100000:
        print('>', '{:b}'.format(result))
        prev_time = now
        prev_result = 0
        s.sendto(bytes([result]), ("192.168.4.1", PORT))

    time.sleep(0.01)
