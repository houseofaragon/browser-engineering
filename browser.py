import tkinter
from url import URL
TK_SILENCE_DEPRECATION=1
"""
    import tkinter
    window = tkinter.Tk()
    tkinter.mainloop()

    // mainloop() is a blocking function that waits for events to happen
    while True:
        for evt in pendingEvents():
            handleEvent(evt)
        drawScreen()
"""

WIDTH, HEIGHT = 400, 400

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window, 
            width=WIDTH,
            height=HEIGHT, background="white"
        )
        self.canvas.pack()

    def load(self, url):
        self.canvas.create_rectangle(10, 20, 400, 300)
        self.canvas.create_oval(100, 100, 150, 150)
        self.canvas.create_text(200, 150, text="Hi!")

if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()