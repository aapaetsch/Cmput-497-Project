import tkinter as tk
from tkinter import font as tkfont
import time
import fourInARow
from Computer_Player import FourInARow_AB

class FourInARowGui(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        buttonFrame = tk.Frame(self)
        buttonFrame.pack(side='top', fill='x', expand=False)
        
        self.__p1 = tk.StringVar()
        self.__p2 = tk.StringVar()

        self.__p1.set('Player')
        self.__p2.set('Player')

        
        self.__game = fourInARow.Four_In_A_Row()

        self.__canvas = tk.Canvas(root, bg='white', height=525, width=600)
        self.__canvas.bind("<Button-1>", self.__click)
        
        self.__menu = tk.Menu(root)
        self.__createMenu(root)
        self.__drawBoard(root)
        self.__gameStarted = False
        self.__allowClick = True
        

        


    def __createMenu(self, root):
        __playerOptions = ['Player', 'Easy Computer', 'Hard Computer']
        
        #Submenus for self.__menu, tearoff gets rid of --- separator 
        p1OptionMenu = tk.Menu(root, tearoff=0)
        p2OptionMenu = tk.Menu(root, tearoff=0)
        diffOptionMenu = tk.Menu(root, tearoff=0)
            
        self.__menu.add_command(label=u"\u22EE", state='disabled' ,activebackground=self.__menu.cget('background'))

        self.__menu.add_command(label='Start Game!', command=lambda: self.startGame(root))
        
        self.__menu.add_command(label=u"\u22EE", state='disabled' ,activebackground=self.__menu.cget('background'))
        
        
        self.__menu.add_cascade(label='Player 1: ' + self.__p1.get()+u' \u25BC', menu=p1OptionMenu)
        self.__menu.add_command(label=u"\u22EE", state='disabled' ,activebackground=self.__menu.cget('background'))

        self.__menu.add_cascade(label='Player 2: '+self.__p2.get()+u' \u25BC', menu=p2OptionMenu)
        
        for option in __playerOptions:
            p1OptionMenu.add_command(label=option, command=lambda x=option: self.__updateCommandLabel(x, self.__p1, 4 ))
            p2OptionMenu.add_command(label=option, command=lambda x=option: self.__updateCommandLabel(x, self.__p2, 6 ))
        
        self.__menu.add_command(label=u"\u22EE", state='disabled',activebackground=self.__menu.cget('background'))

        self.__menu.add_command(label='Reset!', command=self.__resetGame)

        self.__menu.add_command(label=u"\u22EE", state='disabled',activebackground=self.__menu.cget('background'))


        root.config(menu=self.__menu)

    def __updateCommandLabel(self, option, strVar, index):
        
        strVar.set(option)
        if index == 4:
            pre = 'Player 1: '
        elif index == 6:
            pre = 'Player 2: '
        self.__menu.entryconfigure(index, label=pre + strVar.get()+u' \u25BC')



    def __click(self, event):
        if self.__gameStarted and self.__allowClick:
            item = self.__canvas.find_closest(event.x, event.y)
            # current = self.__game.getCurrentPlayer()
            try:
                move = self.__canvas.gettags(item)[0]
                self.__placeTkn(move)
                self.__computerTurn()
            except:
                pass

    def __resetGame(self):
        self.__game.resetGame()
        tokenSpaces = self.__canvas.find_withtag('token')
        for i in tokenSpaces:
            self.__canvas.itemconfig(i, fill='white')
        self.__menu.entryconfigure(4, state='active')
        self.__menu.entryconfigure(6, state='active')
        self.__gameStarted == False



        

    def __placeTkn(self,move):
        if move != 'current':
            tokenSpaces = self.__canvas.find_withtag('token')
            board = self.__game.getBoard()

            if self.__game.turn(move):

                for y in range(len(board)):
                    for x in range(len(board[y])):

                        if board[y][x] == 1:
                            self.__canvas.itemconfig(tokenSpaces[y*7 + x], fill='red')
                        elif board[y][x] == 2:
                            self.__canvas.itemconfig(tokenSpaces[y*7 + x], fill='yellow')
                print(board)
            
            else:
                print("Invalid move")



    def __displayPlayerToGo(self, root):
        playerTurn = tk.StringVar()


    def startGame(self, root):
        self.__menu.entryconfigure(4, state='disabled')
        self.__menu.entryconfigure(6, state='disabled')
        self.__gameStarted = True
        

        if self.__p1.get().split(' ')[1] == 'Computer' and self.__p2.get().split(' ')[1] == 'Computer':
            self.__gameType = 'cc'
            print('Triggered')
            self.__computer_vs_Computer()





    def __computer_vs_Computer(self):

        if self.__p1.get().split(' ')[0] == 'Easy':
            depthC1 = 3
        else:
            depthC1 = 10

        if self.__p2.get().split(' ')[0] == 'Easy':
            depthC2 = 3
            print('A')
        else:
            depthC2 = 10

            cpu1 = FourInARow_AB(depthC1)
            print('cpu1 loaded')
            cpu2 = FourInARow_AB(depthC2)
            print('a')
            while not self.__game.getWinStatus():
                print('Turn')
                if self.__game.getCurrentPlayer() == 1:
                    #CPU 1 Plays
                    move = cpu1.findMove(self.__game)

                else:
                    #CPU 2 Plays
                    move = cpu2.findMove(self.__game)

                self.__placeTkn(move)
                self.__canvas.update_idletasks()
                time.sleep(2)


    def __drawBoard(self, root):
        x0, x1, y0, y1 = [50, 550, 50, 500]
        boardBG = self.__canvas.create_polygon(x0, y0, x0, y1, x1, y1, x1, y0, fill='blue')

        x0Tkn, y0Tkn, x1Tkn, y1Tkn = [65, 115, 115, 65]
        for i in range(6):
            for j in range(7):              
                tag = j
                self.__canvas.create_oval(x0Tkn+(j*70), y0Tkn+(i*70), x1Tkn+(j*70), y1Tkn+(i*70), fill='white', tags=(tag,'token'))

        self.__canvas.pack()


def adjScreenPlacement(root, x, y):
    posRight = int(root.winfo_screenwidth()/2 - x/2)
    posDown = int(root.winfo_screenheight()/2 - y/2)
    root.geometry("+{}+{}".format(posRight, posDown))

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Four In A Row!')
    app = FourInARowGui(root)
    root.minsize(600,600)

    adjScreenPlacement(root, 700, 500)
    app.pack(side='top', fill='both', expand=True)
    root.mainloop()
    