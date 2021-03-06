import socket
import threading


HEADER = 1024
PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def receive():
    while True:
        try:
            #recibe un mensaje del servidor
            msg = client.recv(HEADER).decode(FORMAT)
            #dependiendo de que mensaje reciba, hace algo
            if msg =="nickname":
                client.send(nickname.encode(FORMAT))
            elif len(msg)>1:
                print(msg)
        except:
            print("An error ocurred!")
            client.close()
            break



def write():
    while True:
        msg = f"{input()}"
        client.send(msg.encode(FORMAT))
        res = client.recv(HEADER).decode(FORMAT)
        print(res)

#iniciamos los hilos
#este primer hilo es para que este pendiente del metodo receive
#receive_thread = threading.Thread(target=receive)
#receive_thread.start()

#Este hilo solo se preocupa de el metodo write
write_thread = threading.Thread(target=write)
write_thread.start()
