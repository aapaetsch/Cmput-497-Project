import tkinter as tk

class connect4Gui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there['text'] = "hello world\n (click me)"
        self.hi_there['command'] = self.say_hi

        # self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        # self.quit.pack(side='bottom')

    def say_hi(self):
        print("Hi there!")


def main():

    root = tk.Tk()
    app = connect4Gui(master=root)
    app.master.title("Connect 4!")
    app.master.maxsize(1000,400)
    app.mainloop()









if __name__ == '__main__':
    main()