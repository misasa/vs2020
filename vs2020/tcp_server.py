import socket
import time
import threading
import sys
server_ip = "127.0.0.1"
server_port = 25252
listen_num = 10
buffer_size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((server_ip,server_port))
s.listen(listen_num)

client_list = []

def recv_client(s, addr):
    while True:
        try:
            data = s.recv(buffer_size)
            if data == b"":
                break
            command = data.decode("utf-8").rstrip()
            print("Recv [{}] from client:{}".format(command, addr))
            vals = command.split()
            cmd = vals[0]
            if cmd == "POSITION":
                msg = "POSITION SUCCESS,1.000,2.000"
                time.sleep(2)
            elif cmd == "MOVE":
                msg = "MOVE SUCCESS"
                time.sleep(10)
            elif cmd == "STOP":
                msg = "STOP SUCCESS"
                time.sleep(2)
            else:
                msg = "UNKNOWN FAILURE"
            print("Send [{}] to client:{}".format(msg, addr))
            s.send(bytes(msg + "\r\n",'utf-8'))
        except Exception as e:
            print(e, file=sys.stderr)
            break
        time.sleep(1)
    s.shutdown(socket.SHUT_RDWR)
    s.close()

while True:
    c, address = s.accept()
    client_list.append((c, address))
    print("+ join client:{}".format(address))
    thread = threading.Thread(target=recv_client, args=(c, address))
    thread.start()