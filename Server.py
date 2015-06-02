# CSS432 - Server
# Bethel Heo, Bartosz Dabkowski, Xiaoyu Liang
#
# Server.py
# This program is a game server that creates a socket and listens for incoming game connections

from socket import *
import random

# initialize variables
game_list = []
score_board = []
newGameID = 0

# single entry on score board
class ScoreEntry:
    def __init__(self):
        self.player = ""
        self.score = 0

# single game pair
class GamePair:
    def __init__(self):
        self.ID = 0
        self.name = ''
        self.creator = ''
        self.player = ''

#====================================================================================================

# print game list
def print_game_list():
    for game in game_list:
        print '{0:1d} {1:10s} {2:20s} {3:20s}'.format(game.ID, game.name, game.creator, game.player)


# print score board
def print_score_board():
    for entry in score_board[:10]:
        print entry.player, entry.score

#====================================================================================================

# create socket, bind, and listen
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print'The game server is ready to receive'
title = 0

#====================================================================================================

# keep alive while accepting incoming connections
while 1:
    
    # print title
    if title == 0:
        print '{0:1s} {1:10s} {2:20s} {3:20s}'.format('ID', 'NAME', 'CREATOR', 'PLAYER')
        title += 1
    
    # accept connection
    connectionSocket, addr = serverSocket.accept()

    # print connection ip and port
    print('ip and port: ', addr)
    print('accepted')

    # receive request
    request = connectionSocket.recv(1024)
    print ('Request:', request)

    # parse if it is join/end request
    if request.find('_') > 0:
        request, gameID = request.split('_')

#====================================================================================================

    # create game entry into game list
    if request == 'create':
        
        # create game entry
        current = GamePair()
        current.player = 'Waiting'
        game_list.append(current)
        newGameID += 1
        current.ID = newGameID
        current.name = 'Game ' + str(current.ID)
        
        # randomly assign a port number
        port = random.randint(10000, 65535)
        current.creator = list(addr)
        current.creator[1] = port
        
        # send response
        respond = str(current.ID) + '_' + str(port)
        connectionSocket.send(respond)
        
        # print game list
        print_game_list()

#====================================================================================================

    # join game, send back the creator's ip and port
    elif request == 'join':

        for game in game_list:
            if str(game.ID) == gameID:
                #if pair exists
                if game.player != 'Waiting':
                    connectionSocket.send('Game Not Available')
                    print'ERROR: Game Not Available'
                else:
                    
                    # add player addr to the game list
                    game.player = list(addr)

                    # send creator addr back to player
                    response = str(game.creator)
                    print(game.player, 'joining game:', response)
                    connectionSocket.send(response)
                     
                    # print game list
                    print_game_list()
                    break

#====================================================================================================

    # end game, update results, remove game pair from game list
    elif request == 'end':

        # parse gameID and game result
        gameID, result = gameID.split(' ')

        print('End game results', request, gameID, result)

        # update game result and add into scoreboard
        for game in game_list:
            if str(game.ID) == gameID:
                
                # empty score board
                if len(score_board) == 0:
                    if result == '1':
                        # add creator
                        firstEntry = ScoreEntry()
                        firstEntry.player = game.creator[0]
                        firstEntry.score += 1
                        score_board.append(firstEntry)

                        # add player
                        secondEntry = ScoreEntry()
                        secondEntry.player = game.player[0]
                        score_board.append(secondEntry)

                    else:
                        # add player
                        firstEntry = ScoreEntry()
                        firstEntry.player = game.player[0]
                        firstEntry.score += 1
                        score_board.append(firstEntry)

                        # add creator
                        secondEntry = ScoreEntry()
                        secondEntry.player = game.creator[0]
                        score_board.append(secondEntry)
                else:
                    
                    creatorExist = 0
                    playerExist = 0
                    
                    # loop through entries in score board and update result
                    for entry in score_board:
                        
                        # update creator score
                        if entry.player == game.creator[0]:
                            creatorExist = 1
                            if result == '1':
                                entry.score += 1
                    
                        # update player score
                        if entry.player == game.player[0]:
                            playerExist = 1
                            if result == '0':
                                entry.score += 1
                      
                      
                    # creator not exist in the list
                    if creatorExist == 0:
                        if result == '1':
                            # add creator
                            firstEntry = ScoreEntry()
                            firstEntry.player = game.creator[0]
                            firstEntry.score += 1
                            score_board.append(firstEntry)

                        else:
                            # add creator
                            secondEntry = ScoreEntry()
                            secondEntry.player = game.creator[0]
                            score_board.append(secondEntry)

                    # player not exist in the list
                    if playerExist == 0:
                        if result == '0':
                            # add player
                            firstEntry = ScoreEntry()
                            firstEntry.player = game.player[0]
                            firstEntry.score += 1
                            score_board.append(firstEntry)

                        else:
                            # add player
                            secondEntry = ScoreEntry()
                            secondEntry.player = game.player[0]
                            score_board.append(secondEntry)
                                
                # remove game from game list
                game_list.remove(game)
        
        # print game list
        print_game_list()

        # sort score_board on key score
        score_board.sort(key=lambda x : x.score, reverse = True)
        
        # print score board
        print_score_board()
        
        # send back updated
        response = 'result updated'
        connectionSocket.send(response)

#====================================================================================================

    # send back game list in string
    elif request == 'list':
        
        # initialize string varible
        gameList = ""
        
        for game in game_list[:-1]:
            
            # add available game into string varible
            if game.player == 'Waiting':
                gameList += str(game.ID) + ' '
    
        # postfence
        if game_list[len(game_list) - 1].player == 'Waiting':
            gameList += str(game_list[len(game_list) - 1].ID)
        
        # print game list and send back
        print('Game list:', gameList)
        connectionSocket.send(gameList)
        print_game_list()

#====================================================================================================

    # send back score board in string
    elif request == 'top':

        # initialize string varible
        msg = ''
        
        # scoreboard empty
        if(len(score_board) == 0):
            msg = 'empty'
            connectionSocket.send(msg)
            print('No scores')
        else:
            
            # add score into string varible
            for entry in score_board[:-1]:
                
                # parse just the IP address
                msg += entry.player + ' ' + str(entry.score) + ' '
            
            # post fence
            msg += score_board[len(score_board) - 1].player + ' ' + str(score_board[len(score_board) - 1].score)

            # print scoreboard and send back
            connectionSocket.send(msg)
            print msg

    print 'msg sent'
    
    # close socket
    connectionSocket.close()
    print('closed')

# close server socket
serverSocket.close()
