from copy import deepcopy

class User:
    """
    Clase usuario, cada uno de los usuario individuales con su respectiva lista de messages
    """
    def __init__(self,name):
        """
        name -- name del usuario
        """
        self.name = name
        self.messages = [] #stores str,set pair
        self.filters = set()


    def setFilters(self, tags):
        self.filters = set()
        for t in tags:
            self.filters.add(t)


    def getMsgs(self):
        msgs = []
        for msg, tags in self.messages:
            for f in self.filters:
                if f in tags:
                    msgs.append(msg)
                    break
        return msgs


    def pushMsg(self, message, tags):
        """
        Agrega un message a la lista de messages

        message -- Message para agregar en la lista
        """
        self.messages.append((message, tags))



class Channel:
    """
    Clase canal, aqui se creara lo que viene siendo cada uno de los cols
    con su respectiva lista de usuarios

    name -- name del canal a crear
    """
    def __init__(self,name,creator):
        """
        name -- name del canal
        """
        self.creator=creator
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
            return False, f"{name} connected to channel {self.name}"
        elif name in self.subbed:
            return False, f"{name} already subbed to channel {self.name}"
        else: 
            self.subbed[name]=User(name) 
            return True, f"{name} subbed to channel {self.name}"


    def storeMsg(self, msg, tags):
        for sub in self.subbed.values():
            sub.pushMsg(msg, tags)
            
        return self.conns.keys()


    def getSubbdMsg(self, usern, filters):
        if usern in self.subbed.keys():
            msgs = subbed[user].getMsgs(filters)
            self.subbed[usern].messages.clear()
            return (True, msgs)
        else:
            return (False, f"User {usern} not subbed")

        
    def addConn(self, name, filters):
        """
        Agrega usuario connectado 
        
        name -- name del usuario a crear
        """
        if name in self.conns: # return error 
            return False, [f"{name} was already connected 
                        to channel {self.name}"]

        else:
            usr_msgs = []
            usr = None

            if name in self.subbed:
                # copiar mensajes y enviarlos
                usr = self.subbed[name]
                usr_msgs = usr.getMsgs(filters)
                usr.messages.clear()
                
                del self.subbed[name]            
            else:
                usr = User(name)
                usr.setFilters(filters)
                
            self.conns[name] = usr
            return True, usr_msgs

    def getConn(self,name):
        if name in self.conns:
            return True
        else:
            return False

class Queue:
    """
    Clase canal, aqui se creara lo que viene siendo cada uno de los cols
    con su respectiva lista de usuarios

    name -- name del canal a crear
    """
    def __init__(self, name, creator):
        """
        name -- name del canal
        """
        self.creator=creator
        self.name=name
        self.conns = set()  # key: name (str) 
        self.messages=[]
        self.index=0

    def getName(self):
        """
        retorna el name del canal
        """
        return self.name


    def getNames(self):
        """
        Retorna una lista con los nombres de los usuarios en strings
        """
        return list(self.conns)
    


    def storeMsg(self, msg):
        self.messages.append(msg)


    def getMsg(self):
        if len(self.messages) > 0 and len(self.conns) > 0:
            self.index = (self.index + 1) % len(self.conns)
            user = list(self.conns)[self.index]
            msg = self.messages.pop() 
            return user, msg
        else:
            return None, "No messages available or no users"

        
    def addConn(self, name):
        """
        Agrega usuario connectado 
        
        name -- name del usuario a crear
        """
        if name in self.conns: # return error 
            return False, [f"{name} was already connected to Queue {self.name}"]
        else: 
            self.conns.add(name)
            return True, [f"{name} connected succesfully to {self.name}"]


    def getConn(self,name):
        if name in self.conns:
            return True
        else:
            return False

#cola = Queue("eafit")
#print(cola)
#cola.addConn("luis")
#cola.addConn("andreshpta")
#cola.storeMsg("1")
#cola.storeMsg("2")
#cola.storeMsg("holi3")
#print(cola.getMsg())
#print(cola.getMsg())
#print(cola.getMsg())
#print(cola.getMsg())
#print(cola.getNames())
#print()
