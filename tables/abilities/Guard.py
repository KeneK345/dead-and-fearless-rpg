from tables.Ability import Ability
import math
class Guard(Ability):
    name = "Em Guarda"
    desc = "Entre em guarda, aumentando sua defesa e evitando alguns ataques especiais"
    def __init__(self, name=name, desc=desc, char=None, id=0, hpCost=0, mpCost=0):
        super().__init__(name, desc, char, id, hpCost, mpCost)

    def callAbility(self):
        self.char.increaseDefMod(math.ceil(self.char.defense/2))
        return True