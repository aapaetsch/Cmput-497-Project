#This file generates the scores of each possible row for a game of four in a row
#It is from the view of the current player

from itertools import combinations_with_replacement as cwr 
from itertools import permutations
from itertools import groupby
import re
import json

def iterations(arr, length):
	#<---This function generates all possible rows for connect 4 of a given length--->
	possible = []
	combs = list(cwr(arr, length))
	for c in combs:
		c = list(c)
		if c not in possible:
			perms = permutations(c)
			for p in perms:
				p = list(p)
				if p not in possible:
					possible.append(p)

	return possible

def isLegal(arr, toggle):
	#<---This function checks if a row is a legal row for connect 4--->
	arr = list(arr)
	#<---All arrays of length = 4 are legal ---> 
	if len(arr) == 4:
		return True

	if toggle == 'comb':
		for a, b in groupby(arr):
			if len(list(b)) == len(arr) and a != 0:
				return False
		return True
	else:
		for a, b in groupby(arr):
			if len(list(b)) >= 5 and a != 0:
				return False
		return True


def getScore(arr):
	#<---This function calculates the score for the player and opponent of a given row--->
	strArr = ''.join([str(i) for i in arr])

	if re.search(r'1111', strArr):
		return [10000  ,0]

	elif re.search(r'2222', strArr):
		return [0,10000]

	else:
		score , bounds = checkZeros( [], strArr, r'111')
		s , _ = checkZeros( bounds, strArr, r'11')
		score += s
		
		opponentScore , bounds2 = checkZeros( [], strArr, r'222')
		oS , _ = checkZeros( bounds2, strArr, r'22')
		opponentScore += oS

	return [score , opponentScore]



def checkZeros(bounds, strArr, regex):
	#<---This function finds how many tokens in a row a player has, assigns it a score based on leading and trailing zeros (usefulness) --->
	matchObj = re.finditer(regex, strArr)
	score = 0 

	if matchObj != None:
		
		if regex == r'111' or regex == r'222':
			#<---We must keep track of the bounds for a 3 in a row to avoid collisions with two in a row--->
			for match in matchObj:
				bound = match.span()
				zeros = 0
				bounds += [b for b in range(bound[0], bound[1])]
				zeros += 1 if bound[0] > 0 and strArr[bound[0] - 1] == '0' else 0
				zeros += 1 if bound[1] < len(strArr) and strArr[bound[1]] == '0' else 0
				score += zeros * 10  
				# print('Score: {} Zeros: {} Bounds: {} String: {}'.format(score, zeros, bound, strArr))

		else:
			#<---We must check if two in a row matches are part of a three in a row set--->
			for match in matchObj:
				bound = match.span()
				zeros = 0 
				if bound[0] not in bounds and bound[1]-1 not in bounds:				
					zeros += 1 if bound[0] > 0 and strArr[bound[0] - 1] == '0' else 0 
					zeros += 1 if bound[1] < len(strArr) and strArr[bound[1]] == '0' else 0 
				score += zeros * 2

	return score, bounds

def generateScore(array):
	#<---This function generates the score dict for a given length of array-->
	s = {}
	for row in array:
		#<---Calculate a row address--->
		# address = 0 
		# for i in range(len(row)):
		# 	address += row[i] * 4 ** i 

		#<---Find its player and opponent score--->
		# s[address] = getScore(row)
		s[str(row)] = getScore(row)
	return s

def createScoreFile(FileName):
	#<---This function generates a score file--->
	Scores = {4:{}, 5:{}, 6:{}, 7:{}}
	arr = [0,1,2]
	
	for i in range(4, 8):
		rows = iterations(arr, i)
		Scores[i] = generateScore(rows)

	with open(FileName, 'w') as f:
		f.write(json.dumps(Scores))

if __name__ == '__main__':
	createScoreFile('scores.json')