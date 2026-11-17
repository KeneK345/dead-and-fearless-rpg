import os, time, math
import administratum
from tables.User import User
from tables.archetypes.DarkKnight import DarkKnight
from tables.archetypes.ReddishPriest import ReddishPriest
from tables.archetypes.PurpleMage import PurpleMage
from tables.Item import Item
from tables.abilities.Guard import Guard

def signLoginLoop():
    currentCharacter = False
    while not currentCharacter:
        currentUser = loginMenu()
        currentCharacter = characterCreationMenu(currentUser)
    return currentUser, currentCharacter

def loginMenu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"{"Identificação de Usuário":-^50}\nSelecione uma das opções:\n0 — Fechar o jogo\n1 — Entrar com um usuário existente\n2 — Cadastrar-se como um novo usuário\n3 — Jogar como um convidado")
        try:
            loginOpt = int(input("Opção: "))
        except ValueError:
            print("Digite um número!")
            time.sleep(2)
            continue
        except:
            print("Algo deu extraordinariamente errado")
        match loginOpt:
            case 0:
                os.system("cls" if os.name == "nt" else "clear")
                print("Volte sempre! As masmorras estarão te esperando >:)")
                administratum.sacredLink.close()
                exit()
            case 1:
                cursor = administratum.sacredLink.cursor()
                while True:
                    cursor.execute('SELECT id,name,victories,defeats FROM user;')
                    users = cursor.fetchall()
                    if len(users) == 0:
                        os.system("cls" if os.name == "nt" else "clear")
                        print("Não existem usuários! Você é o primeiro a entrar no jogo! (Ou todos os outros eram convidados sem nome...)")
                        input("Aperte \"Enter\" para voltar")
                        break
                    max_width = max(len(uData[1]) for uData in users) + 5
                    os.system("cls" if os.name == "nt" else "clear")
                    print(f"{"Lista de usuários":-^50}")
                    print(f"{"identificador":<16}{"Nome":<{max_width}}{"Vitórias":<10}{"Derrotas":<5}")
                    for user in users:
                        print(f"{user[0]:^13}\t{user[1]:<{max_width+3}}{user[2]:<10}{user[3]}")
                    try:
                        idUser = int(input("\nSelecione um usuário pelo número identificador\nInsira 0 para voltar\nIdentificador: "))
                    except ValueError:
                        print("Digite um número!")
                        time.sleep(2)
                        os.system("cls" if os.name == "nt" else "clear")
                        continue
                    if idUser == 0:
                        break
                    foundUser = False
                    for user in users:
                        if user[0] == idUser:
                            os.system("cls" if os.name == "nt" else "clear")
                            while True:
                                print(f"Identificador inserido: {idUser}\nUsuário selecionado: {user[1]}\nVitórias: {user[2]}\nDerrotas: {user[3]}\nEsse é você? Insira 1 se sim")
                                try:
                                    isYou = int(input("Insira 0 para voltar\nSou eu: "))
                                except ValueError:
                                    print("Digite um número!")
                                    time.sleep(2)
                                    os.system("cls" if os.name == "nt" else "clear")
                                    continue
                                match isYou:
                                    case 0:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        break
                                    case 1:
                                        while True:
                                            os.system("cls" if os.name == "nt" else "clear")
                                            currentUser = User(user[0],user[1],user[2],user[3])
                                            print(f"Bem-vindo de volta às masmorras, {currentUser.name}!\n0 — Voltar à seleção de usuário\n1 — Continuar para a seleção de personagem\n2 — Mudar nome de usuário\n3 — Excluir usuário")
                                            try:
                                                userChoice = int(input("O que fazer: "))
                                            except ValueError:
                                                print("Insira um número!")
                                                time.sleep(2)
                                                continue
                                            match userChoice:
                                                case 0:
                                                    break
                                                case 1:
                                                    return currentUser
                                                case 2:
                                                    newName = str(input("Digite seu nome novo. Pode ser qualquer coisa, até mesmo seu nome antigo!\nInsira 0 para voltar\nNome: "))
                                                    if newName == "0":
                                                        continue
                                                    currentUser.changeName(newName)
                                                    print(administratum.updateUserData(administratum.sacredLink,currentUser.getUserUpdData()))
                                                    time.sleep(2)
                                                    break
                                                case 3:
                                                    try:
                                                        confirmDelete = int(input("Tem certeza que quer deletar esse usuário? Você nunca mais o verá!\n0 — Cancelar e poupar a vida desse cidadão\n1 — Deletar esse usuário\nEscolha: "))
                                                    except ValueError:
                                                        print("Digite um número!")
                                                        time.sleep(2)
                                                        continue
                                                    match confirmDelete:
                                                        case 0:
                                                            continue
                                                        case 1:
                                                            administratum.deleteUser(administratum.sacredLink,(currentUser.id,))
                                                            print("Usuário deletado. Eu já esqueci o nome dele... ou era dela? Não lembro :P")
                                                            input("Aperte \"Enter\" para voltar à tela de login")
                                                            break
                                                        case _:
                                                            print("Insira um valor válido!\nPelo seu erro, vou te mandar de volta como se tivesse apertado 0")
                                                            input("Aperte \"Enter\" para voltar")
                                        #input("Aperte \"Enter\" para continuar à seleção de personagem")
                                        #os.system("cls" if os.name == "nt" else "clear")
                                        #return currentUser
                                        break
                                    case _:
                                        print("Digite um valor válido (1 ou 0, cara...)")
                                        time.sleep(3)
                                        os.system("cls" if os.name == "nt" else "clear")
                            foundUser = True
                    if foundUser == False:
                        print("Usuário não encontrado! Verifique o identificador inserido e tente de novo. Ou volte para a tela anterior...")
                        input("Aperte \"Enter\" para continuar")
                        os.system("cls" if os.name == "nt" else "clear")
            case 2:
                os.system("cls" if os.name == "nt" else "clear")
                userName = str(input(f"{"Criando um novo usuário!":-^50}\nInsira seu nome de usuário. Pode ser qualquer coisa, sem restrições! A não ser, claro, sua consciência...\nInsira 0 para voltar\nNome de usuário: "))
                if userName == "0":
                    continue
                userId = administratum.signUp(administratum.sacredLink,(userName,))
                currentUser = User(userId,userName)
                print(f"Usuário cadastrado. Divirta-se lá embaixo, {userName}!")
                return currentUser
            case 3:
                os.system("cls" if os.name == "nt" else "clear")
                try:
                    mayGuest = int(input("Tem certeza que quer entrar como convidado? Seus dados não serão salvos!\nInsira 1 para entrar como convidado (e renunciar seus direitos a estadia permanente)\nInsira 0 para voltar\nVou ser convidado: "))
                except ValueError:
                    print("Digite um valor válido (1 ou 0, cara...)")
                    time.sleep(3)
                    print("Vou te mandar de volta como se tivesse inserido 0")
                    input("Aperte \"Enter\" para voltar")
                    mayGuest = 0
                match mayGuest:
                    case 0:
                        pass
                    case 1:
                        print("Ok, então... bem-vindo, convidado sem nome. Não iremos nos lembrar de você quando se for.")
                        input("Aperte \"Enter\" para continuar")
                        return False
                    case _:
                        print("Digite um valor válido (1 ou 0, cara...)")
                        time.sleep(3)
                        print("Vou te mandar de volta como se tivesse inserido 0")
                        input("Aperte \"Enter\" para voltar")
            case _:
                print("Digite um valor válido!")
                time.sleep(2)

def characterCreationMenu(currentUser):
    if not currentUser:
        while True:
            try:
                os.system("cls" if os.name == "nt" else "clear")
                print(f"{"Um cruzado para o convidado":-^50}\nComo você entrou como convidado, não vai poder dar um nome ao seu cruzado. Ao invés disso, ele só vai ser chamado de \"Condenado\"")
                print(f"{"|Arquétipo de cruzado|":-^50}\nNa luta contra os mortos, as forças tradicionais não são o suficiente para enfrentar as hordas.\nÉ aqui que entram os talentos mais excepcionais e inortodoxos encontrados.\nDas mais poderosas das casas nobres até as mais humildes das vilas, existem alguns indivíduos extremamente distinguidos.\nPara lidar com a invasão de mortos-vivos, três arquétipos nos interessam:")
                charArch = int(input("\n1 — Cavaleiro Negro, o baluarte, uma montanha estoica contra o mar da corrupção;\n2 — Mago Púrpura, o ocultista, um canal entre o mundo terreno e as forças que o conduzem;\n3 — Sacerdote Rubro, o sanguinário, um arauto dos deuses antigos que regem sobre nós e nos amam tanto quanto nós os tememos.\nInsira 0 para voltar\nArquétipo de cruzado: "))
            except ValueError:
                print("Digite um número!")
                time.sleep(2)
                continue
            except:
                print("Algo deu extraordinariamente errado")
            charName = "Condenado"
            match charArch:
                case 0:
                    return False
                case 1:
                    while True:
                        os.system("cls" if os.name == "nt" else "clear")
                        print(f"{"Cavaleiro Negro":-^50}\nAo longo de toda a história, lutadores e soldados convencionais sempre vestiram roupas e armaduras de cores claras.\nElas tendem a refletir melhor as magias usadas por seus inimigos, e não absorvem tanto quanto cores mais escuras.\nExistem alguns guerreiros que decidem abraçar as forças mágicas ao invés de evitá-las e usar a dor que sofrem a seu favor.\nChamamos esses guerreiros de Cavaleiros Negros, que usam armaduras pesadas e tintas escuras para absorver feitiços,\nconvertendo até o seu próprio sangue derramado em um catalisador para os deuses antigos.")
                        try:
                            archChoice = int(input(f"\nÉ esse o dom que {charName} tem? Enfrentar qualquer tempestade, não importa o quão brutal, sem se abater?\n\nInsira 1 para confirmar\nInsira 0 para voltar\nÉ isso que concedo a este cruzado: "))
                        except ValueError:
                            print("Digite um número!")
                            time.sleep(2)
                            continue
                        except:
                            print("Algo deu extraordinariamente errado")
                        match archChoice:
                            case 0:
                                break
                            case 1:
                                os.system("cls" if os.name == "nt" else "clear")
                                currentCharacter = DarkKnight(0,charName,0)
                                currentCharacter.weapon = Item("Punhos","Falcon PAWNCH!",0,0)
                                currentCharacter.armor = Item("Corpão Sarado","Ganhe no argumento como Platão",0,0)
                                currentCharacter.abilities.append(Guard())
                                print(f"Cruzado criado. Nem se importe em desejar sorte, o futuro desse aqui já está pré-determinado.")
                                input("Aperte \"Enter\" para continuar")
                                return currentCharacter
                            case _:
                                print("Digite um valor válido (1 ou 2, cara...)")
                                time.sleep(3)
                case 2:
                    while True:
                        os.system("cls" if os.name == "nt" else "clear")
                        print(f"{"Mago Púrpura":-^50}\nQuando o mundo foi criado, os deuses antigos — Deusa-Sol Aurette, Deus-Lua Burdum, e sua divina prole — deixaram rastros de\nmagia por toda parte. Cada entidade divina deixou um rastro diferente, fazendo o mundo do jeito que é agora.\nCom tantos poderes arcanos a estudar e mistérios divinos a desvendar, muitos magos decidem focar em apenas um rastro arcano.\nExistem magos que, dotados de curiosidade voraz, se dedicam a muitos rastros e expandem seu conhecimento agressivamente.\nChamamos esses indivíduos de Magos Púrpura, que têm suas roupas tingidas em consequência das várias magias que estudam.\nMuitos também ficam insanos, mas isso é só um detalhe. Nada que vá te impedir...")
                        try:
                            archChoice = int(input(f"\nÉ esse o dom que {charName} tem? Canalizar as várias magias dos antigos sem deixar a insanidade tomar conta?\n\nInsira 1 para confirmar\nInsira 0 para voltar\nÉ isso que concedo a este cruzado: "))
                        except ValueError:
                            print("Digite um número!")
                            time.sleep(2)
                            continue
                        except:
                            print("Algo deu extraordinariamente errado")
                        match archChoice:
                            case 0:
                                break
                            case 1:
                                os.system("cls" if os.name == "nt" else "clear")
                                currentCharacter = PurpleMage(0,charName,0)
                                currentCharacter.weapon = Item("Punhos","Falcon PAWNCH!",0,0)
                                currentCharacter.armor = Item("Corpão Sarado","Ganhe no argumento como Platão",0,0)
                                currentCharacter.abilities.append(Guard())
                                print(f"Cruzado criado. Nem se importe em desejar sorte, o futuro desse aqui já está pré-determinado.")
                                input("Aperte \"Enter\" para continuar")
                                return currentCharacter
                            case _:
                                print("Digite um valor válido (1 ou 2, cara...)")
                                time.sleep(3)
                case 3:
                    while True:
                        os.system("cls" if os.name == "nt" else "clear")
                        print(f"{"Sacerdote Rubro":-^50}\nOs deuses sempre foram uma fonte de medo e poder em todas as sociedades terrenas, e por bom motivo.\nSegredos que nunca serão revelados, mistérios que nunca serão resolvidos... a incerteza é desesperadora.\nMas não para o sacerdote.\nAlguns estudiosos da fé não só tentam desvendar esses mistérios, mas aceitam o desconhecido de braços abertos.\nChamamos esses estudiosos de Sacerdotes Rubros, que vestem roupas vermelhas para esconder as feridas ritualísticas.\nEm tempos de paz, eles pregam os ensinamentos que extraíram dos deuses e performam milagres com seu próprio sangue.\nEm tempos de guerra, eles usam esses mesmos ensinamentos para subjugar o inimigo, trazendo consigo a fúria dos divinos.")
                        try:
                            archChoice = int(input(f"\nÉ esse o dom que {charName} tem? Transformar a dor em fúria, e a fúria em força?\n\nInsira 1 para confirmar\nInsira 0 para voltar\nÉ isso que concedo a este cruzado: "))
                        except ValueError:
                            print("Digite um número!")
                            time.sleep(2)
                            continue
                        except:
                            print("Algo deu extraordinariamente errado")
                        match archChoice:
                            case 0:
                                break
                            case 1:
                                os.system("cls" if os.name == "nt" else "clear")
                                currentCharacter = ReddishPriest(0,charName,0)
                                currentCharacter.weapon = Item("Punhos","Falcon PAWNCH!",0,0)
                                currentCharacter.armor = Item("Corpão Sarado","Ganhe no argumento como Platão",0,0)
                                currentCharacter.abilities.append(Guard())
                                print(f"Cruzado criado. Nem se importe em desejar sorte, o futuro desse aqui já está pré-determinado.")
                                input("Aperte \"Enter\" para continuar")
                                return currentCharacter
                            case _:
                                print("Digite um valor válido (1 ou 2, cara...)")
                                time.sleep(3)
                case _:
                    print("Digite um valor válido!")
                    time.sleep(2)
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"{"Seleção de Cruzado":-^50}\nSelecione uma das opções:\n0 — Voltar ao login de usuário\n1 — Selecionar um cruzado\n2 — Criar novo cruzado\n3 — Criar cruzado condenado (não é salvo no computador)")
        try:
            charOpt = int(input("Opção: "))
        except:
            print("Digite um número!")
            time.sleep(2)
            continue
        match charOpt:
            case 0:
                return False
            case 1:
                os.system("cls" if os.name == "nt" else "clear")
                chars = administratum.getAllCrusaders(administratum.sacredLink,(currentUser.id,))
                if len(chars) == 0:
                    print(f"Você não tem nenhum cruzado, {currentUser.name}. Crie um.")
                    input("Aperte \"Enter\" para voltar")
                    continue
                max_width = max(len(cData[1]) for cData in chars) + 5
                while True:
                    print(f"{"Lista de cruzados":-^50}")
                    print(f"{"identificador":<16}{"Nome":<{max_width}}{"Arquétipo":<10}")
                    for char in chars:
                        print(f"{char[0]:^13}\t{char[1]:<{max_width}}{char[2]:<10}")
                    try:
                        idChar = int(input("\nSelecione um cruzado pelo número identificador\nInsira 0 para voltar\nIdentificador: "))
                    except ValueError:
                        print("Digite um número!")
                        time.sleep(2)
                        os.system("cls" if os.name == "nt" else "clear")
                        continue
                    if idChar == 0:
                        break
                    foundChar = False
                    for char in chars:
                        if char[0] == idChar:
                            os.system("cls" if os.name == "nt" else "clear")
                            while True:
                                print(f"Identificador inserido: {idChar}\nCruzado selecionado: {char[1]}, {char[2]}\nÉ esse que você quer? Insira 1 se sim")
                                try:
                                    isChar = int(input("Insira 0 para voltar\nEu quero: "))
                                except ValueError:
                                    print("Digite um número!")
                                    time.sleep(2)
                                    os.system("cls" if os.name == "nt" else "clear")
                                    continue
                                match isChar:
                                    case 0:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        break
                                    case 1:
                                        currentCharacter = administratum.getCrusaderStats(administratum.sacredLink,(idChar,))
                                        currentCharacter = currentCharacter[0]
                                        archetype = currentCharacter[3]
                                        match archetype:
                                            case "Cavaleiro Negro":
                                                currentCharacter = DarkKnight(currentCharacter[0],currentCharacter[1],currentCharacter[2],currentCharacter[3],currentCharacter[4],currentCharacter[5],currentCharacter[6],currentCharacter[7],None,None,currentCharacter[8],currentCharacter[9],currentCharacter[10],currentCharacter[11],currentCharacter[12],currentCharacter[13],[],currentCharacter[14])
                                            case "Mago Púrpura":
                                                currentCharacter = PurpleMage(currentCharacter[0],currentCharacter[1],currentCharacter[2],currentCharacter[3],currentCharacter[4],currentCharacter[5],currentCharacter[6],currentCharacter[7],None,None,currentCharacter[8],currentCharacter[9],currentCharacter[10],currentCharacter[11],currentCharacter[12],currentCharacter[13],[],currentCharacter[14])
                                            case "Sacerdote Rubro":
                                                currentCharacter = ReddishPriest(currentCharacter[0],currentCharacter[1],currentCharacter[2],currentCharacter[3],currentCharacter[4],currentCharacter[5],currentCharacter[6],currentCharacter[7],None,None,currentCharacter[8],currentCharacter[9],currentCharacter[10],currentCharacter[11],currentCharacter[12],currentCharacter[13],[],currentCharacter[14])
                                        charWeapon = administratum.getCharWeapon(administratum.sacredLink,(currentCharacter.id,))
                                        if len(charWeapon) > 0:
                                            charWeapon = charWeapon[0]
                                            currentCharacter.weapon = Item(charWeapon[3],charWeapon[4],charWeapon[5],charWeapon[6])
                                        else:
                                            currentCharacter.weapon = Item("Punhos","Falcon PAWNCH!",0,0)
                                        charArmor = administratum.getCharArmor(administratum.sacredLink,(currentCharacter.id,))
                                        if len(charArmor) > 0:
                                            charArmor = charArmor[0]
                                            currentCharacter.armor = Item(charWeapon[3],charWeapon[4],charWeapon[5],charWeapon[6])
                                        else:
                                            currentCharacter.armor = Item("Corpão Sarado","Ganhe no argumento como Platão",0,0)
                                        charAbilities = administratum.getCharAbilities((currentCharacter.id,))
                                        for ability in charAbilities:
                                            # Pega a classe da abilidade com o nome. Direto do Stack Overflow >:D
                                            ability = globals()[ability[4]]
                                            currentCharacter.abilities.append(ability)
                                        os.system("cls" if os.name == "nt" else "clear")
                                        print(currentCharacter.abilities[0])
                                        return currentCharacter
                                    case _:
                                        print("Digite um valor válido (1 ou 0, cara...)")
                                        time.sleep(3)
                                        os.system("cls" if os.name == "nt" else "clear")
                            foundChar = True
                    if foundChar == False:
                        print("Cruzado não encontrado! Verifique o identificador inserido e tente de novo. Talvez ele tenha morrido... Ou volte para a tela anterior...")
                        input("Aperte \"Enter\" para continuar")
                        os.system("cls" if os.name == "nt" else "clear")
            case 2:
                os.system("cls" if os.name == "nt" else "clear")
                charName = str(input(f"{"|Mais um corpo para a luta|":-^50}\nSe você nasceu, você pelo menos tem um nome. Diga-me o seu.\nInsira 0 para voltar\nNome do cruzado: "))
                os.system("cls" if os.name == "nt" else "clear")
                if charName == "0":
                    continue
                print(f"Um nome interessante. {charName}...")
                time.sleep(3)
                while True:
                    try:
                        os.system("cls" if os.name == "nt" else "clear")
                        print(f"{"|Arquétipo de cruzado|":-^50}\nNa luta contra os mortos, as forças tradicionais não são o suficiente para enfrentar as hordas.\nÉ aqui que entram os talentos mais excepcionais e inortodoxos encontrados.\nDas mais poderosas das casas nobres até as mais humildes das vilas, existem alguns indivíduos extremamente distinguidos.\nPara lidar com a invasão de mortos-vivos, três arquétipos nos interessam:")
                        charArch = int(input("\n1 — Cavaleiro Negro, o baluarte, uma montanha estoica contra o mar da corrupção;\n2 — Mago Púrpura, o ocultista, um canal entre o mundo terreno e as forças que o conduzem;\n3 — Sacerdote Rubro, o sanguinário, um arauto dos deuses antigos que regem sobre nós e nos amam tanto quanto nós os tememos.\nInsira 0 para voltar\nArquétipo de cruzado: "))
                    except ValueError:
                        print("Digite um número!")
                        time.sleep(2)
                        continue
                    except:
                        print("Algo deu extraordinariamente errado")
                    match charArch:
                        case 0:
                            break
                        case 1:
                            while True:
                                os.system("cls" if os.name == "nt" else "clear")
                                print(f"{"Cavaleiro Negro":-^50}\nAo longo de toda a história, lutadores e soldados convencionais sempre vestiram roupas e armaduras de cores claras.\nElas tendem a refletir melhor as magias usadas por seus inimigos, e não absorvem tanto quanto cores mais escuras.\nExistem alguns guerreiros que decidem abraçar as forças mágicas ao invés de evitá-las e usar a dor que sofrem a seu favor.\nChamamos esses guerreiros de Cavaleiros Negros, que usam armaduras pesadas e tintas escuras para absorver feitiços,\nconvertendo até o seu próprio sangue derramado em um catalisador para os deuses antigos.")
                                try:
                                    archChoice = int(input(f"\nÉ esse o dom que {charName} tem? Enfrentar qualquer tempestade, não importa o quão brutal, sem se abater?\n\nInsira 1 para confirmar\nInsira 0 para voltar\nÉ isso que concedo a este cruzado: "))
                                except ValueError:
                                    print("Digite um número!")
                                    time.sleep(2)
                                    continue
                                except:
                                    print("Algo deu extraordinariamente errado")
                                match archChoice:
                                    case 0:
                                        break
                                    case 1:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        charId = administratum.newCrusader(administratum.sacredLink,(charName,currentUser.id,"Cavaleiro Negro",115,115,100,100,12,12,0,1,1,0,0))
                                        currentCharacter = DarkKnight(charId,charName,currentUser.id)
                                        currentCharacter.weapon = Item("Punhos","Falcon PAWNCH!",0,0)
                                        currentCharacter.armor = Item("Corpão Sarado","Ganhe no argumento como Platão",0,0)
                                        dkAbilities = Guard()
                                        idAbility = administratum.newAbility((charId,dkAbilities.name,dkAbilities.desc,dkAbilities.__class__.__name__))
                                        dkAbilities.setId(idAbility)
                                        dkAbilities.setCharId(charId)
                                        print(f"Cruzado criado. Deseje-nos sorte, {charName} vai precisar...\n'A árvore antiga — muitos ventos a curvaram — e aprofundaram ainda mais suas raízes'\n— Desconhecido")
                                        input("Aperte \"Enter\" para continuar")
                                        return currentCharacter
                                    case _:
                                        print("Digite um valor válido (1 ou 2, cara...)")
                                        time.sleep(3)
                        case 2:
                            while True:
                                os.system("cls" if os.name == "nt" else "clear")
                                print(f"{"Mago Púrpura":-^50}\nQuando o mundo foi criado, os deuses antigos — Deusa-Sol Aurette, Deus-Lua Burdum, e sua divina prole — deixaram rastros de\nmagia por toda parte. Cada entidade divina deixou um rastro diferente, fazendo o mundo do jeito que é agora.\nCom tantos poderes arcanos a estudar e mistérios divinos a desvendar, muitos magos decidem focar em apenas um rastro arcano.\nExistem magos que, dotados de curiosidade voraz, se dedicam a muitos rastros e expandem seu conhecimento agressivamente.\nChamamos esses indivíduos de Magos Púrpura, que têm suas roupas tingidas em consequência das várias magias que estudam.\nMuitos também ficam insanos, mas isso é só um detalhe. Nada que vá te impedir...")
                                try:
                                    archChoice = int(input(f"\nÉ esse o dom que {charName} tem? Canalizar as várias magias dos antigos sem deixar a insanidade tomar conta?\n\nInsira 1 para confirmar\nInsira 0 para voltar\nÉ isso que concedo a este cruzado: "))
                                except ValueError:
                                    print("Digite um número!")
                                    time.sleep(2)
                                    continue
                                except:
                                    print("Algo deu extraordinariamente errado")
                                match archChoice:
                                    case 0:
                                        break
                                    case 1:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        charId = administratum.newCrusader(administratum.sacredLink, (charName,currentUser.id,"Mago Púrpura",100,100,125,125,9,9,0,0,0,0,0))
                                        currentCharacter = PurpleMage(charId,charName,currentUser.id)
                                        currentCharacter.weapon = Item("Punhos","Falcon PAWNCH!",0,0)
                                        currentCharacter.armor = Item("Corpão Sarado","Ganhe no argumento como Platão",0,0)
                                        pmAbilities = Guard()
                                        idAbility = administratum.newAbility((charId,pmAbilities.name,pmAbilities.desc,pmAbilities.__class__.__name__))
                                        pmAbilities.setId(idAbility)
                                        pmAbilities.setCharId(charId)
                                        print(f"Cruzado criado. Deseje-nos sorte, {charName} vai precisar...\n'Achei que viveria até os 200, talvez 300 anos. Mas cá estou eu, uma jovem criança nos seus meros 100 anos...'\n— Desconhecido")
                                        input("Aperte \"Enter\" para continuar")
                                        return currentCharacter
                                    case _:
                                        print("Digite um valor válido (1 ou 2, cara...)")
                                        time.sleep(3)
                        case 3:
                            while True:
                                os.system("cls" if os.name == "nt" else "clear")
                                print(f"{"Sacerdote Rubro":-^50}\nOs deuses sempre foram uma fonte de medo e poder em todas as sociedades terrenas, e por bom motivo.\nSegredos que nunca serão revelados, mistérios que nunca serão resolvidos... a incerteza é desesperadora.\nMas não para o sacerdote.\nAlguns estudiosos da fé não só tentam desvendar esses mistérios, mas aceitam o desconhecido de braços abertos.\nChamamos esses estudiosos de Sacerdotes Rubros, que vestem roupas vermelhas para esconder as feridas ritualísticas.\nEm tempos de paz, eles pregam os ensinamentos que extraíram dos deuses e performam milagres com seu próprio sangue.\nEm tempos de guerra, eles usam esses mesmos ensinamentos para subjugar o inimigo, trazendo consigo a fúria dos divinos.")
                                try:
                                    archChoice = int(input(f"\nÉ esse o dom que {charName} tem? Transformar a dor em fúria, e a fúria em força?\n\nInsira 1 para confirmar\nInsira 0 para voltar\nÉ isso que concedo a este cruzado: "))
                                except ValueError:
                                    print("Digite um número!")
                                    time.sleep(2)
                                    continue
                                except:
                                    print("Algo deu extraordinariamente errado")
                                match archChoice:
                                    case 0:
                                        break
                                    case 1:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        charId = administratum.newCrusader(administratum.sacredLink, (charName,currentUser.id,"Sacerdote Rubro",100,100,100,100,14,14,0,1,1,0,0))
                                        currentCharacter = ReddishPriest(charId,charName,currentUser.id)
                                        currentCharacter.weapon = Item("Punhos","Falcon PAWNCH!",0,0)
                                        currentCharacter.armor = Item("Corpão Sarado","Ganhe no argumento como Platão",0,0)
                                        rpAbilities = Guard()
                                        idAbility = administratum.newAbility((charId,rpAbilities.name,rpAbilities.desc,rpAbilities.__class__.__name__))
                                        rpAbilities.setId(idAbility)
                                        rpAbilities.setCharId(charId)
                                        print(f"Cruzado criado. Deseje-nos sorte, {charName} vai precisar...\n'O que entende-se como \"vazio\" é isto: onde as coisas não estão, e o que não pode ser conhecido, é dito como vazio.\nVazio, é claro, é o que não está ali. Sabendo o que está ali, sabe-se o que não está, e isso é o vazio.'\n— Myamoto Musashi, O Livro dos Cinco Anéis")
                                        input("Aperte \"Enter\" para continuar")
                                        return currentCharacter
                                    case _:
                                        print("Digite um valor válido (1 ou 2, cara...)")
                                        time.sleep(3)
                        case _:
                            print("Digite um valor válido!")
                            time.sleep(2)
            case 3:
                while True:
                    try:
                        os.system("cls" if os.name == "nt" else "clear")
                        print(f"{"|Arquétipo de cruzado|":-^50}\nNa luta contra os mortos, as forças tradicionais não são o suficiente para enfrentar as hordas.\nÉ aqui que entram os talentos mais excepcionais e inortodoxos encontrados.\nDas mais poderosas das casas nobres até as mais humildes das vilas, existem alguns indivíduos extremamente distinguidos.\nPara lidar com a invasão de mortos-vivos, três arquétipos nos interessam:")
                        charArch = int(input("\n1 — Cavaleiro Negro, o baluarte, uma montanha estoica contra o mar da corrupção;\n2 — Mago Púrpura, o ocultista, um canal entre o mundo terreno e as forças que o conduzem;\n3 — Sacerdote Rubro, o sanguinário, um arauto dos deuses antigos que regem sobre nós e nos amam tanto quanto nós os tememos.\nInsira 0 para voltar\nArquétipo de cruzado: "))
                    except ValueError:
                        print("Digite um número!")
                        time.sleep(2)
                        continue
                    except:
                        print("Algo deu extraordinariamente errado")
                    charName = "Condenado"
                    match charArch:
                        case 0:
                            break
                        case 1:
                            while True:
                                os.system("cls" if os.name == "nt" else "clear")
                                print(f"{"Cavaleiro Negro":-^50}\nAo longo de toda a história, lutadores e soldados convencionais sempre vestiram roupas e armaduras de cores claras.\nElas tendem a refletir melhor as magias usadas por seus inimigos, e não absorvem tanto quanto cores mais escuras.\nExistem alguns guerreiros que decidem abraçar as forças mágicas ao invés de evitá-las e usar a dor que sofrem a seu favor.\nChamamos esses guerreiros de Cavaleiros Negros, que usam armaduras pesadas e tintas escuras para absorver feitiços,\nconvertendo até o seu próprio sangue derramado em um catalisador para os deuses antigos.")
                                try:
                                    archChoice = int(input(f"\nÉ esse o dom que {charName} tem? Enfrentar qualquer tempestade, não importa o quão brutal, sem se abater?\n\nInsira 1 para confirmar\nInsira 0 para voltar\nÉ isso que concedo a este cruzado: "))
                                except ValueError:
                                    print("Digite um número!")
                                    time.sleep(2)
                                    continue
                                except:
                                    print("Algo deu extraordinariamente errado")
                                match archChoice:
                                    case 0:
                                        break
                                    case 1:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        currentCharacter = DarkKnight(0,charName,currentUser.id)
                                        currentCharacter.weapon = Item("Punhos","Falcon PAWNCH!",0,0)
                                        currentCharacter.armor = Item("Corpão Sarado","Ganhe no argumento como Platão",0,0)
                                        currentCharacter.abilities.append(Guard())
                                        print(f"Cruzado criado. Nem se importe em desejar sorte, o futuro desse aqui já está pré-determinado.")
                                        input("Aperte \"Enter\" para continuar")
                                        return currentCharacter
                                    case _:
                                        print("Digite um valor válido (1 ou 2, cara...)")
                                        time.sleep(3)
                        case 2:
                            while True:
                                os.system("cls" if os.name == "nt" else "clear")
                                print(f"{"Mago Púrpura":-^50}\nQuando o mundo foi criado, os deuses antigos — Deusa-Sol Aurette, Deus-Lua Burdum, e sua divina prole — deixaram rastros de\nmagia por toda parte. Cada entidade divina deixou um rastro diferente, fazendo o mundo do jeito que é agora.\nCom tantos poderes arcanos a estudar e mistérios divinos a desvendar, muitos magos decidem focar em apenas um rastro arcano.\nExistem magos que, dotados de curiosidade voraz, se dedicam a muitos rastros e expandem seu conhecimento agressivamente.\nChamamos esses indivíduos de Magos Púrpura, que têm suas roupas tingidas em consequência das várias magias que estudam.\nMuitos também ficam insanos, mas isso é só um detalhe. Nada que vá te impedir...")
                                try:
                                    archChoice = int(input(f"\nÉ esse o dom que {charName} tem? Canalizar as várias magias dos antigos sem deixar a insanidade tomar conta?\n\nInsira 1 para confirmar\nInsira 0 para voltar\nÉ isso que concedo a este cruzado: "))
                                except ValueError:
                                    print("Digite um número!")
                                    time.sleep(2)
                                    continue
                                except:
                                    print("Algo deu extraordinariamente errado")
                                match archChoice:
                                    case 0:
                                        break
                                    case 1:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        currentCharacter = PurpleMage(0,charName,currentUser.id)
                                        currentCharacter.weapon = Item("Punhos","Falcon PAWNCH!",0,0)
                                        currentCharacter.armor = Item("Corpão Sarado","Ganhe no argumento como Platão",0,0)
                                        currentCharacter.abilities.append(Guard())
                                        print(f"Cruzado criado. Nem se importe em desejar sorte, o futuro desse aqui já está pré-determinado.")
                                        input("Aperte \"Enter\" para continuar")
                                        return currentCharacter
                                    case _:
                                        print("Digite um valor válido (1 ou 2, cara...)")
                                        time.sleep(3)
                        case 3:
                            while True:
                                os.system("cls" if os.name == "nt" else "clear")
                                print(f"{"Sacerdote Rubro":-^50}\nOs deuses sempre foram uma fonte de medo e poder em todas as sociedades terrenas, e por bom motivo.\nSegredos que nunca serão revelados, mistérios que nunca serão resolvidos... a incerteza é desesperadora.\nMas não para o sacerdote.\nAlguns estudiosos da fé não só tentam desvendar esses mistérios, mas aceitam o desconhecido de braços abertos.\nChamamos esses estudiosos de Sacerdotes Rubros, que vestem roupas vermelhas para esconder as feridas ritualísticas.\nEm tempos de paz, eles pregam os ensinamentos que extraíram dos deuses e performam milagres com seu próprio sangue.\nEm tempos de guerra, eles usam esses mesmos ensinamentos para subjugar o inimigo, trazendo consigo a fúria dos divinos.")
                                try:
                                    archChoice = int(input(f"\nÉ esse o dom que {charName} tem? Transformar a dor em fúria, e a fúria em força?\n\nInsira 1 para confirmar\nInsira 0 para voltar\nÉ isso que concedo a este cruzado: "))
                                except ValueError:
                                    print("Digite um número!")
                                    time.sleep(2)
                                    continue
                                except:
                                    print("Algo deu extraordinariamente errado")
                                match archChoice:
                                    case 0:
                                        break
                                    case 1:
                                        os.system("cls" if os.name == "nt" else "clear")
                                        currentCharacter = ReddishPriest(0,charName,currentUser.id)
                                        currentCharacter.weapon = Item("Punhos","Falcon PAWNCH!",0,0)
                                        currentCharacter.armor = Item("Corpão Sarado","Ganhe no argumento como Platão",0,0)
                                        currentCharacter.abilities.append(Guard())
                                        print(f"Cruzado criado. Nem se importe em desejar sorte, o futuro desse aqui já está pré-determinado.")
                                        input("Aperte \"Enter\" para continuar")
                                        return currentCharacter
                                    case _:
                                        print("Digite um valor válido (1 ou 2, cara...)")
                                        time.sleep(3)
                        case _:
                            print("Digite um valor válido!")
                            time.sleep(2)
            case _:
                print("Digite um valor válido!")
                time.sleep(2)

def combatLoop(currentCharacter,enemies):
    while True:
        while True:
            print(f"{"Em Combate":-^50}\nInimigos no campo:")
            for i in enemies:
                print(i.basicInfo())
            print("\nVocê:\n",currentCharacter)
            print(f"{"Ações":-^50}\n0 — Passar o turno\n1 — Atacar um inimigo\n2 — Meditar e restaurar mente\n3 — Mutilar-se por nenhum motivo")
            try:
                action = int(input("O que vai fazer: "))
                print("\n")
            except ValueError:
                print("Digite um número!")
                time.sleep(2)
                continue
            match action:
                case 0:
                    print(f"{currentCharacter._name} aguarda uma próxima oportunidade.")
                    currentCharacter.healHP(2)
                    currentCharacter.restoreMind(2)
                    break
                case 1:
                    back = False
                    print("Selecione um inimigo para atacar:")
                    for i in enemies:
                        print(f"{enemies.index(i)+1} — {i.basicInfo()}")
                    while True:
                        try:
                            victim = int(input("\nInsira 0 para voltar\nSua vítima: "))
                        except ValueError:
                            print("Digite um número!")
                            time.sleep(2)
                            continue
                        if victim == 0:
                            back = True
                            break
                        try:
                            currentCharacter.attackEnemy(enemies[victim-1])
                            break
                        except IndexError:
                            print("Inimigo não encontrado. Insira um número válido")
                            time.sleep(3)
                            continue
                    if back:
                        continue
                    break
                case 2:
                    currentCharacter.restoreMind(math.floor(currentCharacter.maxMP/5))
                    break
                case 3:
                    print(f"{currentCharacter._name} ataca a si mesmo... por algum motivo")
                    time.sleep(2)
                    currentCharacter.attackEnemy(currentCharacter,False)
                    break
                case _:
                    print("Digite um número válido!")
                    time.sleep(2)
                    continue
        # Tira inimigos com vida 0
        enemies = [foes for foes in enemies if foes.health > 0]
        if len(enemies) == 0:
            break
        else:
        # Inimigos atacam
            print("\n")
            for i in enemies:
                i.attackEnemy(currentCharacter)
                print("\n")
            input(f"Pressione \"Enter\" para continuar")
            # Colocar morte de jogador aqui
            if currentCharacter.health <= 0:
                currentCharacter.resetMods()
                return False
    input(f"Todos os inimigos derrotados!\nPressione \"Enter\" para continuar")
    currentCharacter.resetMods()
    return True