import socket
import threading
import ssl
import pprint
import itertools
HEADER = 1024
PORT = 5050
SERVER_ADDR = '52.1.123.152'
#SERVER_ADDR = socket.gethostname()




FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(SERVER_ADDR)
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(ADDR)

context = ssl.SSLContext()
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations("server.pem")
context.load_cert_chain(certfile="client.pem", keyfile="client.key")

secure_sock= context.wrap_socket(client)
secure_sock.connect(ADDR)


# verify server

def receive():
    while True:
        try:
            #recibe un mensaje del servidor
            msg = secure_sock.recv(HEADER).decode(FORMAT)
            print(msg)
        except:
            print("An error ocurred!")
            client.close()
            break



def write():
    while True:
        msg = f"{input()}"
        secure_sock.send(msg.encode(FORMAT))

#iniciamos los hilos
#este primer hilo es para que este pendiente del metodo receive
receive_thread = threading.Thread(target=receive)
receive_thread.start()

#Este hilo solo se preocupa de el metodo write
write_thread = threading.Thread(target=write)
write_thread.start()
