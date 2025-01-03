import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from displayTumor import DisplayTumor
from frames import Frames
from predictTumor import predictTumor


class Gui:
    def __init__(self):
        self.MainWindow = tk.Tk()
        self.MainWindow.geometry('1200x720')
        self.MainWindow.resizable(width=False, height=False)

        self.DT = DisplayTumor()

        self.fileName = tk.StringVar()

        self.FirstFrame = Frames(self, self.MainWindow, 1180, 700, 0, 0)
        self.FirstFrame.btnView['state'] = 'disable'

        self.listOfWinFrame = [self.FirstFrame]

        windowLabel = tk.Label(self.FirstFrame.winFrame,
                               text="Brain Tumor Detection", height=1, width=40)
        windowLabel.place(x=320, y=30)
        windowLabel.configure(background="White", font=(
            "Comic Sans MS", 16, "bold"))

        self.val = tk.IntVar()
        rb1 = tk.Radiobutton(self.FirstFrame.winFrame, text="Detect Tumor",
                             variable=self.val, value=1, command=self.check)
        rb1.place(x=250, y=200)

        rb2 = tk.Radiobutton(self.FirstFrame.winFrame, text="View Tumor Region",
                             variable=self.val, value=2, command=self.check)
        rb2.place(x=250, y=250)

        browseBtn = tk.Button(self.FirstFrame.winFrame,
                              text="Browse", width=8, command=self.browseWindow)
        browseBtn.place(x=800, y=550)

        self.MainWindow.mainloop()

    def browseWindow(self):
        fileOpenOptions = dict(defaultextension='*.*', filetypes=[(
            'jpg', '*.jpg'), ('png', '*.png'), ('jpeg', '*.jpeg'), ('All Files', '*.*')])
        self.fileName = filedialog.askopenfilename(**fileOpenOptions)
        image = Image.open(self.fileName)
        imageName = str(self.fileName)
        mriImage = Image.open(imageName)
        self.listOfWinFrame[0].readImage(image)
        self.listOfWinFrame[0].displayImage()
        self.DT.readImage(image)

    def check(self):
        if self.val.get() == 1:
            self.listOfWinFrame = [self.FirstFrame]
            self.listOfWinFrame[0].setCallObject(self.DT)

            res = predictTumor(self.DT.getImage())

            resLabel = tk.Label(self.FirstFrame.winFrame, text="Tumor Detected" if res >
                                0.5 else "No Tumor", height=1, width=20)
            resLabel.configure(background="White", font=(
                "Comic Sans MS", 16, "bold"), fg="red" if res > 0.5 else "green")
            resLabel.place(x=700, y=450)

        elif self.val.get() == 2:
            self.listOfWinFrame = [self.FirstFrame]
            self.listOfWinFrame[0].setCallObject(self.DT)
            self.listOfWinFrame[0].setMethod(self.DT.removeNoise)

            secFrame = Frames(self, self.MainWindow, 1180,
                              700, self.DT.displayTumor, self.DT)
            self.listOfWinFrame.append(secFrame)

            for i in range(len(self.listOfWinFrame)):
                if i != 0:
                    self.listOfWinFrame[i].hide()
            self.listOfWinFrame[0].unhide()
            if len(self.listOfWinFrame) > 1:
                self.listOfWinFrame[0].btnView['state'] = 'active'


if __name__ == "__main__":
    Gui()
