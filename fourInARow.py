import numpy as np
import sys
import os
import random
import time
import re

class Four_In_A_Row(object):

    def __init__(self):

        self.__player = 1
        
        self.boardSize = (6,7) #Just in case we want to do variable sizes
        self.__board = np.zeros(self.boardSize, dtype=int)

        self.isWin = False
        self.winType = None
        self.winner = None
        self.previousYX = None


    def resetGame(self):
        self.__player = 1
        self.__board = np.zeros(self.boardSize, dtype=int)
        self.isWin = False
        self.winType = None
        self.winner = None
        

    def copyState(self):
        cBoard = Four_In_A_Row()
        cBoard.setCurrentPlayer(self.__player)
        cBoard.isWin = self.isWin
        cBoard.winner = self.winner
        cBoard.winType = self.winType
        cBoard.setBoard(np.copy(self.__board))
        return cBoard

    def checkWin(self, x, y):
        #<---Horizontal--->
        if self.__checkInRow(self.__board[y]):
            return True, 'horizontal'
        #<---Vertical--->
        elif self.__checkInRow(self.__board[:,x]):
            return True, 'vertical'
        #<---diagonalLR--->
        elif self.__checkInRow(self.__board.diagonal(x - y)):
            return True, 'diagonalLR'
        #<---diagonalRL--->
        elif self.__checkInRow(np.fliplr(self.__board).diagonal(abs(x - self.boardSize[0]) - y)):
            return True, 'diagonalRL'

        return False, None

    def __checkInRow(self, arr):
        inRow = 0
        for i in arr:
            inRow = inRow + 1 if i == self.__player else 0
            if inRow == 4:
                return True
        return False

    def playMove(self, move):
        # This method takes in a move and plays it on the board
        y = np.where(self.__board[:,move]==0)[0][-1]
        self.__board[y][move] = self.__player
        self.previousYX = [y,move]
        return [y,move]
        
                
    def turn(self, move):
        # This method is used for a player to take a turn
        # Returns True if move is valid, otherwise False
        try:
            move = int(move)
        
        except:
            return False

        if move in self.getValidMoves():
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
        return np.where(self.__board[0] == 0)[0]

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




