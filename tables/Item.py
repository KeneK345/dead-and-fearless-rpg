class Item:
    def __init__(self, name, desc, attack, defense,id=0):
        self.id=id
        self.name=name
        self.desc=desc
        self.attack=attack
        self.defense=defense
    def __str__(self):
        combatStats = ""
        if self.attack != 0:
            combatStats += f"Ataque: {self.attack}"
        if self.defense != 0:
            if self.attack != 0:
                combatStats += "\n"
            combatStats += f"Defesa: {self.defense}"
        return f"{self.name}\n{self.desc}\n{combatStats}"

    def enchantAttack(self,enchant):
        self.attack += enchant
        return "Encantado!!!"
    def enchantDefense(self,enchant):
        self.defense += enchant
        return "Encantado!!!"

    def setId(self,id):
        self.id = id
        return "Identificado!"