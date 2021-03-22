from momclient import MomClient
momc = MomClient()

def create_channel():
    print("Ingrese el nombre del canal")
    chan_name = input()
    momc.channel_create(chan_name)
    resp, cont = momc.get_nxtmsg()
    return [resp, cont]

def list_channels():
    momc.channel_list()    
    channels = []
    resp, cont = momc.get_nxtmsg()
    inc = 1

    while resp == "INF":
        print(f"{inc}. {cont}")
        channels.append(cont)
        resp, cont = momc.get_nxtmsg()
        inc += 1
    
    return [resp, cont, channels]
    
def delete_channel():
    resp_arr = list_channels()
    if resp_arr[0] == "ERR":
        return resp_arr[:2]

    channels = resp_arr[2]
    ind = int(input("Cual canal? "))
    momc.channel_delete(channels[ind - 1])

    resp, cont = momc.get_nxtmsg()
    return [resp, cont]


def send_mesage():
    resp_arr = list_channels()
    if resp_arr[0] == "ERR":
        return resp_arr[:2]

    channels = resp_arr[2]
    ch_ind = int(input("Cual canal? "))
    
    print("Ingrese los tags del mensaje separados por espacios")
    tags_raw = input()
    tags = []

    if len(tags_raw) > 0:
        tags = tags_raw.split(' ')


    print("Ingrese el contenido del mensaje")
    msg = input()

    momc.channel_recieve(channels[ch_ind - 1], tags, msg)
    resp, cont = momc.get_nxtmsg()

    return [resp, cont]
    

def disconnect_channel():
    resp_arr = list_channels()
    if resp_arr[0] == "ERR":
        return resp_arr[:2]

    channels = resp_arr[2]
    ch_ind = int(input("Cual canal? "))

    momc.channel_disconnect(channels[ch_ind - 1])
    resp, cont = momc.get_nxtmsg()

    return [resp, cont]



def main():
    user = input("Usuario: ")
    passw = input("Contasena: ")

    momc.auth_user(user, passw)
    resp, cont = momc.get_nxtmsg()
    if resp == "ERR":
        print("usuario o contrasena incorrectos")
        return

    while True:
        options =[
            "Digite una opcion",
            "1. Crear canal",
            "2. Borrar canal",
            "3. Listar canales",
            "4. Enviar Mensaje a Canal",
            "5. Desconectarse de canal",
        ]

        for o in options:
            print(o)


        selected = int(input())
        print("seleccion: ", selected);
        funcs = [
            create_channel,
            delete_channel,
            list_channels,
            send_mesage,
            disconnect_channel
        ]
        
        resp_arr = funcs[selected - 1]()
        print(resp_arr[0], resp_arr[1])


main()
