class Queue:

    def __init__(self):
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

class Queues:
    """
    Clase cola, aqui se creara lo que viene siendo cada uno de los channels
    con su respectiva lista de usuarios

    name -- name del cola a crear
    """
    def __init__(self,name):
        """
        name -- name del cola
        """
        self.queues=[]

    
    def getChannels(self):
        """
        Retorna una cadena con los nombres de los canales
        """
        queues=[]
        for x in self.channels:
            channels.append(x.getName())
        return channels