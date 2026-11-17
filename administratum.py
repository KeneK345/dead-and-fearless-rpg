import sqlite3

dataTables = [
    """CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name text NOT NULL,
        victories INTEGER NOT NULL,
        defeats INTEGER NOT NULL
    );""",
    """CREATE TABLE IF NOT EXISTS character (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name text NOT NULL,
            player INTEGER NOT NULL,
            archetype TEXT NOT NULL,
            maxHP INTEGER NOT NULL,
            health INTEGER NOT NULL,
            maxMP INTEGER NOT NULL,
            mind INTEGER NOT NULL,
            baseATK INTEGER NOT NULL,
            attack INTEGER NOT NULL,
            modATK INTEGER NOT NULL,
            baseDEF INTEGER NOT NULL,
            defense INTEGER NOT NULL,
            modDEF INTEGER NOT NULL,
            gamestage INTEGER NOT NULL,
            FOREIGN KEY (player) REFERENCES user (id) ON DELETE CASCADE
    );""",
    """CREATE TABLE IF NOT EXISTS item (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        charId INTEGER NOT NULL,
        type text NOT NULL,
        name text NOT NULL,
        desc text NOT NULL,
        attack INTEGER NOT NULL,
        defense INTEGER NOT NULL,
        FOREIGN KEY (charId) REFERENCES character (id) ON DELETE CASCADE
    );""",
    """CREATE TABLE IF NOT EXISTS ability (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        charId INTEGER NOT NULL,
        name text NOT NULL,
        desc text NOT NULL
        FOREIGN KEY (charId) REFERENCES character (id) ON DELETE CASCADE
    );"""
]

def signUp(sacredLink,user):
    newUser = '''INSERT INTO user(name,victories,defeats) VALUES(?,0,0);'''
    cursor = sacredLink.cursor()
    cursor.execute(newUser,user)
    sacredLink.commit()
    return cursor.lastrowid
def getAllUsers(sacredLink):
    cursor = sacredLink.cursor()
    cursor.execute('SELECT id,name,victories,defeats FROM user;')
    users = cursor.fetchall()
    return users
def updateUserData(sacredLink,user):
    cursor = sacredLink.cursor()
    cursor.execute('UPDATE user SET name=?,victories=?,defeats=? WHERE id=?',user)
    sacredLink.commit()
    return "Usuário atualizado"
def deleteUser(sacredLink,user):
    cursor = sacredLink.cursor()
    cursor.execute('DELETE FROM user WHERE id = ?',user)
    sacredLink.commit()
    return "Usuário deletado"

def newCrusader(sacredLink,charData):
    newCharacter = '''INSERT INTO character (name,player,archetype,maxHP,health,maxMP,mind,baseATK,attack,modATK,baseDEF,defense,modDEF,gamestage) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    cursor = sacredLink.cursor()
    cursor.execute(newCharacter,charData)
    sacredLink.commit()
    return cursor.lastrowid
def getAllCrusaders(sacredLink, currentUser):
    cursor = sacredLink.cursor()
    cursor.execute('SELECT id,name,archetype FROM character WHERE player = ?', currentUser)
    chars = cursor.fetchall()
    return chars
def getCrusaderStats(sacredLink, savedCrusader):
    cursor = sacredLink.cursor()
    cursor.execute('SELECT id,name,player,archetype,maxHP,health,maxMP,mind,baseATK,attack,modATK,baseDEF,defense,modDEF,gamestage FROM character WHERE id = ?', savedCrusader)
    crusader = cursor.fetchall()
    return crusader
def updateCrusader(sacredLink, currentCrusader):
    cursor = sacredLink.cursor()
    cursor.execute('''UPDATE character SET maxHP=?,health=?,maxMP=?,mind=?,baseATK=?,attack=?,modATK=?,baseDEF=?,defense=?,modDEF=?,gamestage=? WHERE id = ?''', currentCrusader)
    sacredLink.commit()
    return "Cruzado atualizado"
def deleteCrusader(sacredLink, currentCrusader):
    cursor = sacredLink.cursor()
    cursor.execute('DELETE FROM character WHERE id = ?', currentCrusader)
    sacredLink.commit()
    return "Cruzado deletado"

def charObtainItem(sacredLink,itemData):
    newTreasure = '''INSERT INTO item (charId,type,name,desc,attack,defense) VALUES (?,?,?,?,?,?)'''
    cursor = sacredLink.cursor()
    cursor.execute(newTreasure,itemData)
    sacredLink.commit()
    return cursor.lastrowid
def editItem(sacredLink,itemData):
    item = '''UPDATE item SET name=?,desc=?,attack=?,defense=? WHERE id=?'''
    cursor = sacredLink.cursor()
    cursor.execute(item,itemData)
    sacredLink.commit()
    return "Item atualizado!!!"
def getCharWeapon(sacredLink,currentCrusader):
    excalibur = '''SELECT * FROM item WHERE charId = ? AND type = "Arma"'''
    cursor = sacredLink.cursor()
    cursor.execute(excalibur,currentCrusader)
    excalibur = cursor.fetchall()
    return excalibur
def getCharArmor(sacredLink,currentCrusader):
    hercules = '''SELECT * FROM item WHERE charId = ? AND type = "Armadura"'''
    cursor = sacredLink.cursor()
    cursor.execute(hercules,currentCrusader)
    hercules = cursor.fetchall()
    return hercules
def deleteItem(sacredLink, item):
    cursor = sacredLink.cursor()
    cursor.execute('DELETE FROM item WHERE id = ?', item)
    sacredLink.commit()
    return "Cruzado deletado"

def newAbility(abil):
    # Eu poderia ter usado isso...
    global sacredLink, cursor
    cursor.execute('INSERT INTO ability (charId,name,desc) VALUES (?,?,?)',abil)
    sacredLink.commit()
    return cursor.lastrowid
def getCharAbilities(character):
    global sacredLink,cursor
    cursor.execute('SELECT * FROM ability WHERE charId=?',character)
    return cursor.fetchall()
def updAbility(abil):
    global sacredLink,cursor
    cursor.execute('UPDATE ability SET name=?,desc=? WHERE id=?',abil)
def deleteAbility(abil):
    global sacredLink,cursor
    cursor.execute('DELETE FROM ability WHERE id=?',abil)

try:
    with sqlite3.connect("deadNfearless.bd") as sacredLink:
        # Retire o hash para recitar o Rito de Ativação
        #print("Thus do we invoke the Machine God\nThus do we stir this spirit from slumber\nMay it be filled with the holy power of the Motive Force\nMay its awakening be swift, its sacred code untarnished, uncorrupted\nSing praise for this new machine that lives in service to the Omnissiah's Great Work\nMay its spark never fade!\nAve Deus Mechanicus!")
        
        sacredLink.execute("PRAGMA foreign_keys = ON")
        cursor = sacredLink.cursor()

        for table in dataTables:
            cursor.execute(table)

        sacredLink.commit()
except sqlite3.OperationalError as e:
    print("You fucking dumbass. What went wrong: ", e)