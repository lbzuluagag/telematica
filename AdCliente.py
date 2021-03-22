from momclient import MomClient
from threading import Thread, Lock
from copy import deepcopy
momc = MomClient(blocking = False)
inf_msgs = []
inf_recvd = Lock()
inf_read = True

def read_msgs():    
    global inf_read, inf_recvd
    inf_terms = ["All channels listed", "No channels created"]

    # does this thread have the lock
    # just so that the while doesnt
    # reqcuire te loop every time
    # if inf_read is true
    has_lock = False     

    while True:
        # print(inf_read, has_lock)
        if not has_lock:
            inf_recvd.acquire()
            has_lock = True

        resp, cont = momc.get_nxtmsg() 

        
        # print(resp, cont)
        
        if resp == "INF":
            inf_msgs.append(cont)
            inf_read = False
        elif resp != None:
            if cont in inf_terms:
                inf_read = False
            print(resp, cont)
        
        if not inf_read:
            has_lock = False
            inf_recvd.release()


def list_channels():   
    global inf_read, inf_recvd
    momc.channel_list() 
    
    inf_recvd.acquire() #wait for INFS to be over
    channels = deepcopy(inf_msgs)
    inf_msgs.clear()
    inf_read = True
    inf_recvd.release()

    print(channels)    

    inc = 1
    for ch in channels:
        print(f"{inc}. {ch}")
        inc += 1
   
    return channels
 

def connect_2channel():
    channels = list_channels()
    if len(channels) == 0:
        print("Por favor cree un canal")
    else:    
        ch_ind = int(input("Cual Canal? "))
    
        print("Ingrese los tags del mensaje separados por espacios")
        tags_raw = input()
        tags = []
   
        if len(tags_raw) > 0:
            tags = tags_raw.split(' ')

        momc.channel_connect(channels[ch_ind - 1], tags)


def subscribe_2channel():
    channels = list_channels()
    if len(channels) == 0:
        print("Por favor cree un canal")
    else: 
        ch_ind = int(input("Cual Canal? "))
        momc.channel_subscribe(channels[ch_ind - 1])

    

def recieve_msgs():
    channels = list_channels()
    if len(channels) == 0:
        print("por favor cree un canal")
        return
 

    ch_ind = int(input("Cual Canal? "))
    
    print("Ingrese los tags del mensaje separados por espacios")
    tags_raw = input()
    tags = []

    if len(tags_raw) > 0:
        tags = tags_raw.split(' ')

    
    momc.channel_send(channels[ch_ind - 1], tags)
    
    

def main():
    user = input("Usuario: ")
    passw = input("Contasena: ")

    momc.auth_user(user, passw)
    resp, cont = momc.get_nxtmsg()
    if resp == "ERR":
        print("usuario o contrasena incorrectos")
        return
    

    read_thread = Thread(target=read_msgs)
    read_thread.start()

    while True:
        options =[
            "Digite una opcion",
            "1. Conectarse a un canal",
            "2. Subscribirse a un canal",
            "3. Listar canales",
            "4. Obtener mensajes de canal"
        ]

        for o in options:
            print(o)


        selected = int(input())
        print("seleccion: ", selected);
        funcs = [
            connect_2channel,
            subscribe_2channel,
            list_channels,
            recieve_msgs
        ]
        
        funcs[selected - 1]()
    

main()

