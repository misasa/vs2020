import socket
import time
import threading
import sys
import os
from os.path import expanduser
from optparse import OptionParser

parser = OptionParser("""usage: %prog [options]

NAME
  demo_terminal.py -- TCP server with dummy stage controller

SYNOPSIS
  python -m vs2020.demo_terminal [options]

DESCRIPTION
  TCP server with dummy stage controller. The stage position can be
  moved by keyboard input or command by vs2020-sentinel.  Type `quit'
  to terminate session.  Communication log will be stored to
  `~/stage.log'.  This program is fork of tcp_server.py.

IMPLEMENTATION
  Copyright (c) 2025 IPM, Okayama University
  Licensed under the same terms as Python

HISTORY
  January 16, 2025: MY creates this fork to communicate with vs2020-sentinel without VisualStage
""")
parser.add_option("-v","--verbose",action="store_true",dest="verbose",default=False,help="make lots of noise")
(options, args) = parser.parse_args()

server_ip = "127.0.0.1"
server_port = 25252
listen_num = 10
buffer_size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((server_ip,server_port))
s.listen(listen_num)

client_list = []
position_x = 0.0
position_y = 0.0

def recv_client(s, addr):
    global position_x
    global position_y

    log_path = os.path.join(expanduser("~"),'stage.log')
    while True:
        try:
            data = s.recv(buffer_size)
            if data == b"":
                break
            command = data.decode("utf-8").rstrip()
            with open(log_path,'a') as fileout:
                print("Recv [{}] from client:{}".format(command, addr),file=fileout)
            vals = command.split()
            cmd = vals[0]
            if cmd == "POSITION":
                msg = "POSITION SUCCESS,{0},{1}".format(position_x,position_y)
                time.sleep(2)
            elif cmd == "MOVE":
                poss = vals[1].split(",")
                position_x = poss[0]
                position_y = poss[1]
                msg = "MOVE SUCCESS"
                time.sleep(2)
            elif cmd == "STOP":
                msg = "STOP SUCCESS"
                time.sleep(2)
            else:
                msg = "UNKNOWN FAILURE"
            with open(log_path,'a') as fileout:
                print("Send [{}] to client:{}".format(msg, addr),file=fileout)
            s.send(bytes(msg + "\r\n",'utf-8'))
        except Exception as e:
            print(e, file=sys.stderr)
            break
        time.sleep(1)
    s.shutdown(socket.SHUT_RDWR)
    s.close()

def is_float(s):
    try:
        f=float(s)
        return True
    except:
        return False

def wait_input():
    global position_x
    global position_y

    time.sleep(1)
    while True:
        try:
            inp = input("Move stage from ({},{}) to [x,y]$ ".format(position_x,position_y))
            if inp == "":
                continue
            elif inp == "quit":
                os._exit(0)
            poss = inp.split(",")
            if is_float(poss[0]) and is_float(poss[1]):
                position_x = poss[0]
                position_y = poss[1]
                print("X: ", position_x)
                print("Y: ", position_y)
                time.sleep(1)
            else:
                print("Invalid input")
                continue
        except Exception as e:
            print(e, file=sys.stderr)

thread2 = threading.Thread(target=wait_input, daemon=True)
thread2.start()

try:
    while True:
        c, address = s.accept()
        client_list.append((c, address))
        print("+ join client:{}".format(address))
        thread = threading.Thread(target=recv_client, args=(c, address))
        thread.start()
except Exception as e:
    print(e, file=sys.stderr)
