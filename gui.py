import port
import numpy as np
from appJar import gui 
import os


app = gui("Serial Communication")
app.setSticky("news")
app.setExpand("both")
app.addRadioButton("ft", "Use file", 0, 0)
app.addRadioButton("ft", "Use text", 1, 0)
app.addFileEntry("f1", 2, 0)
app.addLabelEntry("Frequency", 3, 0)
app.addTextArea("t1", 4, 0)
app.addLabelEntry("COM port name", 5, 0)
app.addLabelEntry("Baud rate", 6, 0)
app.addVerticalSeparator(0, 1, 0, 8, colour="black")
app.setEntry("COM port name", "COM1")
app.setEntry("Baud rate", 9600)
app.setEntry("f1", "C://Users//1//Desktop/s.txt")
app.setEntry("Frequency", 1000)


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
    x = np.arange(0.0, np.size(y)/int(app.getEntry("Frequency")), 1/int(app.getEntry("Frequency")))
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
            c = port.SerialWrite(
                app.getEntry("COM port name"), app.getEntry(
                    "Baud rate"), "input.txt", app
            )
            c.comWriteField()
        else:
            c = port.SerialWrite(
                app.getEntry("COM port name"),
                app.getEntry("Baud rate"),
                app.getEntry("f1"), app
            )
            c.comWrite()
        axes = app.updatePlot("p1", *getXY())
        showLabels()


app.setStopFunction(checkStop)
f = open("input.txt", "w+")
f1 = open("output.txt", "w+")
app.addButtons(["Submit", "Cancel"], press, 7, 0)
axes = app.addPlot("p1", *getXY(), 0, 2, 8, 8)
showLabels()
app.go()
