import tkinter as tk
from tkinter import font as tkfont
import time
import fourInARow

class FourInARowGui(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        buttonFrame = tk.Frame(self)
        buttonFrame.pack(side='top', fill='x', expand=False)
        
        self.__p1 = tk.StringVar()
        self.__p2 = tk.StringVar()
        self.__diff = tk.StringVar()
        self.__p1.set('Player')
        self.__p2.set('Player')
        self.__diff.set('Easy')
        self.__game = fourInARow.Four_In_A_Row()

        self.__canvas = tk.Canvas(root, bg='white', height=525, width=600)
        self.__canvas.bind("<Button-1>", self.__click)
        
        self.__menu = tk.Menu(root)
        self.__createMenu(root)
        self.__drawBoard(root)
        

        


    def __createMenu(self, root):
        __playerOptions = ['Player', 'Computer']
        __difficultyOptions = ['Easy', 'Hard']
        
        #Submenus for self.__menu, tearoff gets rid of --- separator 
        p1OptionMenu = tk.Menu(root, tearoff=0)
        p2OptionMenu = tk.Menu(root, tearoff=0)
        diffOptionMenu = tk.Menu(root, tearoff=0)
            
        self.__menu.add_command(label=u"\u22EE", state='disabled' ,activebackground=self.__menu.cget('background'))

        self.__menu.add_command(label='New Game!', command=lambda: self.startGame(root))
        
        self.__menu.add_command(label=u"\u22EE", state='disabled' ,activebackground=self.__menu.cget('background'))
        
        
        self.__menu.add_cascade(label='Player 1: ' + self.__p1.get()+u' \u25BC', menu=p1OptionMenu)
        self.__menu.add_command(label=u"\u22EE", state='disabled' ,activebackground=self.__menu.cget('background'))

        self.__menu.add_cascade(label='Player 2: '+self.__p2.get()+u' \u25BC', menu=p2OptionMenu)
        
        for option in __playerOptions:
            p1OptionMenu.add_command(label=option, command=lambda x=option: self.__updateCommandLabel(x, self.__p1, 4 ))
            p2OptionMenu.add_command(label=option, command=lambda x=option: self.__updateCommandLabel(x, self.__p2, 6 ))
        
        self.__menu.add_command(label=u"\u22EE", state='disabled',activebackground=self.__menu.cget('background'))

        self.__menu.add_cascade(label='Difficulty: '+u'Easy \u25bc', menu=diffOptionMenu)
        for option in __difficultyOptions:
            diffOptionMenu.add_command(label=option, command=lambda x=option: self.__updateCommandLabel(x, self.__diff, 8))

        self.__menu.add_command(label=u"\u22EE", state='disabled',activebackground=self.__menu.cget('background'))

        self.__menu.add_command(label='Reset!', command=self.__resetGame)

        self.__menu.add_command(label=u"\u22EE", state='disabled',activebackground=self.__menu.cget('background'))


        root.config(menu=self.__menu)

    def __updateCommandLabel(self, option, strVar, index):
        
        strVar.set(option)
        if index == 8:
            pre = 'Difficulty: '
        elif index == 4:
            pre = 'Player 1: '
        elif index == 6:
            pre = 'Player 2: '
        self.__menu.entryconfigure(index, label=pre + strVar.get()+u' \u25BC')



    def __click(self, event):
        item = self.__canvas.find_closest(event.x, event.y)
        # current = self.__game.getCurrentPlayer()
        try:
            move = self.__canvas.gettags(item)[0]
            if move != 'current':
                tknSpaces = 
            self.__placeTkn(move)
        except:
            pass

    def __resetGame(self):
        self.__game.resetGame()
        tokenSpaces = self.__canvas.find_withtag('token')
        for i in tokenSpaces:
            self.__canvas.itemconfig(i, fill='white')

        self.__menu.entryconfigure(4, state='active')
        self.__menu.entryconfigure(6, state='active')
        self.__menu.entryconfigure(8, state='active')



        

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
        self.__menu.entryconfigure(8, state='disabled')
        

        
        


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
    