import math,random,time
class Character:
    def __init__(self,id,name,player,archetype,maxHP,health,maxMP,mind,weapon,armor,baseATK,attack,modATK,baseDEF=0,defense=0,modDEF=0,abilities=[],gameStage=0):
        self.id = id
        self._name = name
        self.player = player
        self.archetype = archetype
        self.maxHP = maxHP
        self.health = health
        self.maxMP = maxMP
        self.mind = mind
        self.weapon = weapon
        self.armor = armor
        self.baseATK = baseATK
        self.attack = attack
        self.modATK = modATK
        self.baseDEF = baseDEF
        self.defense = defense
        self.modDEF = modDEF
        self.abilities = abilities
        self.gameStage = gameStage

    def __str__(self):
        return f"{self._name}\n{self.archetype}\nVida: {self.health}/{self.maxHP}\tSanidade: {self.mind}/{self.maxMP}\nAtaque: {self.baseATK}-{self.attack}\tDefesa: {self.defense}"

    def basicInfo(self):
        return f"{self._name} HP: {self.health}/{self.maxHP}"

    def getCharUpdData(self):
        return (self.maxHP,self.health,self.maxMP,self.mind,self.baseATK,self.attack,self.modATK,self.baseDEF,self.defense,self.modDEF,self.gameStage,self.id)

    def updAtk(self, newWeap):
        self.attack = self.baseATK + newWeap
        print("Dano atualizado")
        time.sleep(1)
        return self.attack
    def increaseBaseAtk(self, plusAtk):
        self.baseATK += plusAtk
        self.attack += plusAtk
        print("Dano base aumentado")
        time.sleep(1)
        return self.baseATK
    def decreaseBaseAtk(self, lossAtk):
        self.baseATK -= lossAtk
        self.attack -= lossAtk
        print("Dano base reduzido")
        time.sleep(1)
        return self.baseATK
        
    def updDef(self, newArmor):
        self.defense = self.baseDEF + newArmor
        print("Armadura atualizada")
        time.sleep(1)
        return self.defense
    def increaseBaseDef(self, plusDef):
        self.baseDEF += plusDef
        self.defense += plusDef
        print("Armadura base aumentada")
        time.sleep(1)
        return self.baseDEF
    def decreaseBaseDef(self, lossDef):
        self.baseDEF -= lossDef
        self.defense -= lossDef
        print("Armadura base reduzida")
        time.sleep(1)
        return self.baseDEF

    def calculateNewItem(self):
        totalATK = self.weapon.attack + self.armor.attack
        self.updAtk(totalATK)
        totalDEF = self.weapon.defense + self.armor.defense
        self.updDef(totalDEF)
        return "Atributos atualizados de acordo com itens"
    def obtainNewWeapon(self, weapon):
        self.weapon = weapon
        self.calculateNewItem()
        return "Nova arma!!!"
    def obtainNewArmor(self, armor):
        self.armor = armor
        self.calculateNewItem()
        return "Nova armadura!!!"

    def takeDMG(self, damage):
        processedDefense = self.defense + self.modDEF
        damageTaken = 0
        if damage > processedDefense:
            damageTaken = damage-math.ceil(processedDefense/4)
            self.health -= damageTaken
        elif ((damage*5) - processedDefense) <= 0:
            print(f"{self.name} absorveu o ataque!")
            time.sleep(1)
            return ((damage*5) - processedDefense)
        else:
            damageTaken = damage - math.floor(processedDefense/5)
            self.health -= damageTaken
        print(f"{self._name} levou {damageTaken} de dano")
        time.sleep(1)
        return damageTaken
    def healHP(self, heal, doPrint=True):
        overheal = 0
        oldHealth = self.health
        self.health += heal
        if self.health > self.maxHP:
            overheal = self.health - self.maxHP
            self.health = self.maxHP
        if doPrint:
            if oldHealth == self.health:
                print("Vida já está no máximo")
                time.sleep(1)
            else:
                print(f"Vida restaurada em {self.health-oldHealth}")
                time.sleep(1)
        return self.health-oldHealth, overheal
    def increaseHP(self, plusHP):
        self.maxHP += plusHP
        self.healHP(plusHP*1.1)
        print("Vida máxima aumentada")
        time.sleep(1)
        return self.maxHP
    def decreaseHP(self, lossHP):
        self.maxHP -= lossHP
        self.takeDMG(lossHP)
        print("Vida máxima reduzida")
        time.sleep(1)
        return self.maxHP

    def useMind(self, insane, doPrint=True):
        if insane > self.mind:
            if doPrint:
                print("Seus poderes são fortes demais para a sua mente perturbada!")
                time.sleep(1)
            oldMind = self.mind
            self.mind = 0
            print(self.takeDMG(insane-oldMind))
            return insane, insane-oldMind
        self.mind -= insane
        if doPrint:
            print(f"{insane} de sanidade usada")
            time.sleep(1)
        return insane
    def restoreMind(self, sane, doPrint=True):
        overmind = 0
        oldMind = self.mind
        self.mind += sane
        if self.mind > self.maxMP:
            overmind = self.mind - self.maxMP
            self.mind = self.maxMP
        if doPrint:
            if oldMind == self.mind:
                print("Sanidade já está no máximo")
                time.sleep(1)
            else:
                print(f"Sanidade restaurada em {self.mind-oldMind}")
                time.sleep(1)
        return self.mind-oldMind, overmind
    def increaseMP(self, plusMP, doPrint=True):
        self.maxMP += plusMP
        self.restoreMind(plusMP)
        if doPrint:
            print("Sanidade aumentada")
        time.sleep(1)
        return self.maxMP
    def decreaseMP(self, lossMP):
        self.maxMP += lossMP
        self.useMind(lossMP)
        print("Sanidade reduzida")
        time.sleep(1)
        return self.maxMP

    def setAtkMod(self, dmgMod):
        self.modATK = dmgMod
        return f"Modificador de dano atualizado para {self.modATK}"
    def increaseAtkMod(self, dmgMod):
        self.modATK += dmgMod
        return f"Modificador de dano aumentado em {dmgMod} para {self.modATK}"
    def decreaseAtkMod(self, dmgMod):
        self.modATK -= dmgMod
        return f"Modificador de dano reduzido em {dmgMod} para {self.modATK}"
    def resetAtkMod(self):
        self.modATK = 0
        return "Modificador de dano zerado"
    
    def setDefMod(self, defMod):
        self.modDEF = defMod
        return f"Modificador de defesa atualizado para {self.modDEF}"
    def increaseDefMod(self, defMod):
        self.modDEF += defMod
        return f"Modificador de defesa aumentado em {defMod} para {self.modDEF}"
    def decreaseDefMod(self, defMod):
        self.modDEF -= defMod
        return f"Modificador de defesa reduzido em {defMod} para {self.modDEF}"
    def resetDefMod(self):
        self.modDEF = 0
        return "Modificador de defesa zerado"
    
    def resetMods(self):
        self.resetAtkMod()
        self.resetDefMod()
        return "Todos os modificadores zerados"

    def attackEnemy(self, enemy, doPrint=True):
        processedDamage = random.randint(self.baseATK, self.attack)+self.modATK
        if doPrint:
            print(f"{self._name} ataca {enemy._name} por {processedDamage} de dano")
        return enemy.takeDMG(processedDamage)

    def setGameStage(self,stage):
        self.gameStage = stage
        return self.gameStage