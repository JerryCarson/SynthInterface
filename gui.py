from faulthandler import disable
import port as port
import numpy as np
from appJar import gui 
import os
import signal_presets

app = gui("Serial Communication")

def pressRB(rb):
    if app.getRadioButton("ft") != "Use preset":
        app.disableOptionBox("Signal preset")
    else:
        app.enableOptionBox("Signal preset")

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
    x = np.arange(0.0, np.size(y))#/int(app.getEntry("Frequency")), 1/int(app.getEntry("Frequency")))
    return x, y

def showLabels():
    axes.set_xlabel("Time")
    axes.set_ylabel("Amplitude")
    app.refreshPlot("p1")

def press(button):
    if button == "Cancel":
        app.stop()
    else:
        if app.getTabbedFrameSelectedTab("TabbedFrame") == "Simple signals":
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
                if app.getOptionBox("Signal preset") == "sin":
                    signal_presets.sine(app)
                elif app.getOptionBox("Signal preset") == "pulse":
                    signal_presets.square(app)
                c = port.SerialWrite(
                    app.getEntry("COM port name"),
                    app.getEntry("Baud rate"),
                    "input.txt", app
                )
                c.comWrite()
        elif app.getTabbedFrameSelectedTab("TabbedFrame") == "OFDM generation":
            signal_presets.ofdm(app.getEntry("Frequency samples"), app.getEntry("Number of carriers"), app.getEntry("QAM order"), app.getEntry("Pilots distance"), app)
            c = port.SerialWrite(
                        app.getEntry("COM port name"),
                        app.getEntry("Baud rate"),
                        "input.txt", app
                    )
            c.comWrite()

        axes = app.updatePlot("p1", *getXY())
        showLabels()

app.startTabbedFrame("TabbedFrame")
app.startTab("Simple signals")
app.setExpand("both")
app.addRadioButton("ft", "Use file", 0, 0)
app.addRadioButton("ft", "Use text", 1, 0)
app.addRadioButton("ft", "Use preset", 2, 0)
app.addLabelOptionBox("Signal preset", ["- Presets -", "sin", "pulse"], 3, 0)
app.addFileEntry("f1", 4, 0)
# app.addLabelEntry("Frequency", 5, 0)
app.addTextArea("t1", 6, 0)
app.addLabelEntry("COM port name", 7, 0)
app.addLabelEntry("Baud rate", 8, 0)
app.addVerticalSeparator(0, 1, 0, 10, colour="black")
app.setEntry("COM port name", "COM1")
app.setEntry("Baud rate", 9600)
# app.setEntry("f1", "C://Users//1//Desktop/s.txt")
# app.setEntry("Frequency", 1000)
app.disableOptionBox("Signal preset")
app.setRadioButtonChangeFunction("ft", pressRB)
app.setStopFunction(checkStop)

app.stopTab()

app.startTab("OFDM generation")

app.setExpand("both")
# app.setSticky("nw")
# app.addFileEntry("f2")
app.addTextArea("t2")
app.addLabelEntry("Frequency samples")
app.addLabelEntry("Number of carriers")
app.addLabelEntry("QAM order")
app.addLabelEntry("Pilots distance")
app.setEntry("Frequency samples", 2048)
app.setEntry("Number of carriers", 16)
app.setEntry("QAM order", 8)
app.setEntry("Pilots distance", 12)

app.stopTab()
app.stopTabbedFrame()

app.addButtons(["Submit", "Cancel"], press, 9, 0)
# app.addMessage("")
app.addWebLink("GitHub", "https://github.com/JerryCarson/SynthInterface")

f = open("input.txt", "w+")
f1 = open("output.txt", "w+")
axes = app.addPlot("p1", *getXY(), 0, 2, 10, 10)
showLabels()
app.go()
