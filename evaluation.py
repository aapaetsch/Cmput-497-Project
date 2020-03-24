	def evaluation(self, gameState):
		s = time.time()
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
					
		score = self.calculateScore(playerScores, False) - self.calculateScore(opponentScores, True)
		self.evalTimes.append(time.time()-s)
		return score

	def getInRow(self, arr, player, opponent):
		s = time.time()
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
		self.inRowTime.append(time.time() - s)
		return inRowCount, inRowCountOpp