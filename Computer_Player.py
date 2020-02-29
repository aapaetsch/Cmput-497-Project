#Alpha Beta code adapted from https://webdocs.cs.ualberta.ca/~c455/python/alphabeta_with_move.py
#Transposition Table adapted from https://webdocs.cs.ualberta.ca/~c455/python/transposition_table_simple.py
import random
import time

class TranspositionTable(object):
    def __init__(self):
        self.visited = {}

    def __repr__(self):
        return self.visited.__repr__()

    def store(self, hashValue, score):
        self.visited[hashValue] = score
        

    def lookup(self, hashValue):
    	#<--Returns None if State has not been visited, otherwise it returns its value--->
        return self.visited.get(hashValue)

class FourInARow_AB:
	def __init__(self, maxDepth):
		self.__maxDepth = maxDepth
		#<---Give the state as a copy of the board--->
		#<---Give it access to check win and move coords--->
		#<--access to the current player--->

	def findMove(self, gameState):
		#<---Creates the zobrist Array and sets the current hash--->
		self.tt = TranspositionTable()
		rootState = gameState.copyState()
		self.bestMove = None
		self.ComputerPlayer = rootState.getCurrentPlayer()
		self.zobristinit(rootState)
		
		alpha = -float('Inf')
		beta = float("Inf")
		value = self.alphaBetaGetMove(alpha, beta, self.__maxDepth, rootState)
		print('Best Move:', self.bestMove, '\tValue:', value)
	
		return self.bestMove if self.bestMove != None else random.choice(rootState.getValidMoves())

	def alphaBetaGetMove(self, alpha, beta, depth, gameState):
		legalMoves = gameState.getValidMoves()
		terminalState, points = self.isTerminal(legalMoves, gameState)
		bestMove = None

		if terminalState:
			return points, None 

		for move in legalMoves:
			
			oldHash = self.hash
			y, x = gameState.playMove(move)
			self.updateHash(self.hash, self.zobristArr[y][x][gameState.getCurrentPlayer()], self.zobristArr[y][x][0])
			self.changePlayer(gameState)

			value = -self.alphaBetaDL( -beta, -alpha, depth - 1, gameState)

			if value > alpha:
				alpha = value
				bestMove = move

			self.hash = oldHash
			self.undo(y, x, gameState)

			if value >= beta:
				return beta, bestMove

		return alpha, bestMove

	def alphaBetaDL(self, alpha, beta, depth, gameState):
		result = self.tt.lookup(self.hash)
		if result !=  None:
			return result

		legalMoves = gameState.getValidMoves()
		terminalState, points = self.isTerminal(legalMoves, gameState)
		#<---Is terminal needs a state--->
		if terminalState:
			return points
		elif depth == 0:
			return self.evaluation(gameState)
		
		for move in legalMoves:

			#<---Play the move on a copy of the board
			oldHash = self.hash
			#<---Update the hash
			y, x = gameState.playMove(move)
			self.updateHash(self.hash, self.zobristArr[y][x][gameState.getCurrentPlayer()], self.zobristArr[y][x][0])
			#<---UPDATE THE CURRENT PLAYER
			self.changePlayer(gameState)

			value = -alphaBetaDL(-beta, -alpha, depth - 1, gameState)
			if value > alpha:
				alpha = value

			#<---Revert to previous hash and undo move from board
			self.hash = oldHash
			self.undo(y, x, gameState)

			if value >= beta:
				return beta

		return alpha

	def changePlayer(self, gameState):
		gameState.setCurrentPlayer( 3 - gameState.getCurrentPlayer())

	def undo(self, y, x, gameState):
		self.changePlayer(gameState)
		gameState.setBoardPosition(y, x, 0)

	def isTerminal(self, legalMoves, gameState):
		#<---If you can win + 10000            
		if gameState.previousYX != None:
			#<----If we are in a terminal state--->
			if gameState.checkWin(gameState.previousYX[1],gameState.previousYX[0]):
				return True, 10000
			
			elif len(legalMoves) == 0:
				return True, 0 
		
		return False, None


	# def evaluation(self, gameState):
	# 	#100 for 4  in a row
	# 	#50 for 3 in a row
	# 	#10 for 2 in a row
	# 	#Only add if they have at least 1 empty next to it
	# 	opponent = 3 - self.ComputerPlayer
	# 	board = gameState.getBoard()
	# 	#<---Count Horizontal--->
	# 	self.boardSize[0]#<---For Rows
	# 	for row in range(gameState.boardSize[0]):
	# 		pass

	# 	#<---Count vertical--->
	# 	for col in range(gameState.boardSize[1]):
	# 		pass

	# 	#<---Count Diagonal--->
	# 	for diag in range()

	# 	#<---Count Anti Diagonal--->

	# def getInRow(self, row, player, opponent):
	# 	inRowCount = [0,0,0]
	# 	inRowCountOpp = [0,0,0]
	# 	pass




	def zobristinit(self, gameState):

		self.zobristArr = []
		for i in range(gameState.boardSize[0]):
			self.zobristInnerArr = []
			for j in range(gameState.boardSize[1]):
				self.zobristInnerArr.append([random.getrandbits(64) for _ in range(3)])
			self.zobristArr.append(self.zobristInnerArr)

		board = gameState.getBoard()
		c = 0 
		for row in range(gameState.boardSize[0]):
			for column in range(gameState.boardSize[1]):
				if row == 0 and column == 0 :
					self.hash = self.zobristArr[0][0][board[row][column]]
				else:
					self.hash = self.hash ^ self.zobristArr[row][column][board[row][column]]


	def updateHash(self, oldHash, XORin, XORout):
		self.hash = oldHash ^ XORin ^XORout

	
