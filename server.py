import socket
import threading
from Channel import *

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
        self.VERBS = {"ERR", "OKO"}

        self.clients = {} #k: connection, v: ClientConn
        self.conn_users = {} #k: str (uname), v: connection (socket)
        self.channels = {} # k: str, v: Channel

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


    def rem_client(self, client):
        client.close()
        client_conn = self.get_client(client) 
        if client_conn != None:
            del self.conn_users[client_conn.uname]
            del self.clients[client]


    def get_channel(self, chan_name):
        self.channels_lock.acquire()

        if chan_name in self.channels:
            self.channels_lock.release()
            return self.channels[chan_name]         
        
        self.channels_lock.release()
        return None
        


    def add_channel(self, chan_name):
        self.channels_lock.acquire()

        if chan_name in self.channels:
            self.channels_lock.release()
            return False, f"Channel {chan_name} already exists"
        else:
            self.channels[chan_name] = Channel(chan_name)
            self.channels_lock.release()
            return True, f"Channel {chan_name} created succesfully"   

        


    def rem_channel(self, chan_name):
        self.channels_lock.acquire()

        if payload in self.channels:
            del self.channels[payload]
            resp = f"Channel {payload} deleted succesfully"    
        else:
            succ =  False
            resp = f"Channel {payload} does not exists"

        self.channels_lock.release()
        return resp


    def get_uname(self, uname):
        retval = None

        self.conn_users_lock.acquire()
        if uname in self.conn_users:
            retval = self.conn_users[uname]
        self.conn_users_lock.release()

        return retval
    
    
    def send_msg(self, verb, msg, conn):
        verb = verb.strip()
        if verb in self.VERBS:
            msg = verb+str(msg)
            conn.send(msg.encode(self.FORMAT))

    
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
            payload=msg[3:]
            
            if msg.startswith("AUT"):
                succ, resmsg = self.auth_user(payload, client)
                if succ:
                    new_client = ClientConn(client, addr, payload)
                    self.add_client(new_client)
                    self.send_msg("OKO", resmsg, client)
                else:
                    self.send_msg("ERR", resmsg, client)
            
            else:
                client_conn = self.get_client(client)
                                
                succ = True
                resp = ""
                if  client_conn == None:
                    succ, resp = (False, "Not logged in")

                elif msg.startswith("CCR"): #CHANNEL CREATE
                    succ, resp = self.add_channel(payload)

                elif msg.startswith("CDE"): #CHANNEL DELETE
                    succ, resp = self.del_channel(payload)

                elif msg.startswith("CLI"): #CHANNEL LIST
                    resp = list(self.channels.keys())

                elif msg.startswith("CSU"): #CHANNEL SUB                    
                    channel = self.get_channel(payload)
                    if channel != None: 
                        succ, resp = channel.addSub(client_conn.uname)
                    else:
                        succ, resp = (False, f"Channel {payload} does not exist")
                
                elif msg.startswith("CCO"): #CHANNEL CON                    
                    channel = self.get_channel(payload)
                    if channel != None: 
                        succ, resp = channel.addConn(client_conn.uname)
                        print(channel.conns)
                    else:
                        succ, resp = (False, f"Channel {payload} does not exist")

                elif msg.startswith("CRE"): #CHANNEL RECIEVE (MSG)
                    startind = msg.find(" ")
                    channel = msg[3:startind]
                    msg= msg[startind:]

                    


                    
                else:
                    succ, resp = (False, f"Invalid verb {msg[:2]}")
                
              
                if succ:
                    self.send_msg("OKO", resp, client)
                else:
                    self.send_msg("ERR", resp, client)

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
