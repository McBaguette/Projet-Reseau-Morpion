#!/usr/bin/python3
import socket
import select
import threading

START_GAME = 5
ERROR_MOVE = 6
GAME_MOVE = 7
ACK = 8
GAME_OVER = 9
GOOD_CASE = 10
SPECTATOR = 11
WINNER = 12
LOOSER = 13

hote = "localhost"
port = 7778

array_player = [2,2,2,2,2,2,2,2,2]
array_game = [2,2,2,2,2,2,2,2,2]
game_over = 0

connexion_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #le client se connecte au serveur
connexion_with_server.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

def print_help():
    print("         0|1|2")
    print("         3|4|5")
    print("         6|7|8")                                    
    print("")
    
def print_game_player():#affiche le tableau de jeu du joueur

    for i in range(len(array_player)):
        if i % 3 == 0:
            print("")
        if (array_player[i] == 2):
            print(" ", end=" | ")
        else:
            print("U", end=" | ")
    print("")
    print("")
    
def print_game():#affiche le tableau de jeu du joueur
    
    for i in range(len(array_game)):
        if i % 3 == 0:
            print("")
        if (array_game[i] == 2):
            print(" ", end=" | ")
        elif (array_game[i] == 0):
            print("O", end=" | ")
        else:
            print("X", end=" | ")
    print("")
    print("")
    
while(game_over!=1):
        
    response=connexion_with_server.recv(1024).decode(); #reçoit une réponse du serveur
    response=int(response)
  
    if(response == START_GAME):
        
        print("Le nombre de joueur est atteint !")
        print_help()
                
    if(response==GAME_MOVE or response==ERROR_MOVE): #si on doit choisir une case pour jouer ou si la case donnée précedemment est fausse
                   
        if(response==ERROR_MOVE):
            print("Le mouvement est impossible")
        move=0
        while move!=1:
            message=input("Entrer une case : ")
            message=int(message)
            if((message<10)&(message>=0)): #vérifie si la case est comprise dans l'intervalle du tableau de jeu
                message = str(message).encode()
                connexion_with_server.send(message)
                move=1
            else:
                message=print("Erreur de frappe")

    if(response==GAME_OVER or response==SPECTATOR): #affiche le tableau du jeu reçu par le serveur
        if(response==SPECTATOR):
            print("O = J1 | X = J2")
        array_game = connexion_with_server.recv(1024)
        print_game()

        
    if(response==GOOD_CASE): #si la case jouait précédemment était valide alors on affiche le tableau du jeu du joueur
        message=int(message)
        array_player[message]=3
        print_game_player()
                
    if(response==WINNER):
        print("Vous avez gagné")
        game_over=1

    if(response==LOOSER):
        print("Vous avez perdu")
        game_over=1
        
connexion_with_server.close()

