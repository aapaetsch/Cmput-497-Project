import connect4
import easyComputer as eC
import sys
import os


CLEARTOGGLE = True  
DEBUG_MODE = True
def main():
  
    while True:
        
        mode = modeSelection()
        game = connect4.Connect4()

        while True:
            clearScreen(CLEARTOGGLE)
            game.showBoard()
            
            if mode == 'player':
                playerTurn(game)

            elif mode == 'easy':
                if game.getCurrentPlayer() == 1:
                    playerTurn(game)
                else:
                    validMoves = game.getValidMoves()
                    computerTurn(game, validMoves, 'e')

            elif mode == 'ysea':
                if game.getCurrentPlayer() == 2:
                    playerTurn(game)
                else:
                    validMoves = game.getValidMoves()
                    computerTurn(game, validMoves, 'e')

            elif mode == 'hard' or mode == 'drah':
                print("Error Mode not Implemeted")
                break


            if game.getWin():
                clearScreen(CLEARTOGGLE)
                game.showBoard()
                if DEBUG_MODE:
                    print("Win Type: {}".format(game.getWinType()))
                print("\nPlayer {} Wins!".format(game.getWinner()))
                break

            if len(game.getValidMoves()) == 0:
                print("Game Is A Draw!")
                break

        reset = input('Play Again? (y/n) >')

        if reset != 'y':
            break

def playerTurn(game):
    while True:
        move = input('Player {} Turn > '.format(game.getCurrentPlayer()))
        if game.turn(move):
            break
        else:
            print('Error Invalid Move!')

def computerTurn(game, validMoves, cType):
    if cType == 'e':
        move = eC.easyComputer(validMoves)
        game.turn(move)
    else:
        pass


def modeSelection():
    clearScreen(True)
    print('Connect 4!\n1: Player vs Player\
        \n2: Player vs Easy Computer\n3: Easy Computer vs Player\
        \n4: Player vs Hard Computer\n5: Hard Computer vs Player\
        \n6: Quit')
    while True:
        x = input("Game Mode > ")
        try:
            x = int(x)
            
            if x == 1:
                return 'player'
            elif x == 2: 
                return 'easy'
            elif x == 3:
                return 'ysea'
            elif x == 4:
                return 'hard'
            elif x == 5:
                return 'drah'
            elif x == 6:
                sys.exit()
            else:
                print('Error Invalid Mode!')
        except:
            print('Error Invalid Mode!')

def clearScreen(toggle):
    if toggle:
        os.system('cls' if sys.platform == 'win32' else 'clear')







if __name__ == "__main__":
    main()