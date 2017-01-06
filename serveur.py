#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
import select
import threading
import time

START_GAME = 5
ERROR_MOVE = 6
GAME_MOVE = 7
ACK = 8
GAME_OVER = 9
GOOD_CASE = 10
SPECTATOR = 11
WINNER = 12
LOOSER = 13

hote= "localhost"
port = 7778

nb_client = 0
gamers=[]
spectator = []
array_game = [2,2,2,2,2,2,2,2,2]
current_player = 0
game_over=0

def winner(player):
    if (player==gamers[0]): #on attribue la valeur de la case de chaque joueur
        player_box=0
    if (player==gamers[1]):
        player_box=1

    # horizontal line
    for y in range(3): 
        if array_game[y*3] == player_box and array_game[y*3+1] == player_box and array_game[y*3+2] == player_box:
            return True
    #vertical line
    for x in range(3):
        if array_game[x] == player_box and array_game[3+x] == player_box and array_game[6+x] == player_box:
            return True
    #diagonals :
    if array_game[0] == player_box and array_game[4] == player_box and array_game[8] == player_box:
        return True
    if array_game[2] == player_box and array_game[4] == player_box and array_game[6] == player_box:
        return True
        
    return False
	
def gameOver():
    global game_over
    if winner(gamers[0]):
        game_over=1
        return gamers[0]    
    if winner(gamers[1]):
        game_over=1
        return gamers[1]
    return 0         

def game():
    
    while nb_client<2: #on attend deux joueurs pour commencer la partie
        time.sleep(1)
        
    message = str(START_GAME).encode()#envoie du signal de début de jeu
    gamers[0].send(message)
    gamers[1].send(message)

    current_player = gamers[1]#le premier joueur est le dernier joueur a avoir rejoint la connexion
    
    global game_over
    
    while (game_over != 1):#tant qu'aucun des deux joueurs a gagné on continue
    
        message = str(GAME_MOVE).encode() #envoie de message pour demander au joueur actif de choisir une case
        time.sleep(0.1)
        current_player.send(message)
        time.sleep(0.1)
            
        position = current_player.recv(1024).decode() #on attends la réponse du joueur actif
        position = int(position)
                
        for i in range(len(array_game)): #on vérifie chaque position pour savoir si elle est valide ou non
            if i==position:
                if array_game[i] == 2:
                    if(current_player==gamers[0]):
                        array_game[i]=0
                        last_player=gamers[0]
                        message=str(GOOD_CASE).encode()
                        gamers[0].send(message)
                        time.sleep(0.1)
                    else:
                        array_game[i]=1
                        last_player=gamers[1]
                        message=str(GOOD_CASE).encode()
                        gamers[1].send(message)
                        time.sleep(0.1)
                else:
                    message=str(ERROR_MOVE).encode()
                    current_player.send(message)
                    time.sleep(0.1)
                                                
        if (last_player == gamers[0]): #on change le joueur actif si son coup était valide
            current_player=gamers[1]
        else:
            current_player=gamers[0]

        gameOver() #on vérifie si la partie est terminée
        
    message = str(GAME_OVER).encode() #on envoie un message pour dire que la partie est terminé
    gamers[0].send(message)
    gamers[1].send(message)
    message = str(SPECTATOR).encode()
    spectator[0].send(message)
    
    time.sleep(1)
    gamers[0].send(bytes(array_game)) #on envoie le tableau final du jeu
    gamers[1].send(bytes(array_game))
    spectator[0].send(bytes(array_game))
    time.sleep(1)
    
    winner=gameOver()
    
    if(winner==gamers[0]): #on envoie le résultat de la partie au joueur
        message = str(WINNER).encode()
        gamers[0].send(message)
        message = str(LOOSER).encode()
        gamers[1].send(message)
    else:
        message = str(WINNER).encode()
        gamers[1].send(message)
        message = str(LOOSER).encode()
        gamers[0].send(message)
    
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #on ouvre le serveur
socket.bind(('', port))
socket.listen(5)
print("Démarrage serveur : port : {}".format(port))

threadgame = threading.Thread(None, game,None, (), {}) #on crée puis on démarre une thread qui va gérer la partie
threadgame.start()

while 1: #on sauvegarde les connexions
    client, address = socket.accept()
    nb_client = nb_client+1
    if(nb_client==1):
        gamers.append(client)
    if(nb_client==2):
        gamers.append(client)
    if(nb_client>2):
        spectator.append(client)

