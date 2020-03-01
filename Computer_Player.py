#Alpha Beta code adapted from https://webdocs.cs.ualberta.ca/~c455/python/alphabeta_with_move.py
#Transposition Table adapted from https://webdocs.cs.ualberta.ca/~c455/python/transposition_table_simple.py
import random
import time
import re
import numpy as np

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
		self.ComputerPlayer = rootState.getCurrentPlayer()
		self.zobristinit(rootState)
		
		alpha = -float('Inf')
		beta = float("Inf")
		value, move = self.alphaBetaGetMove(alpha, beta, self.__maxDepth, rootState)
		print('Best Move:', move, '\tValue:', value)
	
		return move if move != None else random.choice(rootState.getValidMoves())

	def alphaBetaGetMove(self, alpha, beta, depth, gameState):
		legalMoves = gameState.getValidMoves()
		terminalState, points = self.isTerminal(legalMoves, gameState)
		bestMove = None
		self.nodes = 0 
		if terminalState:
			return points, None 

		#<---we should try move 3 first (center is strongest)
		if 3 in legalMoves:
			legalMoves.remove(3)
			legalMoves = [3] + legalMoves

		for move in legalMoves:
			self.nodes += 1
			start = time.time()
			oldHash = self.hash
			previousYX = gameState.previousYX
			y, x = gameState.playMove(move)
			self.updateHash(self.hash, self.zobristArr[y][x][gameState.getCurrentPlayer()], self.zobristArr[y][x][0])
			self.changePlayer(gameState)

			value = -self.alphaBetaDL( -beta, -alpha, depth - 1, gameState)
			print('Move:', move, 'Time:', time.time() - start)
			if value > alpha:
				alpha = value
				bestMove = move

			self.hash = oldHash
			self.undo(y, x, gameState, previousYX)

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
			# move = legalMoves.pop()
			self.nodes += 1
			#<---Play the move on a copy of the board
			oldHash = self.hash
			#<---Update the hash
			previousYX = gameState.previousYX
			y, x = gameState.playMove(move)
			self.updateHash(self.hash, self.zobristArr[y][x][gameState.getCurrentPlayer()], self.zobristArr[y][x][0])
			#<---UPDATE THE CURRENT PLAYER
			self.changePlayer(gameState)
		
			value = -self.alphaBetaDL(-beta, -alpha, depth - 1, gameState)

			if value > alpha:
				alpha = value

			#<---Revert to previous hash and undo move from board
			self.hash = oldHash
			self.undo(y, x, gameState, previousYX)
			if self.nodes % 100000 == 0:
				print(self.nodes)
			if value >= beta:

				return self.updateTT(beta)

		return self.updateTT(alpha)

	def changePlayer(self, gameState):
		gameState.setCurrentPlayer( 3 - gameState.getCurrentPlayer())

	def undo(self, y, x, gameState, previous):
		self.changePlayer(gameState)
		gameState.setBoardPosition(y, x, 0)
		gameState.previousYX = previous

	def isTerminal(self, legalMoves, gameState):

		#<---If you can win + 10000            
		if gameState.previousYX != None:
			#<----If we are in a terminal state--->
			self.changePlayer(gameState)
			isWin, winType = gameState.checkWin(gameState.previousYX[1],gameState.previousYX[0])
			self.changePlayer(gameState)
			if isWin:
				return True, 1
			
			elif len(legalMoves) == 0:
				return True, 0 
		
		return False, None

	# def orderLegalMoves()

	def evaluation(self, gameState):
		#1000 for 4 in a row
		#50 for 3 in a row
		#10 for 2 in a row
		#Only add if they have at least 1 empty next to it
		cp = gameState.getCurrentPlayer()
		opponent = 3 - cp
		board = gameState.getBoard()
		playerScores = {2:0, 3:0, 4:0}
		opponentScores = {2:0, 3:0, 4:0}

		#<---Count Horizontal--->
		for row in range(gameState.boardSize[0]):
			p, op = self.getInRow(board[row] , cp, opponent)
			playerScores = self.addToScore(playerScores, p)
			opponentScores = self.addToScore(opponentScores, op)

		#<---Count vertical--->
		for col in range(gameState.boardSize[1]):
			p, op = self.getInRow(board[:,col] , cp, opponent)
			playerScores = self.addToScore(playerScores, p)
			opponentScores = self.addToScore(opponentScores, op)
			
		#<---Count Diagonal--->
		#This will only work for gameboards of size (6,7)  
		for diag in range(-2, 4):
			p, op = self.getInRow(board.diagonal(diag), cp, opponent)
			playerScores = self.addToScore(playerScores, p)
			opponentScores = self.addToScore(opponentScores, op)
			#<---Count anti diagonal--->
			p2, op2 = self.getInRow(np.fliplr(board).diagonal(diag), cp, opponent)
			playerScores = self.addToScore(playerScores, p2)
			opponentScores = self.addToScore(opponentScores, op2)
					
		score = self.calculateScore(playerScores) - self.calculateScore(opponentScores)

		return score

	def getInRow(self, arr, player, opponent):
		inRowCount = {2:0,3:0,4:0}
		inRowCountOpp = {2:0,3:0,4:0}
		inRow = 0
		previous = None
		itemBeforeSequence = None
		arrLen = len(arr)
		for i in range(arrLen):
			if arr[i] != 0:
				
				if previous == None:
					inRow += 1

				else:
					if previous == arr[i]:
						#<---If the current pos is who we are counting--->
						inRow += 1

					else:
						#<---If the current position is not who we are currently counting--->

						if itemBeforeSequence == 0 or inRow >= 4:
							inRow = 4 if inRow > 4 else inRow
							if inRow > 1:
								if previous == player:
									inRowCount[inRow] += 1
								elif previous == opponent:
									inRowCountOpp[inRow] += 1

						itemBeforeSequence = previous
						inRow = 1

						
			else:
				inRow = 4 if inRow > 4 else inRow 
				#<---If the current position is empty--->
				if inRow > 1:
					if previous == player:
						inRowCount[inRow] += 1
					elif previous == opponent:
						inRowCountOpp[inRow] += 1

				inRow = 0 #<---Reset the inRow count
				itemBeforeSequence = 0 
				previous = 0 
			
			if i != arrLen - 1:
				previous = arr[i]
		
		if itemBeforeSequence == 0 and inRow > 1:
			inRow = 4 if inRow > 4 else inRow
			if previous == player:
				inRowCount[inRow] += 1
			elif previous == opponent:
				inRowCountOpp[inRow] += 1

		return inRowCount, inRowCountOpp


	def calculateScore(self, scoreDict):
		score = ((scoreDict[4] * 10000) + (scoreDict[3] * 50) + (scoreDict[2] * 5))
		return score

	def addToScore(self, total, lineScore):
		total[2] += lineScore[2]
		total[3] += lineScore[3]
		total[4] += lineScore[4]
		return total



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

	def updateTT(self, value):
		self.tt.store(self.hash, value)
		return value
	
