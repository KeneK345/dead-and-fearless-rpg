from abc import ABC, abstractmethod
class Ability(ABC):
    def __init__(self,name,desc,char,id,hpCost,mpCost):
        self.id=id
        self.char=char
        self.name=name
        self.desc=desc
        self.hpCost=hpCost
        self.mpCost=mpCost
    def __str__(self):
        costs = ""
        if self.hpCost > 0:
            costs += f"\nCusto em vida: {self.hpCost}"
        if self.mpCost > 0:
            costs += f"\nCusto em mente: {self.mpCost}"
        return f"{self.name}\n{self.desc}{costs}"
    def setId(self,newId):
        self.id = newId
        return "Identificado!!!"
    def setCharId(self,char):
        self.char = char
        return "CharIdentificado!!!"

    @abstractmethod
    def callAbility(self):
        pass