# Dados base para construir todas as armas do jogo

def dkStartWeapon(enchant):
    name = "Lança curta com escudo"
    desc = "Uma lança curta com ponta de aço e um escudo de madeira redondo, feitos para a infantaria.\nNada mal, mas longe de ser o melhor."
    attack = 4+enchant
    defense = 4
    return ("Arma",name,desc,attack,defense)
def dkBetterWeapon(enchant):
    name="Espada de Cavaleiro"
    desc="Uma espada de dois gumes, punho cruciforme e curto (para usar com uma mão), com 70 centímetros de lâmina.\nUma arma clássica para qualquer herói arturiano."
    attack=8+enchant
    defense=2
    return ("Arma",name,desc,attack,defense)
def pmStartWeapon(enchant):
    name="Bastão de madeira"
    desc="Um cabo de vassoura? Uma lança sem ponta? O que quer que isso seja, não é muito bom como arma.\nPelo menos serve como catalisador de magia... e nada mal em aparar ataques!"
    attack=3+enchant
    defense=3
    return ("Arma",name,desc,attack,defense)
def pmBetterWeapon(enchant):
    name="Adaga Kris"
    desc="Uma kris (ou keris) é uma adaga cerimonial de lâmina ondada e base assimétrica.\nRelativamente frágil, essa adaga não deve ser usada para aparar ataques."
    attack=10+enchant
    defense=0
    return ("Arma",name,desc,attack,defense)
def rpStartWeapon(enchant):
    name="Cetro Cerimonial"
    desc="Um bastão de metal com um ícone na ponta: uma lua com dois olhos brilhantes, simbolizando o deus-lua Burdum.\nIsso NÃO É uma arma, mas para quem tem fé, tudo é possível."
    attack=4+enchant
    defense=1
    return ("Arma",name,desc,attack,defense)
def rpBetterWeapon(enchant):
    name="Porrete Natural"
    desc="Um graveto robusto com ponta mais grossa e coberta de espinhos.\nA fúria de Nazurah, manifestada num objeto brutal."
    attack=9+enchant
    defense=1
    return ("Arma",name,desc,attack,defense)