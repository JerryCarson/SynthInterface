import port
import numpy as np
from appJar import gui
import os


app = gui()
app.addRadioButton("ft", "Use file")
app.addRadioButton("ft", "Use text")
app.addFileEntry("f1")
app.addTextArea("t1")
app.addLabelEntry("COM port name")
app.addLabelEntry("Baud rate")
app.setEntry("COM port name", "COM1")
app.setEntry("Baud rate", 9600)
app.setEntry("f1", "C://Users//1//Desktop/s.txt")

def checkStop():
    f.close()
    f1.close()
    if os.path.exists("input.txt"):
        os.remove("input.txt")
    if os.path.exists("output.txt"):
        os.remove("output.txt")
    return app

def getXY():
    y = []
    with open("output.txt", "r") as input:
        for line in input:
            y.append(float(line))
    x = np.arange(0.0, np.size(y), 1)
    return x, y


def showLabels():
    axes.set_xlabel("Time")
    axes.set_ylabel("Amplitude")
    app.refreshPlot("p1")


def press(button):
    if button == "Cancel":
        app.stop()
    else:
        if app.getRadioButton("ft") == "Use text":
            with open("input.txt", "w") as input:
                for line in app.getTextArea("t1"):
                    input.write(line)
            c = port.SerialWrite(
                app.getEntry("COM port name"), app.getEntry("Baud rate"), "input.txt"
            )
        else:
            c = port.SerialWrite(
                app.getEntry("COM port name"),
                app.getEntry("Baud rate"),
                app.getEntry("f1"),
            )
        c.comWrite()
        axes = app.updatePlot("p1", *getXY())
        showLabels()

app.setStopFunction(checkStop)
f= open("input.txt","w+")
f1= open("output.txt","w+")
app.addButtons(["Submit", "Cancel"], press)
axes = app.addPlot("p1", *getXY())
showLabels()
app.go()
