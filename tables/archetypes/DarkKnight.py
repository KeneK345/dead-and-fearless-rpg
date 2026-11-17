# Tank
import math,time
from tables.Character import Character
class DarkKnight(Character):
    def __init__(self,id,name,player,archetype="Cavaleiro Negro",maxHP=115,health=115,maxMP=100,mind=100,weapon=None,armor=None,baseATK=12,attack=12,modATK=0,baseDEF=1,defense=1,modDEF=0,gameStage=0):
        super().__init__(id,name,player,archetype,maxHP,health,maxMP,mind,weapon,armor,baseATK,attack,modATK,baseDEF,defense,modDEF,gameStage)

    def takeDMG(self, damage):
        # A armadura do Cavaleiro Negro é mais eficiente do que a dos outros
        processedDefense = self.defense + self.modDEF
        damageTaken = 0
        if damage > processedDefense:
            damageTaken = damage-math.ceil(processedDefense/3)
            self.health -= damageTaken
            # Ao receber muito dano, a armadura se adapta
            self.increaseDefMod(math.ceil(damageTaken/10))
        elif ((damage*4) - processedDefense) <= 0:
            print(f"{self.name} absorveu o ataque!")
            time.sleep(1)
            absorb = math.floor(processedDefense/4) - damage
            if absorb > 0:
                # Para cada quatro de defesa a mais que o dano "recebido", cura 1 de vida
                self.healHP(absorb)
            return ((damage*4)-processedDefense)
        else:
            damageTaken = damage - math.floor(processedDefense/4)
            self.health -= damageTaken
        rage = ""
        # Com dano o suficiente, o Cavaleiro Negro se enfurece
        # Ignora defesa, a não ser que ela abata completamente o dano
        if damage > 5:
            rage = "Seu sangue te guia!"
            # Restaura 1 de sanidade a cada 5 de dano que levar
            sane, overmind = self.restoreMind(math.floor(damage/5),False)
            if sane > 0:
                rage += f"\nMente restaurada em {sane}"
            # A sanidade sobressalente retorna em forma de vida, negando uma parte do dano
            heal, overheal = self.healHP(overmind,False)
            if heal > 0:
                rage += f"\n{heal} de dano negado"
            # Se por algum motivo existir cura sobressalente, ela retorna como ataque bônus
            if overheal > 0:
                self.increaseAtkMod(overheal)
                # ainda não sei se falo pro jogador sobre os modificadores :P
                # rage += f"\nAtaque aumenta em {overheal} para {self.modATK+self.attack} até o combate acabar"
        print(f"{self._name} levou {(damage - math.floor(processedDefense/4))} de dano")
        time.sleep(2)
        if len(rage) > 0:
            print(rage)
            time.sleep(2)
        return damageTaken