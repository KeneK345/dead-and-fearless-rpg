# Dados base para construir todas as armaduras do jogo
import math

def dkStartArmor(enchant):
    name="Cota de Malha"
    desc="Um traje feito de anéis de aço escuro ligados um ao outro, vestido por cima de um gambesão.\nProtege bem para seu peso, e vem com uma cóifa de malha para a cabeça!"
    attack=0
    defense=10+enchant
    return ("Armadura",name,desc,attack,defense)
def pmStartArmor(enchant):
    name="Roupão Reforçado"
    desc="Um roupão grande de mago feito de lã de ovelha e reforçado com seda barata. Chapéu pontudo não incluído.\nA lã fica mais roxa quanto mais feitiços são imbuídos nela."
    attack=2
    defense=2+enchant
    return ("Armadura",name,desc,attack,defense)
def rpStartArmor(enchant):
    name="Peitoral Abençoado"
    desc="Um peitoral de ferro por cima de um roupão vermelho de sacerdote, polido e ungido com óleo inodor.\nInúmeras páginas de livros sagrados foram acopladas dentro do peitoral para imitar a proteção de um gambesão."
    attack=1
    defense=5+enchant
    return ("Armadura",name,desc,attack,defense)