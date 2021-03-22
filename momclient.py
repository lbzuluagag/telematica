import socket 
import threading
import ssl
import pprint
import itertools

SERVER_ADDR = '52.1.123.152'
#SERVER_ADDR = socket.gethostname()

class MomClient:
    def __init__(self, blocking=True):

        self.HEADER = 1024
        self.FORMAT = 'utf-8'
        self.blocking =  blocking
        PORT = 5051

        SERVER = socket.gethostbyname(SERVER_ADDR)
        ADDR = (SERVER, PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        context = ssl.SSLContext()
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations("server.pem")
        context.load_cert_chain(certfile="client.pem", keyfile="client.key")

        self.secure_sock = context.wrap_socket(self.client)
        self.secure_sock.connect(ADDR)
        if not blocking:
            self.secure_sock.setblocking(0)



    def get_nxtmsg(self):
        conn_error = False

        try:
            raw_msg = self.secure_sock.recv(self.HEADER).decode(self.FORMAT)
            conn_error = len(raw_msg) < 3 
        except:
            conn_error = self.blocking
            return None, None
            
        if conn_error:
            print("Oy vey!")
            self.client.close()
            return None, None

        return raw_msg[:3], raw_msg[3:]

    def _send_msg(self, verb, msg):
        print("msg to server", verb, msg)
        verb = verb.strip()
        msg = verb + str(msg)
        try:
            self.secure_sock.send(msg.encode(self.FORMAT))
        except Exception as e:
            print("error sending msg:", e)
 

    def auth_user(self, user, passw):
        self._send_msg("AUT", user + ' ' + passw)

    def channel_create(self, channel_name):
        self._send_msg("CCR", channel_name)
    
    def channel_delete(self, channel_name):
        self._send_msg("CDE", channel_name)

    def channel_list(self):
        self._send_msg("CLI", '')
    
    def channel_subscribe(self, channel_name):
        self._send_msg("CSU", channel_name)

    def channel_connect(self, channel_name, filters):
        msg = f"{channel_name} {len(filters)}"
        for f in filters:
            msg += ' ' + f
        self._send_msg("CCO", msg)

    def channel_recieve(self, channel_name, tags, payload):
        msg = f"{channel_name} {len(tags)}"
        for t in tags:
            msg += ' ' + t
        msg += ' ' + payload
        
        self._send_msg("CRE", msg)

    def channel_send(self, channel_name, filters):
        msg = f"{channel_name} {len(filters)}"
        for f in filters:
            msg += ' ' + f
        self._send_msg("CSE", msg)
    
    def queue_create(self, queue_name):
        self._send_msg("QCR", queue_name)

    def queue_delete(self, queue_name):
        self._send_msg("QDE", queue_name)

    def queue_list(self):
        self._send_msg("QLI", '')
    
    def queue_connect(self, queue_name):
        self._send_msg("QCO", queue_name)

    def queue_recieve(self, queue_name, msg):
        self._send_msg("QRE", queue_name + ' ' + msg)

    def disconnect(self):
        self._send_msg("DEL", '')


