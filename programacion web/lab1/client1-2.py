# import socket programming library
import socket
from time import sleep
import serial

# jajajaj

# HOST = "192.168.43.176"  # The server's hostname or IP address
# PORT = 8890  # The port used by the server
# ardy = serial.Serial('COM', 9600)
# ardy.close()
# ardy.open()
k = False
porta = ['/dev/ttyACM0', '/dev/ttyACM1']
i = 0
import RPi.GPIO as GPIO

HOST = '192.168.43.113'  # The server's hostname or IP address
PORT = 8890  # The port used by the server
# ardy = serial.Serial('COM', 9600)
# ardy.close()
# ardy.open()
k = False
porta = ['/dev/ttyACM0', '/dev/ttyACM1']
i = 0
ID = 2
sensor = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

######Rasp 1######

##Fan##
PWM_FREQ = 50  # Hz
fanSpeed = 0
# GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)
fan1 = GPIO.PWM(24, PWM_FREQ)
fan1.start(0)

##Led##
GPIO.setup(27, GPIO.OUT)
ledControl = 0

######Rasp 2######

##Heat##
heatControl = 0
E1 = 0
Y1 = 0
y = 0
E = 0
# GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
heat1 = GPIO.PWM(23, 35)
heat1.start(100)

##Servo##
doorControl = 0
GPIO.setup(25, GPIO.OUT)
door1 = GPIO.PWM(25, 50)
door1.start(2.5)


def door():
    # start 1500 us servo pulses on gpio2
    # door1.start(2.5)

    if doorControl:
        #door1.start(2.5)
        door1.ChangeDutyCycle(12)
        sleep(0.5)
    else:
        #door1.start(2.5)
        door1.ChangeDutyCycle(6)
        sleep(0.5)


def heat():
    global E1, Y1, y
    Kp = 8.5
    Ki = 4.45
    Ts = 0.2

    temp = heatControl
    E = temp - sensor
    y = ((Ki * Ts * E1) - (Kp * E1) + (Kp * E) + Y1)
    if y < 0:
        y = 0
    if y > 100:
        y = 100
    Y1 = y
    E1 = E
    heat1.start(100)
    heat1.ChangeDutyCycle(y)


######Rasp 1######
def fan():
    fan1.start(24)
    fan1.ChangeDutyCycle(fanSpeed)


def led():
    if ledControl:
        GPIO.output(17, True)
    else:
        GPIO.output(17, False)


while 1:

    if ID == 1:
        fan()
    elif ID == 2:
        heat()
    else:
        a = 0

    global VEC

    S = True
    # sleep(0.5)

    try:
        if not k:
            ardy = serial.Serial(porta[i], 9600)
            ardy.close()
            ardy.open()

        sleep(0.2)

        while S:
            ardy.write(b'a')
            sleep(0.2)
            if ardy.in_waiting > 0:
                VEC = ardy.readline().decode().rstrip()
                sensor = int(VEC)
                print(">", VEC)
                VEC = '2' + VEC + ",123"
                S = False
                k = True

    except:
        print("Connection with Arduino failed.")
        k = False
        if i == 1:
            i = 0
        else:
            i = 1

        # ardy.close()

    if k:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send(str.encode(VEC))
                data = s.recv(10).decode()
                print(data)
                act = data.split(',')
                heatControl = int(act[0])  # fanControl = act[0]
                doorControl = int(act[1])  # ledControl = act[1]
                door()
                # ardy.write(b'5')

                s.close()

                # sleep(0.5)
        except:
         print("Connection with Server failed.")


