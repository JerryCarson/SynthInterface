from faulthandler import disable
import port
import numpy as np
from appJar import gui 
import os
import signal_presets


app = gui("Serial Communication")
app.setSticky("news")
app.setExpand("both")
app.addRadioButton("ft", "Use file", 0, 0)
app.addRadioButton("ft", "Use text", 1, 0)
app.addRadioButton("ft", "Use preset", 2, 0)
app.addLabelOptionBox("Signal preset", ["- Presets -", "sin", "cos"], 3, 0)
app.addFileEntry("f1", 4, 0)
app.addLabelEntry("Frequency", 5, 0)
app.addTextArea("t1", 6, 0)
app.addLabelEntry("COM port name", 7, 0)
app.addLabelEntry("Baud rate", 8, 0)
app.addVerticalSeparator(0, 1, 0, 10, colour="black")
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
        elif app.getRadioButton("ft") == "Use file":
            c = port.SerialWrite(
                app.getEntry("COM port name"),
                app.getEntry("Baud rate"),
                app.getEntry("f1"), app
            )
            c.comWrite()
        elif app.getRadioButton("ft") == "Use preset":
            signal_presets.sine(app)
            c = port.SerialWrite(
                app.getEntry("COM port name"),
                app.getEntry("Baud rate"),
                "input.txt", app
            )
            c.comWrite()
        axes = app.updatePlot("p1", *getXY())
        showLabels()

def press(rb):
    if app.getRadioButton("ft") != "Use preset":
        app.disableOptionBox("Signal preset")
    else:
        app.enableOptionBox("Signal preset")

app.disableOptionBox("Signal preset")
app.setRadioButtonChangeFunction("ft", press)
app.setStopFunction(checkStop)
f = open("input.txt", "w+")
f1 = open("output.txt", "w+")
app.addButtons(["Submit", "Cancel"], press, 9, 0)
axes = app.addPlot("p1", *getXY(), 0, 2, 10, 10)
showLabels()
app.go()
