import numpy as np
import sys
import os
import random


class Four_In_A_Row(object):

    def __init__(self):

        self.__player = 1
        
        self.boardSize = (6,7) #Just in case we want to do variable sizes
        self.__board = np.zeros(self.boardSize, dtype=int)

        self.isWin = False
        self.winType = None
        self.winner = None
        self.validMoves = [i for i in range(self.boardSize[1])]
        self.previousMove = None


    def resetGame(self):
        self.__player = 1
        self.__board = np.zeros(self.boardSize, dtype=int)
        self.isWin = False
        self.winType = None
        self.winner = None
        self.validMoves = [i for i in range(self.boardSize[1])]

    def copyState(self):
        cBoard = Four_In_A_Row()
        cBoard.setCurrentPlayer(self.__player)
        cBoard.isWin = self.isWin
        cBoard.winner = self.winner
        cBoard.validMoves = self.validMoves
        cBoard.winType = self.winType
        cBoard.setBoard(np.copy(self.__board))
        return cBoard

    def checkWin(self, x, y):
        # This method takes in a moves x,y coords and checks if it results in a win
        horizontal = self.__board[y]
        vertical = self.__board[:,x]
        diagonalLR = self.__board.diagonal(x - y)
        diagonalRL = np.fliplr(self.__board).diagonal(abs(x-self.boardSize[0]) - y)

        if self.checkInRow(horizontal):
            return True, 'horizontal'
        
        elif self.checkInRow(vertical):
            return True, 'vertical'
        
        elif self.checkInRow(diagonalLR):
            return True, 'LR Diagonal'

        elif self.checkInRow(diagonalRL):
            return True, 'RL diagonal'

        return False, None

    def __checkInRow(self, array):
        inRow = 0
        for i in array:
            inRow = inRow + 1 if i == self.__player else 0
            if inRow == 4:
                return True
        return False

    def playMove(self, move):
        # This method takes in a move and plays it on the board

        for i in range(self.boardSize[0]-1, -1, -1):
            if self.__board[i][move] == 0:
                self.__board[i][move] = self.__player
                if i == 0:
                    self.validMoves.remove(move)
                self.previousYX = [i, move]
                return [i, move]
                
    def turn(self, move):
        # This method is used for a player to take a turn
        # Returns True if move is valid, otherwise False
        try:
            move = int(move)
        
        except:
            return False

        if move in self.validMoves:
            y, x = self.playMove(move)

            self.isWin, self.winType = self.checkWin(x, y)
            
            if self.isWin:
                self.winner = self.__player

            self.__player = 1 + 2 - self.__player

            return True

        else:
            return False

    def getWin(self):
        return self.isWin

    def getWinType(self):
        return self.winType

    def getWinner(self):
        return self.winner

    def getValidMoves(self):
        valid = []
        for i in self.__board[0]:
            if i == 0:
                valid.append(i)
        return valid

    def getWinStatus(self):
        return self.isWin

    def getCurrentPlayer(self):
        return self.__player

    def getBoard(self):
        return self.__board

    def setCurrentPlayer(self,player):
        self.__player = player

    def setBoard(self, board):
        self.__board = board
    
    def setBoardPosition(self, y, x, state):
        self.__board[y][x] = state


    def showBoard(self):
        # This method is only used for the text version of the game
        
        
        title = '\n Four In A Row!\n\n'
        board = '  ' + ' '.join([str(i) for i in range(self.boardSize[1])]) + '\n'
        
        for row in self.__board:
            board += ' |'
    
            for i in row:
                
                if i == 0:
                    board += ' '
                else:
                    board += str(i)
                
                board += '|'
            board += '\n'

        print(title + board)




