from tables.Character import Character
from tables.Item import Item
from treasure import weapons,armors
import administratum
from menus import signLoginLoop, combatLoop
import time, random, os, math

def setGame(gameStage):
    global currentCharacter, currentUser
    currentCharacter.setGameStage(gameStage)
    if currentUser:
        administratum.updateCrusader(administratum.sacredLink,currentCharacter.getCharUpdData())

def enchantItem(currentCharacter):
    print("Com um novo equipamento, você tem a chance de infundir uma parte de sua sanidade para melhorar sua performance")
    while True:
        try:
            enchant = int(input("Quanta mente você irá sacrificar? 3 mente = +1 dano/defesa\nSacrifício: "))
        except ValueError:
            print("Insira um número!")
            time.sleep(2)
            continue
        if enchant < 1:
            return 0
        currentCharacter.useMind(enchant)
        return math.floor(enchant/3)

login = True

print(f"{"Jogo de RPG Textual":-^50}\nUm jogo de RPG de fantasia genérico de qualidade duvidosa")
input("Aperte \"Enter\" para começar")
while True:
    if login:
        currentUser,currentCharacter = signLoginLoop()
        login = False
    match currentCharacter.gameStage:
        case 0:
            os.system("cls" if os.name == "nt" else "clear")
            print(f"{"A Aventura Começa":-^50}\nNuma vila qualquer, numa parte do mundo qualquer, {currentCharacter._name} cuida de seus afazeres do dia-a-dia.")
            time.sleep(3)
            match currentCharacter.archetype:
                case "Cavaleiro Negro":
                    print("As armas estão sendo polidas, os materiais de construção estão para ser levados para a obra, e ainda há muito a se ler à tarde.")
                case "Mago Púrpura":
                    print("O grande carvalho do centro comunitário precisa de cuidados, os quais somente alguém de mente forte pode oferecer.")
                case "Sacerdote Rubro":
                    print("As velas estão sendo acesas em preparação para a missa, e ninguém se voluntariou para carregar aquele tomo gigante ainda.")
            time.sleep(3)
            print(f"Tudo parece normal... até que uma comoção no cemitério chega à praça e pega a atenção do {currentCharacter.archetype}.")
            time.sleep(3)
            print("Ao sair para investigar, a comoção é clara: dois corpos mortos se levantaram de suas tumbas e estão atacando as pessoas!")
            time.sleep(3)
            print(f"Armado com nada além dos seus próprios punhos, {currentCharacter._name} parte pra cima dos mortos-vivos enquanto os aldeões chamam os guardas.")
            time.sleep(3)
            input(f"Aperte \"Enter\" para continuar")
            os.system("cls" if os.name == "nt" else "clear")
            enemy = Character(0,"Zumbi Decadente",-1,"Foe",31,random.randint(20,31),0,0,None,None,4,random.randint(5,8),0,0,0,0,0)
            enemies = [enemy]
            enemy = Character(0,"Zumbi Selvagem",-1,"Foe",25,25,0,0,None,None,5,random.randint(6,10),0,0,0,0,0)
            enemies.append(enemy)
            if combatLoop(currentCharacter,enemies):
                print("Congratulations! Você é incrível!")
            else:
                currentUser.defeat()
                input("Ferrou...")
                login = True
                continue
            setGame(10)
        case 10:
            os.system("cls" if os.name == "nt" else "clear")
            print("Os zumbis caem no chão, destruídos. Seus corpos podres fedem, mas pelo menos não estão mais se mexendo.")
            time.sleep(3)
            print(f"Quando a luta acaba, um dos jovens aldeões se aproxima de {currentCharacter._name} com uma caixa, puxando-a atrás dele com uma corda")
            time.sleep(3)
            print("Jovem aldeão: \"Com licença, com licença! Senhor, é... senhora... não importa! Tem um monte desses monstros vindo do leste!\"")
            time.sleep(3)
            print("Jovem aldeão: \"Os guardas da vila conseguiram lidar com o primeiro grupo deles, mas não sabemos se vão conseguir de novo.\"")
            time.sleep(3)
            print("Jovem aldeão: \"Eles me pediram pra te entregar isso, mas falaram pra eu não olhar dentro... e não olhei mesmo, juro!\"")
            time.sleep(3)
            print("Jovem aldeão: \"Aqui está, então... espero que te ajude.\"")
            input("Aperte \"Enter\" para continuar")
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print(f"O jovem puxa a caixa mais para perto e a deixa na frente de {currentCharacter._name}, destrancando o cadeado com uma pequena chave.")
                print("Que tipo de item irá te acompanhar a partir de agora?\n1 — Vestes reforçadas e uma arma básica, para o combatente defensivo\n2 — Uma arma mais avançada e especializada, para o combatente ofensivo")
                optWeapon = str(input("Sua escolha: "))
                os.system("cls" if os.name == "nt" else "clear")
                match currentCharacter.archetype:
                    case "Cavaleiro Negro":
                        match optWeapon:
                            case "1":
                                # Isso tudo poderia ser uma função... mas é tarde demais pra isso
                                newWeapon = weapons.dkStartWeapon(0)
                                newWeapon = Item(newWeapon[1],newWeapon[2],newWeapon[3],newWeapon[4])
                                print(newWeapon)
                                enchant = enchantItem(currentCharacter)
                                if currentUser:
                                    weapId = administratum.charObtainItem(administratum.sacredLink, (currentCharacter.id,*weapons.dkStartWeapon(enchant)))
                                    newWeapon.setId(weapId)
                                newWeapon.enchantAttack(enchant)
                                currentCharacter.obtainNewWeapon(newWeapon)
                                os.system("cls" if os.name == "nt" else "clear")
                                newArmor = armors.dkStartArmor(0)
                                newArmor = Item(newArmor[1],newArmor[2],newArmor[3],newArmor[4])
                                print(newArmor)
                                enchant = enchantItem(currentCharacter)
                                if currentUser:
                                    armId=administratum.charObtainItem(administratum.sacredLink, (currentCharacter.id,*armors.dkStartArmor(enchant)))
                                    newArmor.setId(armId)
                                newArmor.enchantDefense(enchant)
                                currentCharacter.obtainNewArmor(newArmor)
                            case "2":
                                newWeapon = weapons.dkBetterWeapon(0)
                                newWeapon = Item(newWeapon[1],newWeapon[2],newWeapon[3],newWeapon[4])
                                print(newWeapon)
                                enchant = enchantItem(currentCharacter)
                                if currentUser:
                                    weapId=administratum.charObtainItem(administratum.sacredLink, (currentCharacter.id,*weapons.dkBetterWeapon(enchant)))
                                    newWeapon.setId(weapId)
                                newWeapon.enchantAttack(enchant)
                                currentCharacter.obtainNewWeapon(newWeapon)
                            case _:
                                print("Insira um valor válido!")
                                time.sleep(2)
                                continue
                    case "Mago Púrpura":
                        match optWeapon:
                            case "1":
                                newWeapon = weapons.pmStartWeapon(0)
                                newWeapon = Item(newWeapon[1],newWeapon[2],newWeapon[3],newWeapon[4])
                                print(newWeapon)
                                enchant = enchantItem(currentCharacter)
                                if currentUser:
                                    weapId=administratum.charObtainItem(administratum.sacredLink, (currentCharacter.id,*weapons.pmStartWeapon(enchant)))
                                    newWeapon.setId(weapId)
                                newWeapon.enchantAttack(enchant)
                                currentCharacter.obtainNewWeapon(newWeapon)
                                os.system("cls" if os.name == "nt" else "clear")
                                newArmor = armors.pmStartArmor(0)
                                newArmor = Item(newArmor[1],newArmor[2],newArmor[3],newArmor[4])
                                print(newArmor)
                                enchant = enchantItem(currentCharacter)
                                if currentUser:
                                    armId=administratum.charObtainItem(administratum.sacredLink, (currentCharacter.id,*armors.pmStartArmor(enchant)))
                                    newArmor.setId(armId)
                                newArmor.enchantDefense(enchant)
                                currentCharacter.obtainNewArmor(newArmor)
                            case "2":
                                newWeapon = weapons.pmBetterWeapon(0)
                                newWeapon = Item(newWeapon[1],newWeapon[2],newWeapon[3],newWeapon[4])
                                print(newWeapon)
                                enchant = enchantItem(currentCharacter)
                                if currentUser:
                                    weapId=administratum.charObtainItem(administratum.sacredLink, (currentCharacter.id,*weapons.pmBetterWeapon(enchant)))
                                    newWeapon.setId(weapId)
                                newWeapon.enchantAttack(enchant)
                                currentCharacter.obtainNewWeapon(newWeapon)
                            case _:
                                print("Insira um valor válido!")
                                time.sleep(2)
                                continue
                    case "Sacerdote Rubro":
                        match optWeapon:
                            case "1":
                                newWeapon = weapons.rpStartWeapon(0)
                                newWeapon = Item(newWeapon[1],newWeapon[2],newWeapon[3],newWeapon[4])
                                print(newWeapon)
                                enchant = enchantItem(currentCharacter)
                                if currentUser:
                                    weapId=administratum.charObtainItem(administratum.sacredLink, (currentCharacter.id,*weapons.rpStartWeapon(enchant)))
                                    newWeapon.setId(weapId)
                                newWeapon.enchantAttack(enchant)
                                currentCharacter.obtainNewWeapon(newWeapon)
                                os.system("cls" if os.name == "nt" else "clear")
                                newArmor = armors.rpStartArmor(0)
                                newArmor = Item(newArmor[1],newArmor[2],newArmor[3],newArmor[4])
                                print(newArmor)
                                enchant = enchantItem(currentCharacter)
                                if currentUser:
                                    armId=administratum.charObtainItem(administratum.sacredLink, (currentCharacter.id,*armors.rpStartArmor(enchant)))
                                    newArmor.setId(armId)
                                newArmor.enchantDefense(enchant)
                                currentCharacter.obtainNewArmor(newArmor)
                            case "2":
                                newWeapon = weapons.rpBetterWeapon(0)
                                newWeapon = Item(newWeapon[1],newWeapon[2],newWeapon[3],newWeapon[4])
                                print(newWeapon)
                                enchant = enchantItem(currentCharacter)
                                if currentUser:
                                    weapId=administratum.charObtainItem(administratum.sacredLink, (currentCharacter.id,*weapons.rpBetterWeapon(enchant)))
                                    newWeapon.setId(weapId)
                                newWeapon.enchantAttack(enchant)
                                currentCharacter.obtainNewWeapon(newWeapon)
                            case _:
                                print("Insira um valor válido!")
                                time.sleep(2)
                                continue
                break
            os.system("cls" if os.name == "nt" else "clear")
            print(f"Enquanto {currentCharacter._name} estava inspecionando seu novo equipamento, o jovem ficou entediado e foi embora.")
            time.sleep(4)
            input("Aperte \"Enter\" para continuar")
            setGame(20)
        case 20:
            input("Esse é o fim da demo, não tem mais nada ):")
            login = True
        case 30:
            pass
# a surprise tool that will help us later
# administratum.updateCrusader(administratum.sacredLink,currentCharacter.getCharUpdData())
