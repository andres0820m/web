# import socket programming library
import socket
# import thread module
from _thread import *
import threading
from time import sleep
import os
import termios, sys, os
import sys, termios, atexit
import select as sl
from select import select

# save the terminal settings
fd = sys.stdin.fileno()
new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)
TERMIOS = termios
print_lock = threading.Lock()
ventilator = 0
led_status = 0
door_status = 0
ep2S = [0, 0]  # %fan,led_status,door_status,button
ep2A = [0, 0]
ep1S = [0, 0]  # temperature,light_buld,place_to_start
ep1A = [0, 0]


# switch to normal terminal
def set_normal_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)


# switch to unbuffered terminal
def set_curses_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)


def putch(ch):
    sys.stdout.write(ch)


def getch():
    return sys.stdin.read(1)


def getche():
    ch = getch()
    putch(ch)
    return ch


def kbhit():
    dr, dw, de = select([sys.stdin], [], [], 0)
    return dr != []


# thread fuction
def threaded(c):
    while True:

        # data received from client
        # c.send(str.encode(" "))
        try:
            rdy_read, rdy_write, sock_err = sl.select([c, ], [], [])
        except select.error:
            print('error')
        if len(rdy_read) > 0:
            data = c.recv(32)
            #data2=data
            if len(data) == 0:
                stop = True
            else:

                if data.rstrip() == 'quit':
                    stop = True

        else:
         stop = True

        stringdata = data.decode()
        #print(data)
        if not data:
            print_lock.release()
            break

        elif (stringdata[0] == '2'):
            client2(data, c)
            #print("entre")
        elif (stringdata[0] == '1'):
            client1(data, c)
        elif (stringdata[0] == '3'):
            client3(data, c)
        else:
            print(stringdata)
            print_lock.release()
            c.send(str.encode(" "))

    c.close()



def Main():
    host = "192.168.43.113"
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 8890
    # port = 8099
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    # put the socket into listening mode
    s.listen(10)
    # print("socket is listening")
    start_new_thread(menu, (1,))
    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()
        #print("aqui me vuelvo popo ")
        # c.send(str.encode(h))
        # lock acquired by client
        print_lock.acquire()
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))

    s.close()


def client2(data, c):
    #h = ''.join(map(str, ep2A))  # conver the list in to a string
    h=""
    h=h+str(ep2A[0])+","+str(ep2A[1])
    #print(h)
    c.send(str.encode(h))
    data = data.decode('utf-8')

    data2 = data[1:]
    try:
        h = data2.split(',')
        #print(h)
        ep2S[0] = h[0]
        #ep2S[1] = h[1] # potenciometro
    except:
        print("data is wrong !! ")


def client1(data, c):
    h = ""
    h = h + str(ep1A[0]) + "," + str(ep1A[1])
    #print(h)
    c.send(str.encode(h))
    data = data.decode('utf-8')

    data2 = data[1:]
    try:
        h = data2.split(',')
        #print(h)
        ep2S[1] = h[0]
    except:
        print("data is wrong !! ")



def client3(data, c):
    p=data.decode('utf-8')
    g= p.split(',')
    #print(g)
    if(g[0]=='31'):
        #print("entre")
        ep1S[1]=1
    else:
        ep1S[1]=0
    if(g[1]=='1'):
        ep1S[0]=1
    else:
        ep1S[0]=0





def print_menu():  ## Your menu design here
    print(30 * "-", "MENU", 30 * "-")
    print("1. Set Fan")
    print("2. Set Temperature")
    print("3. Turn on_of alarm")
    print("4. Open close door")
    print("5. Show Sensors information")
    print("")
    print("6. Exit")
    print(67 * "-")
    look = 0


def menu(h):
    while True:
        print_menu()  ## Displays menu
        choice = input("Enter your choice [1-5]: ")

        if choice == '1':
            print("Menu 1 has been selected")
            data = input("Select the % of the fan between 0 to 100 ")
            ep1A[0] = int(data)  # ep2A[0]= light buld
            ## You can add your code or functions here
        elif choice == '2':
            print("Menu 2 has been selected")
            data = input("Select the % of the heat between 0 to 100 c ")
            ep2A[0] = int(data) # ep2A[0]= light buld
            ## You can add your code or functions here
        elif choice == '3':
            print("Menu 3 has been selected")
            data = input("0 to close 1 to open")
            print()
            if (data == '0' or data == '1'):
                ep1A[1] = data
            else:
                print("Error")
        elif choice == '4':
            print("menu 4 has been selected")
            data = input("0 to close 1 to open")
            print()
            if (data == '0' or data == '1'):
                ep2A[1] = data
            else:
                print("Error")
            ## You can add your code or functions here
        elif choice == '5':
            os.system("clear")
            # print("Menu 4 has been selected")
            N = True
            k = "s"
            while N:
                os.system("clear")
                print("temperatura : ", ep2S[0], " pot ", ep2S[1], " boton: ", ep1S[0], "presencia: ",
                      ep1S[1])
                sleep(0.3)
                if (kbhit()):
                    k = getch()
                    print(k)

                # print(k)
                if k == '\n':
                    N = False

            ## You can add your code or functions here
        elif choice == '6':
            print("Menu 6 has been selected")
            ## You can add your code or functions here
            loop = False  # This will make the while loop to end as not value of loop is set to False
            os._exit(0)
        else:
            # Any integer inputs other than values 1-5 we print an error message
            input("Wrong option selection. Enter any key to try again..")




if __name__ == '__main__':
    Main()
