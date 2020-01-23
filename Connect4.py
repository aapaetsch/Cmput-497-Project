import numpy as np



class Connect4:

	def __init__(self):

		self.__board = []
		self.__player = 1 # (Players as 1 and 2 )
		self.__boardSize = (6,7)

	def __makeBoard(self):
		# Really only necessary if we have varying board sizes
		self.__board =  np.zeros(self.__boardSize)
		


	def getBoard(self):
		return self.__board

	def showBoard(self):
		for row in self.__board:
			print(row)

	def __checkWin(self, move):
		# This method takes in a move and checks if it results in a win

	def __playMove(self, move):
		# This method takes in a move and plays it on the board if it is valid
		try:
			# Check if the move is valid
			move = int(move) - 1
			if move >= 0 and move <= self.__boardSize[1]:

				# Ignore the loop for checking if the column is already full.
				if self.__board[0][move] == 0:
					# Find the last empty pos in column and put tkn there
					for i in range(self.__boardSize[0], -1, -1): #Bottom up
						
						if self.__board[i][move] == 0:
							self.__board[i][move] = self.__player
							return True
				else:
					
					print("Move {} is invalid, column is full.".format(str(move)))
					return False
			else:
				
				print("Move {} is invalid, out of board range.".format(str(move)))
				return False

		except:
			#If invalid move entered, notify user and return False
			print("Move {} is invalid.".format(move))
			return False


		#not sure what to do with this yet

	# def turn(self):
	# 	while True:
	# 		player = 'Red' if self.__player == 1 else 'Yellow'
	# 		move = input("{} player enter a move > ".format(player))
	# 		try:
	# 			move = int(move)

	# 			break
	# 		except:
	# 			print("Move {} is invalid.".format(move))
	
	def test(self):
		self.__makeBoard()
		self.showBoard()



def main():
	c4 = Connect4()
	c4.test()







if __name__ == '__main__':
	main()
