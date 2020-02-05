import numpy as np
import sys
import os


class Connect4:

    def __init__(self):

        self.__player = 1
        
        self.__boardSize = (6,7) #Just in case we want to do variable sizes
        self.__board = np.zeros((self.__boardSize[0], self.__boardSize[1]), dtype=int)

        self.__isWin = False
        self.__winType = None
        self.__winner = None
        self.__validMoves = [i for i in range(self.__boardSize[1])]

    def __checkWin(self, x, y):
        # This method takes in a moves x,y coords and checks if it results in a win
        horizontal = self.__board[y]
        vertical = self.__board[:,x]
        diagonalLR = self.__board.diagonal(x - y)
        diagonalRL = np.fliplr(self.__board).diagonal(abs(x-self.__boardSize[0]) - y)

        if self.__checkInRow(horizontal):
            return True, 'horizontal'
        
        elif self.__checkInRow(vertical):
            return True, 'vertical'
        
        elif self.__checkInRow(diagonalLR):
            return True, 'LR Diagonal'

        elif self.__checkInRow(diagonalRL):
            return True, 'RL diagonal'

        return False, None

    def __checkInRow(self, array):
        inRow = 0
        for i in array:
            inRow = inRow + 1 if i == self.__player else 0
            if inRow == 4:
                return True
        return False

    def __playMove(self, move):
        # This method takes in a move and plays it on the board

        for i in range(self.__boardSize[0]-1, -1, -1):
            if self.__board[i][move] == 0:
                self.__board[i][move] = self.__player
                if i == 0:
                    self.__validMoves.remove(move)
                return [i, move]
                
    def turn(self, move):
        # This method is used for a player to take a turn
        # Returns True if move is valid, otherwise False
        try:
            move = int(move)
        
        except:
            return False

        if move in self.__validMoves:
            y, x = self.__playMove(move)

            self.__isWin, self.__winType = self.__checkWin(x, y)

            self.__winner = self.__player
            self.__player = 2 if self.__player == 1 else 1

            return True

        else:
            return False

    def getWin(self):
        return self.__isWin

    def getWinType(self):
        return self.__winType

    def getWinner(self):
        return self.__winner

    def getValidMoves(self):
        return self.__validMoves

    def getWinStatus(self):
        return self.__isWin

    def getCurrentPlayer(self):
        return self.__player

    def getBoard(self):
        return self.__board

    def showBoard(self):
        # This method is only used for the text version of the game
        
        halfTxt = 10  - self.__boardSize[1]
        title = '\n {}Connect 4!{}\n\n'.format(' '*halfTxt, ' '*halfTxt)
        board = '  ' + ' '.join([str(i) for i in range(self.__boardSize[1])]) + '\n'
        
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




