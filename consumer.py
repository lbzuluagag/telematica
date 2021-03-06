import socket
import threading

HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive():

    try:
        msg="PULL"
        client.send(msg.encode(FORMAT))
        client.recv(HEADER).decode(FORMAT)
        msg = client.recv(HEADER).decode(FORMAT)
        print(msg)

    except:
        print("An error ocurred!")
        client.close()


receive()
