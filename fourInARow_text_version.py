import fourInARow
import easyComputer as eC
import sys
import os
import time
from Computer_Player import FourInARow_AB
from computer_boolean import FourInARow_Bool_MinMax

CLEARTOGGLE = False  
DEBUG_MODE = True
def main():
    
    while True:
        
        mode = modeSelection()
        if mode == 'quit':
            sys.exit()
        game = fourInARow.Four_In_A_Row()
        
        if mode == 'easy' or mode == '2easy':
            depth = 3
        elif mode == 'hard' or mode == '2hard':
            #10 takes 14 sec
            #11 takes 111
            depth = 10
        else:
            depth = 0 

        computer = FourInARow_AB(depth)
        # computer = FourInARow_Bool_MinMax(depth)

        

        while True:
            clearScreen(CLEARTOGGLE)
            game.showBoard()
            
            if mode == 'player':
                playerTurn(game)

            elif mode == 'easy':
                if game.getCurrentPlayer() == 1:
                    playerTurn(game)
                else:
                    # game.turn(eC.easyComputer(game.getValidMoves()))
                    start = time.time()
                    game.turn(computer.findMove(game))
                    print('Turn Time:', time.time() - start)

            elif mode == '2easy':
                if game.getCurrentPlayer() == 2:
                    playerTurn(game)
                else:
                    #<Computer turn>
                    # game.turn(eC.easyComputer(game.getValidMoves()))
                    start = time.time()
                    game.turn(computer.findMove(game))
                    print('Turn Time:', time.time() - start)

            elif mode == 'hard':
                if game.getCurrentPlayer() == 1:
                    playerTurn(game)
                else:
                    start = time.time()
                    game.turn(computer.findMove(game))
                    print('Turn Time:', time.time() - start)


            elif mode == '2hard':
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


def modeSelection():
    clearScreen(True)
    print('Four In A Row!\n1: Player vs Player\
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
                return '2easy'
            elif x == 4:
                return 'hard'
            elif x == 5:
                return '2hard'
            # elif x == 6:
            #     return 'cc'
            elif x == 6:
                return 'quit'
            else:
                print('Error Invalid Mode!')
        except:
            print('Error Invalid Mode!')

def clearScreen(toggle):
    if toggle:
        os.system('cls' if sys.platform == 'win32' else 'clear')







if __name__ == "__main__":
    main()