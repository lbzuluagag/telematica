from copy import deepcopy

class User:
    """
    Clase usuario, cada uno de los usuario individuales con su respectiva lista de messages
    """
    def __init__(self,name):
        """
        name -- name del usuario
        """
        self.name=name
        self.messages=[]


    def getName(self):
        """
        Retorna name del usuario
        """
        return self.name


    def popMessage(self):
        """
        Retorna el message en la posicion 0, luego lo elimina de la lista
        """

        if len(self.messages)>0:
            return self.messages.pop(0)
        else:
            return "No messages left"
        

    def pushMessage(self,message):
        """
        Agrega un message a la lista de messages

        message -- Message para agregar en la lista
        """
        self.messages.append(message)




class Channel:
    """
    Clase canal, aqui se creara lo que viene siendo cada uno de los cols
    con su respectiva lista de usuarios

    name -- name del canal a crear
    """
    def __init__(self,name):
        """
        name -- name del canal
        """
        self.name=name
        self.conns = {}  # key: name (str) val: userobj
        self.subbed = {} # key: name (str) val: userobj

    
    def getName(self):
        """
        retorna el name del canal
        """
        return self.name


    def getNames(self):
        """
        Retorna una lista con los nombres de los usuarios en strings
        """
        return list(self.conns.keys()) + list(self.subbed.keys())
    

    def addSub(self, name: str):
        """
        Agrega usuario subscrito
        
        name -- name del usuario a crear
        """
        if name in self.conns:
            return 0, f"{name} already subbed to channel {self.name}"
        elif name in self.subbed:
            return 0, f"{name} already subbed to channel {self.name}"
        else: 
            self.conns[name]=User(name) 
            return 1, f"{name} subbed to channel {self.name}"


    def addConn(self, name):
        """
        Agrega usuario connectado 
        
        name -- name del usuario a crear
        """
        if name in self.conns: # return error 
            return 0, [f"{name} was already connected to channel {self.name}"]

        elif name in self.subbed:
            # copiar mensajes y enviarlos
            usr = self.subbed[name]
            usr_msgs = deepcopy(user.messages)
            usr.messages.clear()
            
            self.conn[name] = usr
            del self.subbed[name]

            return 1, usr_msgs

        else:
            self.conns[name] = User(name)
            return 2, [f"{name} connected succesfully to {self.name}"]

    def getConn(self,name):
        if name in self.conns:
            return True
        else:
            return False

class Queue:

    def __init__(self,name):
        self.name=name
        self.messages=[]
        self.users=[]
        self.index=0

    def popMessage(self):
        """
        Retorna el message en la posicion 0, luego lo elimina de la lista
        """

        if len(self.messages)>0:
            return self.messages.pop(0)
        else:
            return "No messages left"


    def pushMessage(self,message):
        """
        Agrega un message a la lista de messages

        message -- Message para agregar en la lista
        """
        self.messages.append(message)

    def getName(self):
        """
        Retorna una lista con los nombres de los usuarios en strings
        """
        return self.name
