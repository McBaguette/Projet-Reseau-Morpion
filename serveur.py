#!/usr/bin/python3
import socket
import select
import threading

nb_client= 0
J1=NULL
J2=NULL
spectator = []
array_game = [-1,-1,-1,-1,-1,-1,-1,-1,-1]

def winner(player):
    assert(player==J1 or player==J2)
    # horizontal line
    for y in range(3): 
        if cells[y*3] == player and cells[y*3+1] == player and cells[y*3+2] == player:
            return True
    # vertical line
    for x in range(3): 
        if cells[x] == player and cells[3+x] == player and cells[6+x] == player:
            return True
    #diagonals :
    if cells[0] == player and cells[4] == player and cells[8] == player:
        return True
    if cells[2] == player and cells[4] == player and cells[6] == player:
        return True
    return False

def gameOver():
    if winner(J1):
        return J1
    if winner(J2):
        return J2
    for i in range(NB_CELLS):
        if(cells[i]== EMPTY):
            return -1
    return 0

def game():
    while 1:
        if(nb_client>1):
            sendto(data[, flags], J2)
            
        
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 7777))
connexion_principale.listen(5)
threadgame = threading.Thread(None, game,None, (), {})
threadgame.start()

while gameOver():
    client, address = socket.accept()
    nb_client = nb_client+1
    if(nb_client==1):
        J1=client
    if(nb_client==2):
        J2=client
    if(nb_client>2):
        spectator.append(client)

socket.close()
