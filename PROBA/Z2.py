
from tkinter import  *

class main:
    def __init__(self, master):

        self.master = master
        self.master.title("MENU")

        self.but1 = Button(self.master,
                           text = "RECORD",
                           command = self.record)
        self.but2 = Button(self.master,
                           text = "PRINT")

        #self.but1.bind("<Button-1>", self.record)

        self.but1.pack()
        self.but2.pack()

        self.master.mainloop()

        #self.title = root.title("MENU")
        #self.frame = Frame(root, width = 170, height = 23)
        #self.frame.pack()

        #root.mainloop()

    def record(self):
        Record(self.master)
        self.master.withdraw()




class Record:
    def __init__(self, master):

        self.slave = Toplevel(master)
        self.slave.title("RECORD")


        self.rbut_0 = Button(self.slave,
                             text = "RESET").grid(row = 1, column = 1, columspan = 4 )
        self.rbut_1 = Button(self.slave,
                   text = "INT").grid(row = 2, column = 1)
        self.rbut_2 =  Button(self.slave,
                   text = "UNSINGNED_INT").grid(row = 2, column = 1)
        self.rbut_3 = Button(self.slave,
                   text = "SINGLE").grid(row = 2, column = 1)
        self.rbut_4 = Button(self.slave,
                   text = "DOUBLE").grid(row = 2, column = 1)
        """
        self.rbut_0.pack()
        self.rbut_1.pack()
        self.rbut_2.pack()
        self.rbut_3.pack()
        self.rbut_4.pack()
        """
        self.slave.grab_set()
        self.slave.focus_set()
        self.slave.wait_window()

        self.slave.mainloop()

if __name__ == '__main__':
    root = Tk()
    main(root)