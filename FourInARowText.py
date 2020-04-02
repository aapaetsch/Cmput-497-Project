import fourInARow
import sys
import os
import time
from Computer_Player import FourInARow_AB

CLEARTOGGLE = False
DEBUG_MODE = True
previousMove = None
def game():
	global previousMove
	while True:
		
		mode, p1, difficulty = modeSelection()
		checkQuit(mode)
		

		game = fourInARow.Four_In_A_Row()

		if mode == 1:
			#Player vs. Player
			while True:
				clearScreen(CLEARTOGGLE)
				game.showBoard()
				print('Previous Move > {}'.format(previousMove))
				playerTurn(game)
				if checkWin(game):
					break

		elif mode == 2:
			#Player vs. Computer
			showScores = showStats()
			depth = getDepth(difficulty)
			cpu = FourInARow_AB(depth)
		
			while True:
				clearScreen(CLEARTOGGLE)
				game.showBoard()
				print('Previous Move > {}'.format(previousMove))
				if p1 == 1:
					playerTurn(game) if game.getCurrentPlayer() == 1 else computerTurn(game, cpu)

				else:
					playerTurn(game) if game.getCurrentPlayer() == 2 else computerTurn(game, cpu)

				if checkWin(game):
					break
					

		elif mode == 3:
			showScores = showStats()
			depth1 = getDepth(difficulty[0])
			cpu1 = FourInARow_AB(depth1)

			depth2 = getDepth(difficulty[1])
			cpu2 = FourInARow_AB(depth2)

			while True:
				clearScreen(CLEARTOGGLE)
				game.showBoard()
				print('Previous Move > {}'.format(previousMove))
				computerTurn(game, cpu1) if game.getCurrentPlayer() == 1 else computerTurn(game, cpu2)

				if checkWin(game):
					break

				time.sleep(1)
		
		if input('Play Again? (y/n) > ').lower() != 'y':
			break
		


def playerTurn(game):
	global previousMove
	while True:
		move = input('Player {} Turn > '.format(game.getCurrentPlayer()))
		
		if move.lower() == 'q':
			sys.exit()
		
		elif game.turn(move):
			previousMove = move
			break
		
		print('Error Invalid Move!')


def computerTurn(game, cpu):
	global previousMove
	move = cpu.findMove(game)
	cpu.showScores()
	game.turn(move)
	previousMove = move

def getDepth(diff):
	
	if diff == 1:
		return 2
	elif diff == 2:
		return 4
	elif diff == 3:
		return 8


def checkWin(game):

	if game.getWin():
		game.showBoard()
		if DEBUG_MODE:
			print('Win Type: {}'.format(game.getWinType()))
		print('\nPlayer {} Wins!'.format(game.getWinner()))
		return True

	elif len(game.getValidMoves()) == 0:
		print('Game Is A Draw!')
		return True

	return False

def modeSelection():

	clearScreen(True)
	p1 = None
	diff = None
	while True:
		x = input('Four In A Row!\n1: Player vs. Player\
		\n2: Player vs. Computer\n3: Computer vs. Computer\
		\n4: Quit\nGame Mode > ')

		try:
			assert 1 <= int(x) <= 4

			if int(x) == 2:
				
				while True:
					try:
						print('\nFirst Player')
						p1 = int(input('1: Player First\n2: Computer First\n> '))
						assert p1 == 1 or p1 == 2
						break
					except:
						print('Input must be 1 or 2.')
				diff = getCpuDiff('')
				
			
			elif int(x) == 3:
				diff1 = getCpuDiff('1')
				diff2 = getCpuDiff('2')
				diff = [diff1, diff2]  

			elif int(x) == 4:
				print('Quitting....')
				

			return int(x), p1, diff

				
		except:
			print('Error Invalid Mode!')

def getCpuDiff(text):
	while True:
		try:
			diff = input('\nComputer {} Difficulty\n1: Easy\n2: Medium\n3: Hard\n> '.format(text))
			assert 1 <= int(diff) <= 3
			return int(diff)
		except:
			print("Input must be between 1-3.")



def clearScreen(toggle):
	if toggle: os.system('cls' if sys.platform == 'win32' else 'clear')

def checkQuit(mode):
	if mode == 4:
		sys.exit()

def showStats():
	x = input("Would you like to see the scores for each computer move (y/n) > ").lower()
	return True if x == 'y' else False

if __name__ == '__main__':
	game()