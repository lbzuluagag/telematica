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



def write():
        msg = input()
        client.send(msg.encode(FORMAT))


#Este hilo solo se preocupa de el metodo write
#write_thread = threading.Thread(target=write)
#write_thread.start()
write()