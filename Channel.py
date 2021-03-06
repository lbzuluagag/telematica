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
        self.usuarios=[]

    
    def getName(self):
        """
        retorna el name del canal
        """


        return self.name



    def getUsers(self):
        """
        Retorna la lista de usuarios
        """
        return self.usuarios


    def getNames(self):
        """
        Retorna una lista con los nombres de los usuarios en strings
        """
        names=[]
        for n in self.usuarios:
            names.append(n.getName())
        return names


    
    def getUser(self,pos):
        """
        Retorna usuario en la posicion pos
        
        pos -- Posicion
        """


        return self.usuarios[pos]
    
    def addUser(self,name):
        """
        Agrega usuario
        
        name -- name del usuario a crear
        """


        self.usuarios.append(User(name))


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


class MsgCol:
    """
    Clase MsgCol, esta seria en la que estaria toda la informacion de los cols.
    Esta clase contiene la lista de todos los cols, cada uno con su respectiva informacion
    """
    def __init__(self):
        self.cols=[]


    def getMsgCol(self):
        """
        Retorna una cadena con los nombres de los canales/queues
        """
        cols=[]
        for x in self.cols:
            cols.append(x.getName())
        return cols

    def getCol(self,col):
        """
        Retorna el canal deseado si este existe, de lo contrario retorna un mensaje
        """
        try:
           self.getMsgCol().index(col)
           return self.cols[self.getMsgCol().index(col)]
        except :
            return "The col {{channel}} does not exist"


    def createChannel(self,col):
        """
        Busca si el canal que se desea crear existe, de no existir este canal es creado
        """
        try:
           self.getMsgCol().index(col)
           return False, "The col {{col}} already exist"
        except :
            self.cols.append(Channel(col))
            return True, "Col created succesfully"

    def createQueue(self,col):
        """
        Busca si el canal que se desea crear existe, de no existir este canal es creado
        """
        try:
           self.getMsgCol().index(col)
           return False, "The col {{channel}} already exist"
        except :
            self.cols.append(Queue(col))
            return True, "Col created succesfully"


    def deleteCol(self,col):
        """
        Busca si el canal que se desea borrar existe, de no existir este metodo
        retornara un mensaje
        """
        try:
           self.getMsgCol().index(col)
           del self.cols[self.getMsgCol().index(col)]
           return True, "Col deleted"
        except :
            return False, "The col {{col}} does not exist"


    def subscribeCol(self,col,user):
        """
        Conecta el usuario con el canal deseado, en caso de estar ya estar conectado, se le notificara al usuario
        col -- nombre de canal al cual se desea conectar
        user -- usuario que se va a conectar al canal
        """
        users = self.getCol(col).getNames()

        if user not in users:
            self.getCol(col).addUser(user)
            return True, "{user} subscribed to the {col}"
        else:
            return False, "{user} already subscribed to the {col}"


    def connectCol(self,col,user):
        pass



col = MsgCol()
col.createChannel("eafit")
print(col.subscribeCol("eafit","luis"))
print(col.subscribeCol("eafit","luis"))
print(col.getCol("eafit").getNames())
print("Creando colas")
queue= MsgCol()
queue.createQueue("neafit")
queue.createQueue("andres perro hpta")
print(queue.getMsgCol())
print(queue.deleteCol("neafit"))
print(queue.getMsgCol())