#Alpha Beta code adapted from https://webdocs.cs.ualberta.ca/~c455/python/alphabeta_with_move.py
#Transposition Table adapted from https://webdocs.cs.ualberta.ca/~c455/python/transposition_table_simple.py
import random
import time
import re
import numpy as np
import math
import itertools
import json

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
		self.MoveScores = {}
		with open('scores.json', 'r') as f:
			for line in f:
				self.score = dict(json.loads(line))


	def findMove(self, gameState):
		#<---Creates the zobrist Array and sets the current hash--->
		self.tt = TranspositionTable()
		rootState = gameState.copyState()
		self.ComputerPlayer = rootState.getCurrentPlayer()
		# print('Computer: {}'.format(self.ComputerPlayer))

		self.zobristinit(rootState)
		self.heuristic = {0:0,1:0,2:0,3:0,4:0,5:0,6:0}	
		self.MoveScores = {}
		
		
		alpha = -float('Inf')
		beta = float("Inf")
		value, move = self.alphaBetaGetMove(alpha, beta, self.__maxDepth, rootState)
		# print('Best Move:', move, '\tValue:', value)

		return move if move != None else random.choice(rootState.getValidMoves())

	def alphaBetaGetMove(self, alpha, beta, depth, gameState):
		legalMoves = self.getMoveOrder(gameState.getValidMoves())
		d = self.__maxDepth - (self.__maxDepth - depth)
		bestMove = None

		#<---we should try move 3 first (center is strongest)
		if 3 in legalMoves:
			legalMoves.remove(3)
			legalMoves.append(3)
		

		while legalMoves:
			move = legalMoves.pop()
			start = time.time()
			oldHash = self.hash
			previousYX = gameState.previousYX
			y, x = gameState.playMove(move)

			self.updateHash(self.hash, self.zobristArr[y][x][gameState.getCurrentPlayer()], self.zobristArr[y][x][0])
			self.changePlayer(gameState)

			value = -self.alphaBetaDL( -beta, -alpha, depth - 1, gameState)
			# print('Value:',value)
			# print('Move:', move, 'Time:', time.time() - start)
			if value > alpha:
				alpha = value
				bestMove = move

			self.MoveScores[str(move)] = str(value)

			self.hash = oldHash
			self.undo(y, x, gameState, previousYX)

			if value >= beta:
				self.heuristic[move] += pow(2,d)
				return beta, bestMove

			legalMoves = self.getMoveOrder(legalMoves)

		return alpha, bestMove

	def alphaBetaDL(self, alpha, beta, depth, state):
		
		result = self.tt.lookup(self.hash)
		if result !=  None:
			return result

		gameState = state.copyState()
		d = self.__maxDepth - (self.__maxDepth - depth)

		

		legalMoves = self.getMoveOrder(gameState.getValidMoves())
		#<---Is terminal needs a state--->
		if self.isTerminal(legalMoves, gameState) or depth == 0:
			return self.evaluation(gameState)

		while legalMoves:
			move = legalMoves.pop()
			#<---Play the move on a copy of the board
			oldHash = self.hash
			#<---Update the hash
			previousYX = gameState.previousYX
			y, x = gameState.playMove(move)

			self.updateHash(self.hash, self.zobristArr[y][x][gameState.getCurrentPlayer()], self.zobristArr[y][x][0])
			self.changePlayer(gameState)
		
			value = -self.alphaBetaDL(-beta, -alpha, depth - 1, gameState)
			

			if value > alpha:
				alpha = value

			#<---Revert to previous hash and undo move from board
			self.hash = oldHash
			self.undo(y, x, gameState, previousYX)

			if value >= beta:
				self.heuristic[move] += pow(2,d)
				return self.updateTT(beta)

			legalMoves = self.getMoveOrder(legalMoves)

		return self.updateTT(alpha)



	def getMoveOrder(self, moves):
		return sorted([m for m in moves], key = lambda m: self.heuristic[m])

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
				return True
			
			elif len(legalMoves) == 0:
				return True 

		return False

	def evaluation(self, gameState):
		cp = gameState.getCurrentPlayer()
		board = gameState.getBoard()
		p1Score = 0 
		p2Score = 0 

		for row in range(gameState.boardSize[0]):
			s = self.score[str(gameState.boardSize[1])][self.getAddress(board[row])]
			p1Score += s[0]
			p2Score += s[1]

		for col in range(gameState.boardSize[1]):
			s = self.score[str(gameState.boardSize[0])][self.getAddress(board[:,col])]
			p1Score += s[0]
			p2Score += s[1]

		s = self.diagonalEvaluation(board)
		p1Score += s[0]
		p2Score += s[1]

		s = self.diagonalEvaluation(np.fliplr(board))
		p1Score += s[0]
		p2Score += s[1]

		if self.ComputerPlayer == 1:
			return p1Score - p2Score * 1.1
		return p2Score - p1Score * 1.1


	def diagonalEvaluation(self, board):
		p1Score = 0 
		p2Score = 0 
		lengths = ['4','5','6','6','5','4']
		diags = [-2,-1,0,1,2,3]
		for i in range(6):
			s = self.score[lengths[i]][self.getAddress(board.diagonal(diags[i]))]
			p1Score += s[0]
			p2Score += s[1]
		return p1Score, p2Score


	def zobristinit(self, gameState):

		self.zobristArr = []
		for i in range(gameState.boardSize[0]):
			self.zobristInnerArr = []
			for j in range(gameState.boardSize[1]):
				self.zobristInnerArr.append([random.getrandbits(128) for _ in range(3)])
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
	
	def getAddress(self, arr):
		return str(list(arr))

	def showScores(self):
		text = ''
		c = 1 
		for key in self.MoveScores.keys():
			text += 'Move: {}, Score: {}\t'.format(key,self.MoveScores[key])

			if c == 3:
				text += '\n'
				c = 1 
			else:
				c += 1
		print(text)
			


	def saveScores(self, board, value, move):
		self.boards.append(board)
		self.boardScores.append(str(value))
		self.boardMoves.append(str(move))