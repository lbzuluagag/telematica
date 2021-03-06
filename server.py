import socket
import threading
#from Channel import *

class ClientConn:
    def __init__(self, client, addr, uname):
        self.client = client
        self.addr = addr
        self.uname = uname


# metodo para enviar mensaje a todos los usuarios conectados
# pendiente mas adelante poner que reciba a que sala debe hacer el broadcast
def broadcast(msg):
    for client in CLIENTS:
        client.send(msg)



def handle(client,addr):
    while True:
        #luego voy a probar poner aqui
        #un if donde dependiendo de que llegue se hace un menu
        try:
            msg=client.recv(HEADER)
            broadcast(msg.encode(FORMAT))
        except:
            index = CLIENTS.index(client)
            CLIENTS.remove(client)
            client.close()
            nickname = NICKNAMES[index]
            broadcast("{} left the chat!".format(nickname).encode(FORMAT))
            NICKNAMES.remove(nickname)
            break



class Server: 
    

    def __init__(self):
        # NETWORKING SETUP-------------------------------------------
        #msg length in bytes
        self.HEADER = 1024
        self.PORT = 5051
        #get IP
        self.SERVER = socket.gethostbyname(socket.gethostname()) 
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        # ----------------------------------------------------------
        self.VERBS = {"ER", "OK"}

        self.clients = {}
        self.conn_users = {}
        #self.channels = Channels() 
        self.channels = None

        self.clients_lock = threading.Lock()
        self.conn_users_lock = threading.Lock()
        self.channels_lock = threading.Lock()

    
    # utilidades del servidor---------------------------------------
    def get_client(self, client):
        retval = None

        self.clients_lock.acquire()
        if client in self.clients: 
            retval =  self.clients[client]
        self.clients_lock.release()

        return retval 

    def add_client(self, client_conn):
        self.clients_lock.acquire()
        self.conn_users_lock.acquire()

        self.clients[client_conn.client] = client_conn
        self.conn_users[client_conn.uname] = client_conn.client

        self.conn_users_lock.release()
        self.clients_lock.release()

    def get_uname(self, uname):
        retval = None

        self.conn_users_lock.acquire()
        if uname in self.conn_users:
            retval = self.conn_users[uname]
        self.conn_users_lock.release()

        return retval
    
    
    def send_msg(self, verb, msg, conn):
        if verb in self.VERBS:
            self.msg = verb+msg
            conn.send(msg.encode(self.FORMAT))


    def rem_client(self, client):
        client.close()
        client_conn = self.get_client(client) 
        if client_conn != None:
            del self.conn_users[client_conn.uname]
            del self.clients[client]

    #---------------------------------------------------------------

    def auth_user(self, usern, client):
        client_conn = self.get_client(client)
        
        if self.get_uname(usern) != None:
            # evitar log in a un usuario ya conectado
            # en otro lado 
            errmsg = f"user {usern} already logged-in"
            print(errmsg)
            return (False, errmsg)
        
        elif client_conn != None:
            # evitar log in desde una conexion que ya esta
            # logeada con un usuario
            errmsg = f"this connection is logged-in as {client_conn.uname}"
            print(errmsg)
            return (False, errmsg)

        else:
            okmsg = f"user {usern} logged-in!"
            print(okmsg)
            return (True, okmsg)
        

    def mom(self, client, addr):
        print("--------------")
        while True: 
            msg = None
            try:
                msg=client.recv(self.HEADER).decode(self.FORMAT)
            except: 
                print("error recieving from client")
                self.rem_client(client)
                return 1
                
            #el mensaje sin el comando
            payload=msg[2:]
            
            if msg.startswith("AU"):
                succ, resmsg = self.auth_user(payload, client)
                if succ:
                    new_client = ClientConn(client, addr, payload)
                    self.add_client(new_client)
                    self.send_msg("OK", resmsg, client)
                else:
                    print(resmsg)
                    self.send_msg("ER", resmsg, client)
            
            else:
                client_conn = self.get_client(client)
                authd = client_conn != None

                if msg.startswith("CC"):
                    okmsg=f"{CHANNELS.createChannel(payload)}"
                    self.send_msg("OK", okmsg, client)

                elif msg.startswith("CD"):
                    CHANNELS.deleteChannel(payload)
                    print(CHANNELS.getChannels())
                    okmsg=f"channel {payload} deleted"
                    self.send_msg("OK", okmsg, client)

                elif msg.startswith("CL"):
                    CHANNELS.getChannels()
                    okmsg=f"Channels list: {CHANNELS.getChannels()}"
                    self.send_msg("OK", okmsg, client)
                    
                elif msg.startswith("CS"):    
                    okmsg=f"{CHANNELS.subscribeChannel(payload,client.uname)}"
    

    def start_mom(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            conn, addr = self.server.accept()
            print(f"Connected with {str(addr)}")
            thread = threading.Thread(target=self.mom, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count }")


#inicia el servidor
print("Starting server...")
srvr = Server()
srvr.start_mom()
