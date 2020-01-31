import numpy as np
import sys
import os


class Connect4:

	def __init__(self, diff, opp):

		self.__board = []
		self.__player = 'R' # (Players as 1 and 2 )
		self.__boardSize = (6,7)
		self.__isWin = False
		self.__remainingMoves = 6 * 7
		self.__clear = 'cls' if sys.platform == 'win32' else 'clear'
		self.__opponent = opp #Can be "player or computer"
		self.__difficulty = diff # Maybe do easy medium hard?

	def __makeBoard(self):
		# Really only necessary if we have varying board sizes
		y = self.__boardSize[0]
		x = self.__boardSize[1]
		self.__board =  [ [' '] * x for i in range(y)]

	

	def showBoard(self):

		print(' ' + ' '.join([str(i) for i in range( 1, self.__boardSize[1] + 1) ]))

		for row in self.__board:
			r = '|'
			for i in row: 
				r += i + "|"
			print(r)

	

	def clearScreen(self):
		os.system(self.__clear)

	def __checkWin(self, x, y):
		# This method takes in a Moves x,y coords and checks if it results in a win
		inRow = 0
		# First check horizontal
		if self.__checkHorizontal(y):
			return True, "horizontal"

		if self.__checkVertical(x):
			return True, "vertical"

		# if self.__checkDiagonal(x,y):

		# 	return True, "Left Diagonal"

		# 	return True, "Right Diagonal"

		# return False, "No win"


		
	def __checkHorizontal(self, y):
		inRow = 0 
		for i in range(self.__boardSize[y][i]):
			inRow = inRow + 1 if self.__board[y][i] == self.__player else 0
			if inRow == 4:
				return True
		return False

	def __checkVertical(self, x):
		inRow = 0
		for i in range(self.__boardSize[i][x]):
			inRow = inRow + 1 if self.__board[i][x] == self.__player else 0
			if inRow == 4:
				return True
		return False

	# def __checkDiagonal(x,y):



		# Then check vertical

		# Finally check diagonals 

	

	def __playMove(self, move):


		# This method takes in a move and plays it on the board if it is valid
		try:
			# Check if the move is valid
			move = int(move) - 1
			if move >= 0 and move <= self.__boardSize[1]:
				print('hello')
				# Ignore the loop for checking if the column is already full.
				if self.__board[0][move] == ' ':
					# Find the last empty pos in column and put tkn there
					for i in range(self.__boardSize[0], -1, -1): #Bottom up
						print(i)
						if self.__board[i][move] == ' ':

							self.__board[i][move] = self.__player
							print('hello')
							
							if self.__checkWin(move, i):
								self.__isWin = True
							
							return (True, move)
				else:
					
					print("Move {} is invalid, column is full.".format(str(move + 1)))
					return (False,0)
			else:
				
				print("Move {} is invalid, out of board range.".format(str(move + 1)))
				return (False, 0)

		except: 
			#If invalid move entered, notify user and return False
			print("Move {} is invalid.".format(move))
			return (False, 0)

	def turn(self, move):
		#Change turn to take in move as an argument so that a computer player can play

		while True:

			m = input("Player {} Enter Move >".format(self.__player))
			pMove = self.__playMove(m)
			print(pMove)
			
			if pMove[0]:
				move = pMove[1]
				break
		
		win = self.__checkWin()
		self.__isWin = win[0]
		
		print(win)

		if self.__isWin():
			print("Player {}".format(self.__player))
			return True

		elif self.__remainingMoves == 0:
			print("Game Is A Tie! No Moves Remaining.")
			return True

		else:
			self.__player = 'R' if self.__player == 'Y' else 'R'
			self.__remainingMoves -= 1 
			return False



	def startGame(self):
		self.__makeBoard()

	def getBoard(self):
		return self.__board

	def getWin(self):
		return self.__isWin

	def getPlayer(self):
		return self.__player

	def getRemainingMoves(self):
		return self.__remainingMoves






def main():
	c4 = Connect4()
	c4.startGame()

	while True:

		c4.clearScreen()
		c4.showBoard()

		gameOver = c4.turn()
		
		if gameOver:
			break

	









if __name__ == '__main__':
	main()
