class User:
    def __init__(self, id, name, victories=0, defeats=0):
        self.id = id
        self.name = name
        self.__victories = victories
        self.__defeats = defeats

    def __str__(self):
        return f"Usuário: {self.name}\nNúmero de identificação: {self.id}\nVitórias: {self.__victories}\nDerrotas: {self.__defeats}"

    def changeName(self, newName):
        self.name = newName
        return f"Nome de usuário trocado para {self.name}"

    def getUserUpdData(self):
        return (self.name,self.__victories,self.__defeats,self.id)

    def defeat(self):
        self.__defeats += 1
        return "Você falhou..."

    def victory(self):
        self.__victories += 1
        return "Missão cumprida!"