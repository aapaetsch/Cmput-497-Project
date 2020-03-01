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
						afterSequenceEmpty = False
						if i != arrLen - 1:
							if arr[i+1] == 0:
								afterSequenceEmpty = True


						if itemBeforeSequence == 0 or afterSequenceEmpty or inRow >= 4:
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