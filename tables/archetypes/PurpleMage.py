# Mind
import math, random, time
from tables.Character import Character
class PurpleMage(Character):
    def __init__(self,id,name,player,archetype="Mago Púrpura",maxHP=100,health=100,maxMP=125,mind=125,weapon=None,armor=None,baseATK=9,attack=9,modATK=0,baseDEF=0,defense=0,modDEF=0,gameStage=0):
        super().__init__(id,name,player,archetype,maxHP,health,maxMP,mind,weapon,armor,baseATK,attack,modATK,baseDEF,defense,modDEF,gameStage)

    def restoreMind(self, sane, doPrint=True):
        # O Mago Púrpura restaura 50% a mais de sanidade de qualquer fonte, arredondando para baixo
        sane = math.floor(sane * 1.5)
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
                print(f"Sanidade restaurada em {self.mind - oldMind}")
                time.sleep(1)
        if overmind > 0:
            # Sanidade sobressalente volta como cura
            _, overheal = self.healHP(overmind)
            if overheal > 0:
                # Cura sobressalente volta como dano bônus
                self.increaseAtkMod(overheal)
                # Organizado desse jeito para as mensagens aparecerem na ordem certa no terminal
        return sane, overmind
    def useMind(self, insane, doPrint=True):
        if insane > self.mind:
            if doPrint:
                print("Sem sanidade, o único combustível disponível para os Antigos é o sangue...")
                time.sleep(1)
            oldMind = self.mind
            self.mind = 0
            # O Mago Púrpura leva metade do dano quando usa vida para conjurar feitiços
            self.takeDMG(math.ceil((insane-oldMind)/2))
            return insane, insane-oldMind
        self.mind -= insane
        if doPrint:
            print(f"{insane} de sanidade usada")
            time.sleep(1)
        return insane
    def attackEnemy(self, enemy):
        processedDamage = random.randint(self.baseATK, self.attack)+self.modATK
        # O Mago Púrpura pode infundir magia em seus ataques
        while True:
            try:
                mindDamage = math.ceil(int(input(f"Quanta mente você vai usar nesse ataque? 1 mente = +2 de dano\nMente disponível: {self.mind}/{self.maxMP}\nMente usada: ")))
            except ValueError:
                print("Digite um número!")
                time.sleep(2)
                continue
            if mindDamage < 0:
                print("Não")
                time.sleep(1)
                continue
            if mindDamage > 0:
                self.useMind(mindDamage)
                processedDamage += mindDamage*2
            break
        print(f"{self._name} ataca {enemy._name} por {processedDamage} de dano")
        time.sleep(1)
        return enemy.takeDMG(processedDamage)