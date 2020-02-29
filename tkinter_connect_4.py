import tkinter as tk
from tkinter import font as tkfont
import time
import fourInARow

class FourInARowGui(tk.Frame):
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)

		buttonFrame = tk.Frame(self)
		buttonFrame.pack(side='top', fill='x', expand=False)
		
		self.__p1 = None
		self.__p2 = None
		self.__diff = None
		self.__game = None

		self.__canvas = tk.Canvas(root, bg='white', height=525, width=600)
		self.__canvas.bind("<Button-1>", self.__click)
		
		self.__menuBar(root)
		self.__drawBoard(root)
		

		


	def __menuBar(self, root):
		__playerOptions = ['Player', 'Computer']
		__difficultyOptions = ['Easy', 'Hard']
		# __firstPlayerOptions = ['Red','Yellow']
		

		menuBar = tk.Menu(self)
		menuBar.add_command(label='Quit!', command=self.quit)
		menuBar.add_separator()
		menuBar.add_command(label='New Game!', command=lambda: self.startGame(root))
		menuBar.add_separator()

		
		


		root.config(menu=menuBar)

	def __colSelect(self, col):
		print("Column Click {}".format(col))

	def __click(self, event):
		item = self.__canvas.find_closest(event.x, event.y)
		# current = self.__game.getCurrentPlayer()
		try:
			move = self.__canvas.gettags(item)[0]
			self.__placeTkn(move)
		except:
			pass


		

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
		self.__game = fourInARow.Four_In_A_Row()

		
		


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
	app = FourInARowGui(root)
	root.minsize(600,600)
	adjScreenPlacement(root, 700, 500)
	app.pack(side='top', fill='both', expand=True)
	root.mainloop()
	