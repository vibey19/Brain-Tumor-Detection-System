import tkinter as tk
from PIL import ImageTk, Image


class Frames:
    def __init__(self, mainObj, MainWin, wWidth, wHeight, function, Object, xAxis=10, yAxis=10):
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.MainWindow = MainWin
        self.MainObj = mainObj
        self.MainWindow.title("Brain Tumor Detection")

        self.method = function
        self.callingObj = None

        self.winFrame = tk.Frame(
            self.MainWindow, width=wWidth, height=wHeight, borderwidth=5, relief='ridge')
        self.winFrame.place(x=xAxis, y=yAxis)

        self.btnClose = tk.Button(
            self.winFrame, text="Close", width=8, command=lambda: self.quitProgram(self.MainWindow))
        self.btnClose.place(x=1020, y=600)

        self.btnView = tk.Button(
            self.winFrame, text="View", width=8, command=lambda: self.NextWindow(self.method))
        self.btnView.place(x=900, y=600)

        self.labelImg = None

    def quitProgram(self, window):
        window.destroy()

    def unhide(self):
        self.winFrame.place(x=self.xAxis, y=self.yAxis)

    def hide(self):
        self.winFrame.place_forget()

    def NextWindow(self, methodToExecute):
        listWF = list(self.MainObj.listOfWinFrame)

        if self.method == 0 or self.callingObj == 0:
            print("Calling Method or the Object from which Method is called is 0")
            return

        if self.method != 1:
            methodToExecute()

        if self.callingObj == self.MainObj.DT:
            img = self.MainObj.DT.getImage()

        jpgImg = Image.fromarray(img)
        current = 0

        for i in range(len(listWF)):
            listWF[i].hide()
            if listWF[i] == self:
                current = i

        if current == len(listWF) - 1:
            listWF[current].unhide()
            listWF[current].readImage(jpgImg)
            listWF[current].displayImage()
            self.btnView['state'] = 'disable'
        else:
            listWF[current + 1].unhide()
            listWF[current + 1].readImage(jpgImg)
            listWF[current + 1].displayImage()

        print("Step " + str(current) + " Extraction complete!")

    def readImage(self, img):
        self.image = img

    def setCallObject(self, obj):
        """Sets the calling object."""
        self.callingObj = obj

    def displayImage(self):
        imgTk = self.image.resize((250, 250), Image.Resampling.LANCZOS)
        imgTk = ImageTk.PhotoImage(image=imgTk)
        self.image = imgTk
        if self.labelImg:
            self.labelImg.configure(image=self.image)
        else:
            self.labelImg = tk.Label(self.winFrame, image=self.image)
            self.labelImg.place(x=700, y=150)
