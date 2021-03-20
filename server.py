import socket
import threading
from Channel import Channel, Queue
import json

class ClientConn:
    def __init__(self, client, usern):
        self.client = client
        self.usern = usern


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
        self.clients = {} # k: socket, v: ClientConn 
        self.channels = {} # k: str, v: Channel
        self.conn_users = {} # k: str(usern), v: socket
        self.queues = {} # k: str, v: Queue

    def send_msg(self, verb, msg, conn):
        verb = verb.strip()
        msg = verb+str(msg)
        conn.send(msg.encode(self.FORMAT))
    #---------------------------------------------------------------
    
    def auth_user(self, payload, client):
        usern = None
        passw = None
        
        succ = True
        resp = ""
        
        try:
            usern, passw = payload.split(' ')
            print(usern, passw)
        except:
            errmsg = """please provide user and password 
                    separated by a space"""
            return (False, errmsg)


        if usern in self.conn_users:
            # evitar log in a un usuario ya conectado
            # en otro lado 
            errmsg = f"user {usern} already logged-in"
            print(errmsg)
            succ, resp = (False, errmsg)

        elif client in self.clients: #possible thread err here
            # evitar log in desde una conexion que ya esta
            # logeada con un usuario
            client_conn = self.clients.get(client)
            errmsg = f"this connection is logged-in as {client_conn.usern}"
            print(errmsg)
            succ, resp = (False, errmsg)

        else:
            try:
                f = open("auth.json")
                auth = json.load(f)
                auth = auth[0]
                if auth[usern] == passw:
                    self.clients[client] = ClientConn(client, usern)
                    self.conn_users[usern] = client   

                    okmsg = f"user {usern} logged-in!"
                    print(okmsg)
                    succ, resp = (True, okmsg)
                else:
                    errmsg=f"user not registred"
                    print(errmsg)
                    succ, resp = (False, errmsg)
            except e:
                    errmsg=f"Something went wrong"
                    print(errmsg, e)
                    succ, resp = (False, errmsg)
            
        return succ, resp
    

    def create_channel(self, payload):
        if payload in self.channels:
            return False, f"Channel {payload} already exists"
        else:
            self.channels[payload] = Channel(payload)
            return True, f"Channel {payload} created succesfully"   

    
    def create_queue(self, payload):
        if payload in self.queues:
            return False, f"Queue {payload} already exists"
        else:
            self.queues[payload] = Queue(payload)
            return True, f"Queue {payload} created succesfully"

    
    def channel_delete(self, payload):
        if payload not in self.channels:
            return False, f"Channel {payload} does not exist"
        else:
            del self.channels[payload]
            return True, f"Channel {payload} deleted succesfully"


    def queue_delete(self, payload):
        if payload not in self.queues:
            return False, f"Queue {payload} does not exist"
        else:
            del self.queues[payload]
            return True, f"Queue {payload} deleted succesfully"
    

    def subscribe_channel(self, payload, usern):
        channel = self.channels.get(payload)
        succ = True
        resp = ""
        if channel != None: 
            succ, resp = channel.addSub(usern)
        else:
            succ, resp = (False, f"Channel {payload} does not exist")

        return succ, resp
    

    def connect_channel(self, payload, usern):
        channel = self.channels.get(payload)
        succ = True
        resp = ""
        if channel != None: 
            succ, resp = channel.addConn(usern)
            print(channel.conns)
        else:
            succ, resp = (False, f"Channel {payload} does not exist")

        return succ, resp 


    def connect_queue(self, payload, usern):
        queue = self.queues.get(payload)
        succ = True
        resp = ""
        if queue != None:
            succ, resp = queue.addConn(usern)
            print(queue.conns)
        else:
            succ, resp = (False, f"Queue {payload} does not exist")
        
        return succ, resp

    
    def recieve_msg(self, payload):
        succ = True
        resp = ""
        msg = ""
        try:
            print(payload)
            startind = payload.find(" ")
            channel_name = payload[:startind]
            msg = payload[startind:]
        except:
            errmsg = "Error parsing message"
            return False, errmsg

        channel = self.channels.get(channel_name)
        if channel != None: 
            conn_users = channel.storeMsg(msg)
            msg = channel_name + " " + msg
            for usern in conn_users:
                tmp_client_conn = self.conn_users.get(usern)
                self.send_msg("MSG", msg, tmp_client_conn) 
            succ, resp = (True, "Succesfully sent message")
        else: 
            succ, resp = (False, f"Channel {channel_name} does not exist")
         

        return succ, resp


    def send_msglist(self, payload, client_conn):
        channel = self.channels.get(payload)
        succ, resp = False, ""
        if channel != None:
            msgs_succ, msgs_tosend = channel.getSubbdMsg(client_conn.usern)
            if msgs_succ:
                for nxt_msg in msgs_tosend:
                    nxt_msg = channel.name + " " + nxt_msg
                    self.send_msg("MSG", nxt_msg, client_conn.client)

                succ, resp = (True, "All messags recieved")
            else:
                succ, resp = (False, f"User {client_conn.usern} is not subbed to {payload}")
 
        else:
            succ, resp = (False, f"Channel {payload} does not exist")
        
        return succ, resp

    
    def request_handler(self, verb, payload, client):
        succ, resp = False, ""

        if verb == "AUT":
            succ, resp = self.auth_user(payload, client)
            
        else:
            client_conn = self.clients.get(client)
            if client_conn == None:
                succ, resp = (False, "Not logged in")
            else:
                usern = client_conn.usern
                request_fns = {
                       "CCR": lambda: self.create_channel(payload),
                       "QCR": lambda: self.create_queue(payload),
                       "CDE": lambda: self.channel_delete(payload),
                       "QDE": lambda: self.queue_delete(payload),
                       "CLI": lambda: (True, list(self.channels.keys())),
                       "QLI": lambda: (True, list(self.queues.keys())),
                       "CSU": lambda: self.subscribe_channel(payload, usern),
                       "CCO": lambda: self.connect_channel(payload, usern),
                       "QCO": lambda: self.connect_queue(payload, usern),
                       "CRE": lambda: self.recieve_msg(payload),
                       "CSE": lambda: self.send_msglist(payload, client_conn)
                }
        
                func = request_fns.get(verb);     
                if func != None:
                    succ, resp = func()
                else:
                    succ, resp = False, "{verb} is not a valid verb"
        
        if succ:
            self.send_msg("OKO", resp, client)
        else:
            self.send_msg("ERR", resp, client)

    

    def mom(self, client, addr):
        print("--------------")
        while True:      
            raw_msg = None
            try:
                raw_msg=client.recv(self.HEADER).decode(self.FORMAT)
            except: 
                print("error recieving from client")
                client_conn = self.clients.get(client)
                if client_conn != None:
                    del self.conn_users[client_conn.usern]   
                    del self.clients[client]
        
            payload=raw_msg[3:]
            request_verb = raw_msg[:3].upper()
            self.request_handler(request_verb, payload, client)                


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
