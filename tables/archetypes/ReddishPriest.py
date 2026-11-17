# Damage
import math,time,random
from tables.Character import Character
class ReddishPriest(Character):
    def __init__(self,id,name,player,archetype="Sacerdote Rubro",maxHP=100,health=100,maxMP=100,mind=100,weapon=None,armor=None,baseATK=14,attack=14,modATK=0,baseDEF=1,defense=1,modDEF=0,gameStage=0):
        super().__init__(id,name,player,archetype,maxHP,health,maxMP,mind,weapon,armor,baseATK,attack,modATK,baseDEF,defense,modDEF,gameStage)

    def takeDMG(self, damage):
        processedDefense = self.defense + self.modDEF
        damageTaken = 0
        # O Sacerdote Rubro usa a dor que sofre em batalha como combustível para sua força
        hate = 0
        if damage > processedDefense:
            damageTaken = damage-math.ceil(processedDefense/4)
            self.health -= damageTaken
            hate = math.ceil(damageTaken/2)
        elif ((damage*5) - processedDefense) <= 0:
            print(f"{self.name} absorveu o ataque!")
            time.sleep(1)
            return ((damage*5) - processedDefense)
        else:
            damageTaken = damage-math.floor(processedDefense/5)
            self.health -= damageTaken
            hate = math.floor(damageTaken/3)
        if hate > 0:
            # Se eu estiver correto, isso sempre vai ser maior do que o bônus do Cavaleiro Negro
            self.increaseAtkMod(hate)
        print(f"{self._name} levou {damageTaken} de dano")
        time.sleep(1)
        return damageTaken
    def attackEnemy(self, enemy, doPrint=True):
        # O Sacerdote Rubro bate mais forte quanto mais perto da morte estiver
        processedDamage = random.randint(self.baseATK, self.attack)+self.modATK+math.floor((self.maxHP-self.health)/10)
        if doPrint:
            print(f"{self._name} ataca {enemy._name} por {processedDamage} de dano")
        # Curiosamente, o dano que causa também volta como cura
        self.healHP(math.ceil(processedDamage/15),False)
        return enemy.takeDMG(processedDamage)