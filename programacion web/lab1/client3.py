# import socket programming library
import socket
from time import sleep
import serial

# jajajaj

HOST = '192.168.43.113 '  # The server's hostname or IP address
PORT = 8890  # The port used by the server
# ardy = serial.Serial('COM', 9600)
# ardy.close()
# ardy.open()
k = False
porta = ['/dev/ttyACM0', '/dev/ttyACM1']
i = 0
#import RPi.GPIO as GPIO

HOST = '192.168.43.113'   # The server's hostname or IP address
PORT = 8890  # The port used by the server
# ardy = serial.Serial('COM', 9600)
# ardy.close()
# ardy.open()
k = False
porta = ['/dev/ttyACM0', '/dev/ttyACM1']
i = 0
ID = 3
sensor = 0

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

######Rasp 1######

##Fan##
PWM_FREQ = 25  # Hz
fanSpeed = 0
# GPIO.setmode(GPIO.BCM)
#GPIO.setup(18, GPIO.OUT, initial=GPIO.HIGH)
#fan1 = GPIO.PWM(18, 100)
#fan1.start(0)

##Led##
#GPIO.setup(27, GPIO.OUT)
ledControl = 0

######Rasp 2######

##Heat##
heatControl = 0
E1 = 0
Y1 = 0
y = 0
# GPIO.setmode(GPIO.BCM)
#GPIO.setup(24, GPIO.OUT)
#heat1 = GPIO.PWM(24, 100)
#heat1.start(100)

##Servo##
doorControl = 0
#GPIO.setup(25, GPIO.OUT)
#door1 = GPIO.PWM(25, 50)
#door1.start(2.5)


def door():
    # start 1500 us servo pulses on gpio2
    # door1.start(2.5)
    #print(doorControl)

    if doorControl:
        #door1.start(2.5)
        #door1.ChangeDutyCycle(12)
        sleep(0.5)
    else:
        #door1.start(2.5)
        #door1.ChangeDutyCycle(6)
        sleep(0.5)


def heat():
    global E1, Y1, y
    Kp = 6.44
    Ki = 8.51
    Ts = 1
    E = 0

    temp = heatControl
    E = temp - sensor
    y = 100 - ((Ki * Ts * E1) - (Kp * E1) + (Kp * E) + Y1)
    if y < 0:
        y = 0
    if y > 100:
        y = 100
    Y1 = y
    E1 = E
    #heat1.start(100)
    #heat1.ChangeDutyCycle(100 - temp)


######Rasp 1######
def fan():
    #print(fanSpeed)
    #fan1.start(24)
    #fan1.ChangeDutyCycle(fanSpeed)
    hi=0


def led():
    if ledControl == 1:
        ti=0
        #GPIO.output(27, True)

    else:
        ti=0
        #GPIO.output(27, False)


while 1:

    if ID == 1:
        fan()
    elif ID == 2:
        heat()
    else:
        a = 0

    global VEC

    S = True
    #sleep(1)

    try:
        if not k:
            ardy = serial.Serial(porta[i], 9600)
            ardy.close()
            ardy.open()
            print("entre")

        sleep(1)

        while S:
            ardy.write(b'a')
            sleep(0.2)
            if ardy.in_waiting > 0:
                print("entre2")
                VEC = ardy.readline().decode().rstrip()
                #sensor = int(VEC)
                print(VEC)
                VEC = '3' + VEC
                k = True
            S = False


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
                ardy.write(b'5')

                s.close()
                k=False

                #sleep(1)
        except:
            print("Connection with Server failed.")
